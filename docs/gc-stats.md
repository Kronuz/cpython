# GC statistics (`3.12-gc-stats`, `3.13-gc-stats`, `3.14-gc-stats`)

Out-of-process GC statistics for runtime monitoring. Bases v3.12.13, v3.13.15,
v3.14.7, one commit each.

## What

A preallocated ring of recent collections (generation, start and stop timestamps,
objects examined and collected, live heap size); `candidates` and `duration` keys on
`gc.get_stats()`; and a reader that pulls the ring out of another process, so a
monitor can read a service's GC behavior without running inside it.

## Provenance

A backport of upstream's gcmon work (`gh-146527`, first ships in 3.15), tracked
through `gh-151646`, which adds the free-threaded `gc.get_stats()` lock. Upstream's
remote stack unwinder is not included; stacks are read by a separate out-of-tree
reader.

## ABI: identical to a stock build

The interesting part is that this adds cross-process-readable state and still moves no
offset. The ring pointer reuses a spare slot already present in `_gc_runtime_state`
rather than appending, because appending would move every member after it. Where the
tree keeps upstream's counters array for ABI, the reused field is renamed but not
moved: a member's name is source-only; its offset and size are what the ABI pins. The
free-threaded `gh-151646` lock is appended after the struct's existing mutex, landing
in the trailing padding, so it moves nothing even under `--disable-gil`.
`abi-check.py` reports IDENTICAL, including with `--disable-gil`.

## Two protocol decisions worth knowing

**A zero-duration collection is not an unwritten one.** The ring publishes the stop
timestamp last, and a reader treats `start < stop` as "this slot holds a finished
collection". That breaks the moment a real collection measures as zero, which
happens: on some platforms the performance counter advances in steps larger than a
young-generation collection over an empty heap takes, so a real collection publishes
`stop == start` and the reader discards a good sample as if it were caught
mid-write. Fix it in the writer, which knows the collection finished, by clamping the
stop timestamp to at least `start + 1`. One count below the clock's own resolution
distorts nothing, and duration is recorded separately.

**A published ordering needs a barrier to be true.** The ring's layout sidecar states
that the indexed slot is complete before a reader decodes it. Advancing the index with
a plain store upholds that on x86-64, where stores are not reordered with other
stores, but not on arm64, where the index advance can become visible ahead of the slot
writes and a reader decodes a half-written record. The fix is a release fence before
the index store. On x86-64 that fence compiles to nothing, so verify it in the
generated code on arm64, not in the diff: a release fence is exactly the kind of change
that can compile to a no-op if the header it needs was not actually reachable.

## Remove when

This line reaches 3.15, which ships gcmon.

## Upstream parity

Last fully checked against the 3.15 tip at **v3.15.0rc2** (`435c9e5a`) on
2026-09-06. The gcmon surface (the ring, `get_gc_stats`, the `gc.get_stats()`
keys, and the free-threaded lock at `8b1dbb17540`) has no follow-ups since the
backport point. Three later free-threaded GC fixes (`gh-150411`, `gh-156395`,
`gh-149816`) touch neighboring code but are 3.15/main-only, absent from the 3.12
through 3.14 branches, and reach a 3.15 build through its base rather than through
this patch (`gh-156395` touches `_testcapi` and free-threaded GC, not the gcmon
readers). Next check starts from `435c9e5a`.
