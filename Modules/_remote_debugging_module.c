/******************************************************************************
 * Python Remote Debugging Module (reduced)
 *
 * Reads another process's garbage collector statistics without pausing it or
 * loading anything into it.  Only the two entry points gcmon calls:
 *
 *   get_gc_stats(pid, *, all_interpreters=False)
 *   get_child_pids(pid, *, recursive=True)
 *
 * Unlike 3.14+ upstream, which reuses the incremental-collector slot inside
 * _gc_runtime_state to hold the ring pointer, 3.13 has no such spare slot, so
 * the pointer lives at the tail of PyInterpreterState instead.  The walk is
 * otherwise identical: follow _Py_DebugOffsets from the runtime to each
 * interpreter and read its ring.  See Include/internal/pycore_gc.h.
 *
 * Deliberately absent: RemoteUnwinder, stack reconstruction, asyncio task
 * inspection, and all of PEP 768's remote *execution* path.
 ******************************************************************************/

#define _GNU_SOURCE

#ifndef Py_BUILD_CORE_BUILTIN
#    define Py_BUILD_CORE_MODULE 1
#endif
#include "Python.h"
#include <internal/pycore_gc.h>             // struct gc_stats, NUM_GENERATIONS
#include <internal/pycore_interp.h>         // PyInterpreterState.generation_stats
#include <internal/pycore_runtime.h>        // _Py_DebugOffsets
#include <internal/pycore_pyerrors.h>       // _PyErr_Format
#include <internal/pycore_pystate.h>        // _PyInterpreterState_GET

/* 3.12's configure has no AC_CHECK_FUNCS([process_vm_readv]); that check
 * arrived with 3.13's _testexternalinspection.  remote_debug.h defaults the
 * macro to 0 when undefined, but on Linux it still calls
 * search_linux_map_for_section(), which that same macro guards, so an
 * undefined macro fails to compile rather than degrading.  Defining it here
 * is preferred over regenerating configure with a matching autoconf.
 * process_vm_readv() has been in Linux since 3.2 and glibc since 2.15.
 */
#ifndef HAVE_PROCESS_VM_READV
#  if defined(__linux__) && defined(__GLIBC__) \
      && (__GLIBC__ > 2 || (__GLIBC__ == 2 && __GLIBC_MINOR__ >= 15))
#    define HAVE_PROCESS_VM_READV 1
#  else
#    define HAVE_PROCESS_VM_READV 0
#  endif
#endif

#include "../Python/remote_debug.h"

#include <errno.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

#ifndef MS_WINDOWS
#include <unistd.h>
#include <dirent.h>
#endif

#ifdef MS_WINDOWS
#include <tlhelp32.h>
#endif

typedef struct {
    PyTypeObject *GCStatsInfo_Type;
} RemoteDebuggingState;

static inline RemoteDebuggingState *
RemoteDebugging_GetState(PyObject *module)
{
    void *state = PyModule_GetState(module);
    assert(state != NULL);
    return (RemoteDebuggingState *)state;
}

typedef struct {
    proc_handle_t handle;
    uintptr_t runtime_start_address;
    _Py_DebugOffsets debug_offsets;
    int debug;
} RuntimeOffsets;

#define set_exception_cause(offsets, exc_type, message)                        \
    do {                                                                      \
        assert(PyErr_Occurred() &&                                            \
               "function returned -1 without setting exception");             \
        if ((offsets)->debug && !_Py_RemoteDebug_HasPermissionError()) {      \
            _set_debug_exception_cause(exc_type, message);                    \
        }                                                                     \
    } while (0)

/* GCStatsInfo keeps 3.15's shape so that a consumer needs no version
   handling.  iid is the reporting interpreter's own id; with all_interpreters
   false only the main interpreter (id 0) is reported.  heap_size is 0 on this
   build: this patch adds no hooks to object tracking or untracking, exactly
   as the free-threaded build leaves it. */
