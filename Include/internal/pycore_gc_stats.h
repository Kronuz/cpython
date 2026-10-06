#ifndef Py_INTERNAL_GC_STATS_H
#define Py_INTERNAL_GC_STATS_H
#ifdef __cplusplus
extern "C" {
#endif

#ifndef Py_BUILD_CORE
#  error "this header requires Py_BUILD_CORE define"
#endif

#include <stdint.h>

/* Out-of-process discovery anchor for the GC statistics rings.
 *
 * The rings themselves live at the tail of PyInterpreterState (see struct
 * gc_stats in pycore_gc.h), mirroring upstream 3.15's gcmon.  Upstream and the
 * 3.13/3.14 backports let an external reader reach them through
 * _Py_DebugOffsets, published at the front of _PyRuntime.  3.12 has neither
 * _Py_DebugOffsets nor a cookie'd _PyRuntime section, and adding
 * _Py_DebugOffsets to the front of _PyRuntimeState would move
 * gilstate/interpreters/_finalizing and break the ABI this patch is required
 * to preserve.
 *
 * So this branch publishes one self-describing anchor in its own section
 * instead: a cookie and version, the &_PyRuntime address, and the handful of
 * field offsets a reader needs to walk the interpreter list and find each
 * interpreter's ring.  A new global in its own section changes no struct
 * layout, so it is ABI-safe.  This is the single place the 3.12 backport
 * deviates from the 3.13 reader design; everything a consumer sees (the ring
 * shape and the GCStatsInfo record) is identical.
 */

/* Bumped if the anchor changes shape.  Distinct from the 1/2 the retired
   section-registry design used, so a stale reader rejects this format rather
   than misreading it. */
#define _Py_GCStats_VERSION 3

/* Found by scanning the target's mappings for a section with this name, then
   validating this cookie at its start.  Mirrors how _PyRuntime is located on
   3.14+. */
#define _Py_GCStats_SECTION "gcmonstat"
#define _Py_GCStats_COOKIE "gcmonstat\0\0\0\0\0\0"

/* Self-describing: a reader validates cookie and version, then trusts these
   fields rather than its own headers.  runtime is (uintptr_t)&_PyRuntime; the
   offsets are offsetof() into _PyRuntimeState and PyInterpreterState, so the
   reader can walk the live interpreter list and read each ring without any
   layout knowledge of its own. */
struct _Py_GCStatsAnchor {
    char cookie[16];
    uint64_t version;
    uint64_t flags;                /* bit0 = free-threaded; always 0 on 3.12 */
    uint64_t gc_stats_size;        /* sizeof(struct gc_stats) */
    uint64_t young_slots;          /* GC_YOUNG_STATS_SIZE */
    uint64_t old_slots;            /* GC_OLD_STATS_SIZE */
    uint64_t interpreters_head;    /* offsetof(_PyRuntimeState, interpreters.head) */
    uint64_t interpreter_id;       /* offsetof(PyInterpreterState, id) */
    uint64_t interpreter_next;     /* offsetof(PyInterpreterState, next) */
    uint64_t generation_stats;     /* offsetof(PyInterpreterState, generation_stats) */
    void *runtime;                 /* &_PyRuntime */
};

PyAPI_DATA(struct _Py_GCStatsAnchor) _Py_gc_stats_anchor;

#ifdef __cplusplus
}
#endif
#endif /* !Py_INTERNAL_GC_STATS_H */
