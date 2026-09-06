# Allocation accounting (`3.14-allocated-bytes`)

Python-visible byte accounting for the allocator: `sys.getallocatedbytes()` (live
bytes), `sys.gettotalallocatedbytes()` (cumulative), and
`sys._current_allocated_bytes()` (per-thread). Base v3.14.7, one commit.

## Why

CPython cannot report live bytes at all. `sys.getallocatedblocks()` counts blocks
rather than bytes, and walks every arena and pool to do it. `tracemalloc` can
attribute allocation but charges a traceback on every alloc and free, which is not
affordable on a service already in trouble. These readers are O(1) counters read off
the running interpreter.

## The counters

Per-thread `alloc_bytes` and `freed_bytes` in the private `_PyThreadStateImpl`,
charged once from the pymalloc, mimalloc and raw paths in `Objects/obmalloc.c`. Live
bytes is the difference; total is the running sum of `alloc_bytes`.

**Scope.** Bytes, in both the object and the raw domain, each charged exactly once.
The charge sits in `_PyMem_Raw{Malloc,Calloc,Realloc,Free}` rather than in
`_PyObject_Malloc()`'s raw fallback, because that fallback calls the public
`PyMem_RawMalloc()` and hooking both would count it twice. So a direct
`PyMem_RawMalloc()` (startup, config, thread bootstrap, an extension) is counted too.
Still outside: a custom raw allocator installed with `PyMem_SetAllocator()`, and
memory a C library takes straight from `malloc()`, so this is not process RSS.
pymalloc and mimalloc arenas come from `mmap()` rather than the raw domain, so arena
bytes are never counted alongside the objects carved from them.

**Blocks are not counted.** Once the raw domain is charged, a counted block is not one
`getallocatedblocks()`'s walk can see, so a walk-free stand-in for it could not agree
with it. An earlier version shipped a `getallocatedblocksfast()` reader; it was
removed for exactly this reason, which also took the hot path from two adds to one.

## The one shared counter, and its race

One writer per counter, the owning thread, so no per-thread update is ever lost. The
exception is the no-thread-state accumulator that detached threads share:
`PyMem_RawMalloc()` is legal without a thread state, so every detached thread charges
the same static. That one is charged with a relaxed atomic fetch-add, because a plain
`+=` on a counter with more than one writer loses increments outright. Measured under
contention, a plain add lost the large majority of its increments while a relaxed
fetch-add lost none.

The reader, `_PyAlloc_sum()`, walks the live thread states while their owners keep
allocating, so the total is a **sample, not a snapshot**. That is deliberate and
matches upstream, whose shared `raw_allocated_blocks` is also unsynchronized. On a
naturally aligned platform nothing tears, so the exposure is staleness, not
corruption, and stopping every thread for a true snapshot would buy a reader nothing
it could act on.

## ABI

No field offset moves. The counters go last in `_PyThreadStateImpl`, and 3.14 keeps
`_initial_thread` last in `PyInterpreterState` and `_main_interpreter` last in
`_PyRuntimeState`, so three sizes grow by 16 bytes at the tail and nothing shifts:
`_PyThreadStateImpl` 936 to 952, `PyInterpreterState` 225912 to 225928,
`_PyRuntimeState` 316056 to 316072 on 3.14.7. A free-threaded build selects a
different shape and grows only `_PyThreadStateImpl`; it moves nothing either.
`abi-check.py` reports those grown sizes and exits non-zero, which is expected here.
The offsets it lists, the part a prebuilt wheel depends on, are unchanged.

3.13 is not this shape: there `_initial_thread` sits mid-struct and two members would
move, so the same idea needs a different placement on that version. This is exactly
the kind of thing to re-check with `abi-check.py` on every version and after every
base bump.

## Cost

Within noise: -0.12% median over ten interleaved benchmark rounds against a build
identical but for this patch, where the control itself moved +0.41%. Measured with
`tools/perf-compare.py` and confirmed with `pyperformance`. The transferable unit is
cost per allocator call times allocations per second, not bytes per second. An
earlier, unoptimized line of this work showed a few percent on an unoptimized build;
this per-thread, single-write version does not.

## Forward-port

Every pymalloc function this hooks is structurally unchanged on recent CPython main,
so those hunks regenerate by line offset. The one exception is `_PyObject_MiRealloc`,
which gained an in-place-growth fast path: that hunk needs regenerating against the
new body, and no charge belongs in the early return, which neither allocates nor
frees.

## Remove when

CPython grows equivalent counters upstream. Nothing is proposed today, so expect to
carry it across bumps.