static PyStructSequence_Field GCStatsInfo_fields[] = {
    {"gen", "GC generation number"},
    {"iid", "Reporting interpreter ID (0 when only the main one is recorded)"},
    {"ts_start", "Raw timestamp at collection start"},
    {"ts_stop", "Raw timestamp at collection stop"},
    {"collections", "Total number of collections"},
    {"collected", "Total number of collected objects"},
    {"uncollectable", "Total number of uncollectable objects"},
    {"candidates", "Total objects considered and traversed"},
    {"heap_size", "Live objects as of the last full collection"},
    {"duration", "Total collection time, in seconds"},
    {NULL}
};

static PyStructSequence_Desc GCStatsInfo_desc = {
    "_remote_debugging.GCStatsInfo",
    "Information about a garbage collector stats sample",
    GCStatsInfo_fields,
    10
};

/* ============================================================================
 * LOCATING THE INTERPRETERS
 * ========================================================================== */

static int
init_runtime_offsets(RuntimeOffsets *offsets, int pid, int debug)
{
    offsets->debug = debug;
    if (_Py_RemoteDebug_InitProcHandle(&offsets->handle, pid) < 0) {
        set_exception_cause(offsets, PyExc_RuntimeError,
                            "Failed to initialize process handle");
        return -1;
    }

    if (_Py_RemoteDebug_ReadDebugOffsets(&offsets->handle,
                                         &offsets->runtime_start_address,
                                         &offsets->debug_offsets) < 0) {
        set_exception_cause(offsets, PyExc_RuntimeError,
                            "Failed to read debug offsets");
        _Py_RemoteDebug_CleanupProcHandle(&offsets->handle);
        return -1;
    }

    /* _Py_DebugOffsets is deliberately left byte-identical to an unpatched
       build, so it carries no entry for the ring.  What it does publish,
       gc.size, still confirms that this reader and the target agree on
       struct _gc_runtime_state -- and therefore on the interpreter-state
       layout the ring pointer sits at the tail of.  The ring's own offset
       comes from the local headers, which is sound because _remote_debugging
       already refuses to attach across a different major.minor. */
    if (offsets->debug_offsets.gc.size != sizeof(struct _gc_runtime_state)) {
        PyErr_Format(PyExc_RuntimeError,
                     "Remote _gc_runtime_state size (%llu) does not match "
                     "local size (%zu)",
                     (unsigned long long)offsets->debug_offsets.gc.size,
                     sizeof(struct _gc_runtime_state));
        set_exception_cause(offsets, PyExc_RuntimeError,
                            "Remote _gc_runtime_state size mismatch");
        _Py_RemoteDebug_CleanupProcHandle(&offsets->handle);
        return -1;
    }
    return 0;
}

static void
cleanup_runtime_offsets(RuntimeOffsets *offsets)
{
    _Py_RemoteDebug_CleanupProcHandle(&offsets->handle);
}

/* ============================================================================
 * READING THE RINGS
 * ========================================================================== */

static int
append_records(PyObject *result, PyTypeObject *type, unsigned long gen,
               int64_t iid, const struct gc_generation_stats *items,
               uint64_t count)
{
#define SET_FIELD(converter, expr) do { \
    PyObject *value = converter(expr); \
    if (value == NULL) { \
        goto error; \
    } \
    PyStructSequence_SetItem(item, field++, value); \
} while (0)

    PyObject *item = NULL;

    for (uint64_t i = 0; i < count; i++, items++) {
        item = PyStructSequence_New(type);
        if (item == NULL) {
            goto error;
        }
        Py_ssize_t field = 0;

        SET_FIELD(PyLong_FromUnsignedLong, gen);
        SET_FIELD(PyLong_FromLongLong, iid);

        SET_FIELD(PyLong_FromLongLong, items->ts_start);
        SET_FIELD(PyLong_FromLongLong, items->ts_stop);
        SET_FIELD(PyLong_FromSsize_t, items->collections);
        SET_FIELD(PyLong_FromSsize_t, items->collected);
        SET_FIELD(PyLong_FromSsize_t, items->uncollectable);
        SET_FIELD(PyLong_FromSsize_t, items->candidates);
        SET_FIELD(PyLong_FromSsize_t, items->heap_size);

        SET_FIELD(PyFloat_FromDouble, items->duration);

        int rc = PyList_Append(result, item);
        Py_CLEAR(item);
        if (rc < 0) {
            goto error;
        }
    }

#undef SET_FIELD
    return 0;

error:
    Py_XDECREF(item);
    return -1;
}

static int
append_ring(RuntimeOffsets *offsets, PyObject *result, PyTypeObject *type,
            int64_t iid, uintptr_t ring_addr)
{
    struct gc_stats stats;
    if (_Py_RemoteDebug_ReadRemoteMemory(&offsets->handle, ring_addr,
                                         sizeof(stats), &stats) < 0) {
        set_exception_cause(offsets, PyExc_RuntimeError,
                            "Failed to read per-interpreter GC statistics");
        return -1;
    }
    if (append_records(result, type, 0, iid, stats.young.items,
                       GC_YOUNG_STATS_SIZE) < 0) {
        return -1;
    }
    for (unsigned long gen = 1; gen < NUM_GENERATIONS; gen++) {
        if (append_records(result, type, gen, iid, stats.old[gen - 1].items,
                           GC_OLD_STATS_SIZE) < 0) {
            return -1;
        }
    }
    return 0;
}

static PyObject *
do_get_gc_stats(RuntimeOffsets *offsets, int all_interpreters,
                PyTypeObject *type)
{
    uintptr_t interpreters_head_addr =
        offsets->runtime_start_address
        + (uintptr_t)offsets->debug_offsets.runtime_state.interpreters_head;
    uintptr_t interpreter_id_offset =
        (uintptr_t)offsets->debug_offsets.interpreter_state.id;
    uintptr_t interpreter_next_offset =
        (uintptr_t)offsets->debug_offsets.interpreter_state.next;

    uintptr_t interp_addr = 0;
    if (_Py_RemoteDebug_ReadRemoteMemory(&offsets->handle,
                                         interpreters_head_addr,
                                         sizeof(void *), &interp_addr) < 0) {
        set_exception_cause(offsets, PyExc_RuntimeError,
                            "Failed to read interpreter state address");
        return NULL;
    }
    if (interp_addr == 0) {
        PyErr_SetString(PyExc_RuntimeError, "No interpreter state found");
        return NULL;
    }

    PyObject *result = PyList_New(0);
    if (result == NULL) {
        return NULL;
    }

    int64_t iid = 0;
    for (int count = 0; interp_addr != 0; count++) {
        if (count >= 1024) {
            PyErr_SetString(PyExc_RuntimeError,
                            "Interpreter list exceeds 1024 entries");
            goto error;
        }
        if (_Py_RemoteDebug_ReadRemoteMemory(&offsets->handle,
                                             interp_addr + interpreter_id_offset,
                                             sizeof(iid), &iid) < 0) {
            set_exception_cause(offsets, PyExc_RuntimeError,
                                "Failed to read interpreter id");
            goto error;
        }

        if (all_interpreters || iid == 0) {
            /* The ring pointer lives at the tail of PyInterpreterState.
               _remote_debugging refuses to attach across a different
               major.minor, so the local offsetof is the remote one. */
            uintptr_t ring_pointer_addr =
                interp_addr + offsetof(PyInterpreterState, generation_stats);
            uintptr_t ring_addr = 0;
            if (_Py_RemoteDebug_ReadRemoteMemory(&offsets->handle,
                                                 ring_pointer_addr,
                                                 sizeof(ring_addr),
                                                 &ring_addr) < 0) {
                set_exception_cause(offsets, PyExc_RuntimeError,
                                    "Failed to read GC statistics pointer");
                goto error;
            }
            if (ring_addr == 0) {
                PyErr_SetString(PyExc_RuntimeError,
                                "Target process does not expose GC statistics: "
                                "it is not running an interpreter with the GC "
                                "statistics patch applied");
                goto error;
            }
            if (append_ring(offsets, result, type, iid, ring_addr) < 0) {
                goto error;
            }
        }

        if (_Py_RemoteDebug_ReadRemoteMemory(&offsets->handle,
                                             interp_addr + interpreter_next_offset,
                                             sizeof(void *), &interp_addr) < 0) {
            set_exception_cause(offsets, PyExc_RuntimeError,
                                "Failed to read next interpreter state");
            goto error;
        }
    }
    return result;

error:
    Py_DECREF(result);
    return NULL;
}

/* ============================================================================
 * SUBPROCESS ENUMERATION
 *
 * Backported verbatim from 3.15's Modules/_remote_debugging/subprocess.c
 * (GH-142636, 6658e2cb07f).  gcmon calls get_child_pids() to follow a process
 * tree; the file is self-contained, so only its include of the package header
 * is dropped and the entry point is made static.
 * ========================================================================== */
/******************************************************************************
 * Remote Debugging Module - Subprocess Enumeration
 *
 * This file contains platform-specific functions for enumerating child
 * processes of a given PID.
 ******************************************************************************/


#ifndef MS_WINDOWS
#include <unistd.h>
#include <dirent.h>
#endif

#ifdef MS_WINDOWS
#include <tlhelp32.h>
#endif

/* ============================================================================
 * INTERNAL DATA STRUCTURES
 * ============================================================================ */

/* Simple dynamic array for collecting PIDs */
typedef struct {
    pid_t *pids;
    size_t count;
    size_t capacity;
} pid_array_t;

static int
pid_array_init(pid_array_t *arr)
{
    arr->capacity = 64;
    arr->count = 0;
    arr->pids = (pid_t *)PyMem_Malloc(arr->capacity * sizeof(pid_t));
    if (arr->pids == NULL) {
        PyErr_NoMemory();
        return -1;
    }
    return 0;
}

static void
pid_array_cleanup(pid_array_t *arr)
{
    if (arr->pids != NULL) {
        PyMem_Free(arr->pids);
        arr->pids = NULL;
    }
    arr->count = 0;
    arr->capacity = 0;
}

static int
pid_array_append(pid_array_t *arr, pid_t pid)
{
    if (arr->count >= arr->capacity) {
        /* Check for overflow before multiplication */
        if (arr->capacity > SIZE_MAX / 2) {
            PyErr_SetString(PyExc_OverflowError, "PID array capacity overflow");
            return -1;
        }
        size_t new_capacity = arr->capacity * 2;
        /* Check allocation size won't overflow */
        if (new_capacity > SIZE_MAX / sizeof(pid_t)) {
            PyErr_SetString(PyExc_OverflowError, "PID array size overflow");
            return -1;
        }
        pid_t *new_pids = (pid_t *)PyMem_Realloc(arr->pids, new_capacity * sizeof(pid_t));
        if (new_pids == NULL) {
            PyErr_NoMemory();
            return -1;
        }
        arr->pids = new_pids;
        arr->capacity = new_capacity;
    }
    arr->pids[arr->count++] = pid;
    return 0;
}

static int
pid_array_contains(pid_array_t *arr, pid_t pid)
{
    for (size_t i = 0; i < arr->count; i++) {
        if (arr->pids[i] == pid) {
            return 1;
        }
    }
    return 0;
}

/* ============================================================================
 * SHARED BFS HELPER
 * ============================================================================ */

/* Find child PIDs using BFS traversal of the pid->ppid mapping.
 * all_pids and ppids must have the same count (parallel arrays).
 * Returns 0 on success, -1 on error. */
static int
find_children_bfs(pid_t target_pid, int recursive,
                  pid_t *all_pids, pid_t *ppids, size_t pid_count,
                  pid_array_t *result)
{
    int retval = -1;
    pid_array_t to_process = {0};

    if (pid_array_init(&to_process) < 0) {
        goto done;
    }
    if (pid_array_append(&to_process, target_pid) < 0) {
        goto done;
    }

    size_t process_idx = 0;
    while (process_idx < to_process.count) {
        pid_t current_pid = to_process.pids[process_idx++];

        for (size_t i = 0; i < pid_count; i++) {
            if (ppids[i] != current_pid) {
                continue;
            }
            pid_t child_pid = all_pids[i];
            if (pid_array_contains(result, child_pid)) {
                continue;
            }
            if (pid_array_append(result, child_pid) < 0) {
                goto done;
            }
            if (recursive && pid_array_append(&to_process, child_pid) < 0) {
                goto done;
            }
        }

        if (!recursive) {
            break;
        }
    }

    retval = 0;

done:
    pid_array_cleanup(&to_process);
    return retval;
}

/* ============================================================================
 * LINUX IMPLEMENTATION
 * ============================================================================ */

#if defined(__linux__)

/* Parse /proc/{pid}/stat to get parent PID */
static pid_t
get_ppid_linux(pid_t pid)
{
    char stat_path[64];
    char buffer[2048];

    snprintf(stat_path, sizeof(stat_path), "/proc/%d/stat", (int)pid);

    int fd = open(stat_path, O_RDONLY);
    if (fd == -1) {
        return -1;
    }

    ssize_t n = read(fd, buffer, sizeof(buffer) - 1);
    close(fd);

    if (n <= 0) {
        return -1;
    }
    buffer[n] = '\0';

    /* Find closing paren of comm field - stat format: pid (comm) state ppid ... */
    char *p = strrchr(buffer, ')');
    if (!p) {
        return -1;
    }

    /* Skip ") " with bounds checking */
    char *end = buffer + n;
    p += 2;
    if (p >= end) {
        return -1;
    }
    if (*p == ' ') {
        p++;
        if (p >= end) {
            return -1;
        }
    }

    /* Parse: state ppid */
    char state;
    int ppid;
    if (sscanf(p, "%c %d", &state, &ppid) != 2) {
        return -1;
    }

    return (pid_t)ppid;
}

static int
get_child_pids_platform(pid_t target_pid, int recursive, pid_array_t *result)
{
    int retval = -1;
    pid_array_t all_pids = {0};
    pid_array_t ppids = {0};
    DIR *proc_dir = NULL;

    if (pid_array_init(&all_pids) < 0) {
        goto done;
    }

    if (pid_array_init(&ppids) < 0) {
        goto done;
    }

    proc_dir = opendir("/proc");
    if (!proc_dir) {
        PyErr_SetFromErrnoWithFilename(PyExc_OSError, "/proc");
        goto done;
    }

    /* Single pass: collect PIDs and their PPIDs together */
    for (;;) {
        errno = 0;
        struct dirent *entry = readdir(proc_dir);
        if (entry == NULL) {
            if (errno != 0) {
                int err = errno;
                _set_debug_oserror_from_errno_with_filename(err, "/proc",
                    "Failed to read process directory '/proc': %s",
                    strerror(err));
                goto done;
            }
            break;
        }
        /* Skip non-numeric entries (also skips . and ..) */
        if (entry->d_name[0] < '1' || entry->d_name[0] > '9') {
            continue;
        }
        char *endptr;
        long pid_long = strtol(entry->d_name, &endptr, 10);
        if (*endptr != '\0' || pid_long <= 0) {
            continue;
        }
        pid_t pid = (pid_t)pid_long;
        pid_t ppid = get_ppid_linux(pid);
        if (ppid < 0) {
            continue;
        }
        if (pid_array_append(&all_pids, pid) < 0 ||
            pid_array_append(&ppids, ppid) < 0) {
            goto done;
        }
    }

    if (closedir(proc_dir) != 0) {
        int err = errno;
        proc_dir = NULL;
        _set_debug_oserror_from_errno_with_filename(err, "/proc",
            "Failed to close process directory '/proc': %s",
            strerror(err));
        goto done;
    }
    proc_dir = NULL;

    if (find_children_bfs(target_pid, recursive,
                          all_pids.pids, ppids.pids, all_pids.count,
                          result) < 0) {
        goto done;
    }

    retval = 0;

done:
    if (proc_dir) {
        closedir(proc_dir);
    }
    pid_array_cleanup(&all_pids);
    pid_array_cleanup(&ppids);
    return retval;
}

#endif /* __linux__ */

/* ============================================================================
 * MACOS IMPLEMENTATION
 * ============================================================================ */

#if defined(__APPLE__) && TARGET_OS_OSX

#include <libproc.h>
#include <sys/proc_info.h>

static int
get_child_pids_platform(pid_t target_pid, int recursive, pid_array_t *result)
{
    int retval = -1;
    pid_t *pid_list = NULL;
    pid_t *ppids = NULL;

    /* Count the live PIDs.  proc_listpids() reports a byte count,
       not an element count. */
    int n_bytes = proc_listpids(PROC_ALL_PIDS, 0, NULL, 0);
    int n_pids = n_bytes / (int)sizeof(pid_t);
    if (n_pids <= 0) {
        PyErr_SetString(PyExc_OSError, "Failed to get process count");
        goto done;
    }

    /* Allocate buffer for PIDs (add some slack for new processes) */
    int buffer_size = n_pids + 64;
    pid_list = (pid_t *)PyMem_Malloc(buffer_size * sizeof(pid_t));
    if (!pid_list) {
        PyErr_NoMemory();
        goto done;
    }

    /* Get actual PIDs */
    int n_written = proc_listpids(PROC_ALL_PIDS, 0, pid_list,
                                  buffer_size * (int)sizeof(pid_t));
    if (n_written <= 0) {
        PyErr_SetString(PyExc_OSError, "Failed to list PIDs");
        goto done;
    }
    /* Convert the reported byte count into a pid_t element count so the
       loop below does not walk past the PIDs the kernel actually wrote. */
    int actual = n_written / (int)sizeof(pid_t);

    /* Build pid -> ppid mapping */
    ppids = (pid_t *)PyMem_Malloc(actual * sizeof(pid_t));
    if (!ppids) {
        PyErr_NoMemory();
        goto done;
    }

    /* Get parent PIDs for each process */
    int valid_count = 0;
    for (int i = 0; i < actual; i++) {
        struct proc_bsdinfo proc_info;
        int ret = proc_pidinfo(pid_list[i], PROC_PIDTBSDINFO, 0,
                              &proc_info, sizeof(proc_info));
        if (ret != sizeof(proc_info)) {
            continue;
        }
        pid_list[valid_count] = pid_list[i];
        ppids[valid_count] = proc_info.pbi_ppid;
        valid_count++;
    }

    if (find_children_bfs(target_pid, recursive,
                          pid_list, ppids, valid_count,
                          result) < 0) {
        goto done;
    }

    retval = 0;

done:
    PyMem_Free(pid_list);
    PyMem_Free(ppids);
    return retval;
}

#endif /* __APPLE__ && TARGET_OS_OSX */

/* ============================================================================
 * WINDOWS IMPLEMENTATION
 * ============================================================================ */

#ifdef MS_WINDOWS

static int
get_child_pids_platform(pid_t target_pid, int recursive, pid_array_t *result)
{
    int retval = -1;
    pid_array_t all_pids = {0};
    pid_array_t ppids = {0};
    HANDLE snapshot = INVALID_HANDLE_VALUE;

    snapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
    if (snapshot == INVALID_HANDLE_VALUE) {
        DWORD error = GetLastError();
        PyErr_SetFromWindowsErr(error);
        goto done;
    }

    if (pid_array_init(&all_pids) < 0) {
        goto done;
    }

    if (pid_array_init(&ppids) < 0) {
        goto done;
    }

    /* Single pass: collect PIDs and PPIDs together */
    PROCESSENTRY32 pe;
    pe.dwSize = sizeof(PROCESSENTRY32);
    if (!Process32First(snapshot, &pe)) {
        DWORD error = GetLastError();
        PyErr_SetFromWindowsErr(error);
        goto done;
    }

    do {
        if (pid_array_append(&all_pids, (pid_t)pe.th32ProcessID) < 0 ||
            pid_array_append(&ppids, (pid_t)pe.th32ParentProcessID) < 0) {
            goto done;
        }
    } while (Process32Next(snapshot, &pe));

    DWORD error = GetLastError();
    if (error != ERROR_NO_MORE_FILES) {
        PyErr_SetFromWindowsErr(error);
        goto done;
    }

    CloseHandle(snapshot);
    snapshot = INVALID_HANDLE_VALUE;

    if (find_children_bfs(target_pid, recursive,
                          all_pids.pids, ppids.pids, all_pids.count,
                          result) < 0) {
        goto done;
    }

    retval = 0;

done:
    if (snapshot != INVALID_HANDLE_VALUE) {
        CloseHandle(snapshot);
    }
    pid_array_cleanup(&all_pids);
    pid_array_cleanup(&ppids);
    return retval;
}

#endif /* MS_WINDOWS */

/* ============================================================================
 * UNSUPPORTED PLATFORM STUB
 * ============================================================================ */

#if !defined(__linux__) && !(defined(__APPLE__) && TARGET_OS_OSX) && !defined(MS_WINDOWS)

static int
get_child_pids_platform(pid_t target_pid, int recursive, pid_array_t *result)
{
    PyErr_SetString(PyExc_NotImplementedError,
                   "Subprocess enumeration not supported on this platform");
    return -1;
}

#endif

/* ============================================================================
 * PUBLIC API
 * ============================================================================ */

static PyObject *
enumerate_child_pids(pid_t target_pid, int recursive)
{
    pid_array_t result;

    if (pid_array_init(&result) < 0) {
        return NULL;
    }

    if (get_child_pids_platform(target_pid, recursive, &result) < 0) {
        pid_array_cleanup(&result);
        return NULL;
    }

    /* Convert to Python list */
    PyObject *list = PyList_New(result.count);
    if (list == NULL) {
        pid_array_cleanup(&result);
        return NULL;
    }

    for (size_t i = 0; i < result.count; i++) {
        PyObject *pid_obj = PyLong_FromLong((long)result.pids[i]);
        if (pid_obj == NULL) {
            Py_DECREF(list);
            pid_array_cleanup(&result);
            return NULL;
        }
        PyList_SET_ITEM(list, i, pid_obj);
    }

    pid_array_cleanup(&result);
    return list;
}

/* ============================================================================
 * MODULE
 * ========================================================================== */

static PyObject *
_remote_debugging_get_gc_stats(PyObject *module, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"pid", "all_interpreters", NULL};
    int pid;
    int all_interpreters = 0;
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "i|$p:get_gc_stats", kwlist,
                                     &pid, &all_interpreters)) {
        return NULL;
    }

    RuntimeOffsets offsets;
    if (init_runtime_offsets(&offsets, pid, /*debug=*/1) < 0) {
        return NULL;
    }

    RemoteDebuggingState *st = RemoteDebugging_GetState(module);
    PyObject *result = do_get_gc_stats(&offsets, all_interpreters,
                                       st->GCStatsInfo_Type);

    cleanup_runtime_offsets(&offsets);
    return result;
}

PyDoc_STRVAR(get_gc_stats__doc__,
"get_gc_stats($module, /, pid, *, all_interpreters=False)\n"
"--\n"
"\n"
"Get garbage collector statistics from an external Python process.\n"
"\n"
"Returns a list of GCStatsInfo records, one per ring slot per generation.\n"
"A slot holds a finished collection only when ts_start < ts_stop.  Skip any\n"
"other slot: never-written slots have both zero, mid-write slots have more.\n"
"\n"
"By default only the main interpreter is returned. Pass all_interpreters=True\n"
"to return every live interpreter. heap_size is 0 on this build.");

static PyObject *
_remote_debugging_get_child_pids(PyObject *module, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"pid", "recursive", NULL};
    int pid;
    int recursive = 1;
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "i|$p:get_child_pids", kwlist,
                                     &pid, &recursive)) {
        return NULL;
    }
    return enumerate_child_pids((pid_t)pid, recursive);
}

PyDoc_STRVAR(get_child_pids__doc__,
"get_child_pids($module, /, pid, *, recursive=True)\n"
"--\n"
"\n"
"Get all child process IDs of the given process.");

static PyMethodDef remote_debugging_methods[] = {
    {"get_gc_stats", _PyCFunction_CAST(_remote_debugging_get_gc_stats),
     METH_VARARGS | METH_KEYWORDS, get_gc_stats__doc__},
    {"get_child_pids", _PyCFunction_CAST(_remote_debugging_get_child_pids),
     METH_VARARGS | METH_KEYWORDS, get_child_pids__doc__},
    {NULL, NULL, 0, NULL},
};

static int
_remote_debugging_exec(PyObject *m)
{
    RemoteDebuggingState *st = RemoteDebugging_GetState(m);
    st->GCStatsInfo_Type = PyStructSequence_NewType(&GCStatsInfo_desc);
    if (st->GCStatsInfo_Type == NULL) {
        return -1;
    }
    if (PyModule_AddType(m, st->GCStatsInfo_Type) < 0) {
        return -1;
    }
    if (PyModule_AddIntConstant(m, "PROCESS_VM_READV_SUPPORTED",
                                HAVE_PROCESS_VM_READV) < 0) {
        return -1;
    }
    return 0;
}

static int
remote_debugging_traverse(PyObject *mod, visitproc visit, void *arg)
{
    RemoteDebuggingState *state = RemoteDebugging_GetState(mod);
    Py_VISIT(state->GCStatsInfo_Type);
    return 0;
}

static int
remote_debugging_clear(PyObject *mod)
{
    RemoteDebuggingState *state = RemoteDebugging_GetState(mod);
    Py_CLEAR(state->GCStatsInfo_Type);
    return 0;
}

static void
remote_debugging_free(void *mod)
{
    (void)remote_debugging_clear((PyObject *)mod);
}

static PyModuleDef_Slot remote_debugging_slots[] = {
    {Py_mod_exec, _remote_debugging_exec},
    {Py_mod_multiple_interpreters, Py_MOD_PER_INTERPRETER_GIL_SUPPORTED},
#ifdef Py_GIL_DISABLED
    /* Without this, importing the module re-enables the GIL in a
       free-threaded build.  It only reads another process's memory and holds
       no shared mutable state of its own. */
    {Py_mod_gil, Py_MOD_GIL_NOT_USED},
#endif
    {0, NULL},
};

static struct PyModuleDef remote_debugging_module = {
    PyModuleDef_HEAD_INIT,
    .m_name = "_remote_debugging",
    .m_size = sizeof(RemoteDebuggingState),
    .m_methods = remote_debugging_methods,
    .m_slots = remote_debugging_slots,
    .m_traverse = remote_debugging_traverse,
    .m_clear = remote_debugging_clear,
    .m_free = remote_debugging_free,
};

PyMODINIT_FUNC
PyInit__remote_debugging(void)
{
    return PyModuleDef_Init(&remote_debugging_module);
}
