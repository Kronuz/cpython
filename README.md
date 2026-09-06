# CPython, a feature-branch fork

A personal fork of [CPython](https://github.com/python/cpython). Nothing
interesting lives on `master`; it carries only this guide. The work is on the
branches, in three lineages (Lazy Imports, allocation accounting, and
out-of-process runtime monitoring), plus a few historical working branches I
keep as they actually happened.

Two branch styles:

- **Clean single-feature branches.** A release tag plus exactly one commit, so
  the patch is the diff. Named `<version>-<feature>`.
- **Historical branches.** Real work as it happened, thousands of commits and
  rebases and dead ends, preserved as-is. I don't rewrite these.

The `main` branch is the vanilla 3.12 base these historical branches were cut
from (stock CPython 3.12.0+, frozen in 2023). It carries none of the work below.

The per-feature notes (What, Why, ABI, Remove when) come from the rationale each
patch carries in its own header.

## Digging deeper

- **`AGENTS.md`** is the entry point for working here: the ABI rule that shapes
  every patch, how to verify a branch, and what not to do. Start here if you are an
  agent.
- **`docs/methodology.md`** is the ABI and performance testing discipline, and why
  it is the way it is.
- **`docs/`** has a deep dive per feature: `allocated-bytes.md`, `gc-stats.md`,
  `current-loops.md`, `lazy-imports.md`.
- **`tools/`** carries `abi-check.py`, `abi-witness.py` and `perf-compare.py`, so
  you can check a change yourself. They depend on nothing outside this repository.

## Lazy Imports

Two implementations live here, and the split is worth knowing:

- The original lazy-imports work (the `lazy_imports*` branches), the
  implementation that predates and motivated the standard.
- The standard itself, **PEP 810 (Explicit Lazy Imports)**, as it landed
  upstream, backported on
  [`3.14-lazy-imports`](https://github.com/Kronuz/cpython/tree/3.14-lazy-imports).

### Original implementation (historical)

The core (`Objects/lazyimportobject.c`, `Include/lazyimportobject.h`,
`Include/internal/pycore_lazyimport.h`) is byte-identical across the 3.12
branches below. They differ only in the CPython base they sit on.

| Branch | Base | What it is |
| --- | --- | --- |
| [`lazy_imports`](https://github.com/Kronuz/cpython/tree/lazy_imports) | 3.12.0 | A squashed single-commit share of the full feature, one clean commit to read without the thousands-of-commits churn. |
| [`lazy_imports_3_12`](https://github.com/Kronuz/cpython/tree/lazy_imports_3_12) | 3.12.11 | The full working branch (~2358 commits): vanilla 3.12 built up to full lazy imports, kept rebased to current 3.12. Same feature code as `lazy_imports`. |
| [`lazy_imports_3_10`](https://github.com/Kronuz/cpython/tree/lazy_imports_3_10) | 3.10 | Ported to 3.10. |
| [`lazy_imports_3_8`](https://github.com/Kronuz/cpython/tree/lazy_imports_3_8) | 3.8.13 | The earliest port, from before `lazyimportobject.c` existed. |
| [`lazy_imports-frame_flag`](https://github.com/Kronuz/cpython/tree/lazy_imports-frame_flag) | 3.10-era (2022) | An experiment: a `lazy_imports` flag on `_PyInterpreterFrame`, the `PyImport_SetLazyImports` API, `set_lazy_imports(excluding=...)`. |
| [`lazy_imports-pyperformance`](https://github.com/Kronuz/cpython/tree/lazy_imports-pyperformance) | 3.10-era (2022) | The feature plus committed `pyperformance` before and after results. |

`lazy_imports` and `lazy_imports_3_12` are the same feature code on a different
base. The share branch was squashed at 3.12.0; the working branch was carried
forward to 3.12.11. The large tree diff between them is entirely the upstream
3.12.0 to 3.12.11 maintenance delta, not the feature.

### PEP 810 backport (clean single-feature)

[`3.14-lazy-imports`](https://github.com/Kronuz/cpython/tree/3.14-lazy-imports), base v3.14.7.

- **What.** The full upstream implementation: the `lazy import` grammar and AST,
  the `LAZY_IMPORT_NAME` and `LAZY_IMPORT_FROM` opcodes and their
  specializations, lazy dict values in `dictobject.c` and `moduleobject.c`,
  `sys.set_lazy_imports()` and `-X lazy_imports`, plus the docs and tests.
- **Why.** Import time dominates startup for larger Python services, and lazy
  imports cut it without every service hand-rolling module-level deferral.
- **Provenance.** A faithful backport of upstream's PEP 810 (`gh-142349`), first
  shipped in 3.15. The feature landed in `GH-142351`, and this carries its
  follow-ups too (`GH-150126`, `GH-144856`, `GH-154688`).
- **ABI.** No structure changes; sizes and offsets match a stock build. The lazy
  state is heap-allocated behind the existing unused
  `PyInterpreterState._malloced`, and `PyConfig.lazy_imports` is omitted, so
  `-X lazy_imports` and `PYTHON_LAZY_IMPORTS` still work.
- **Remove when.** This line reaches 3.15, which ships PEP 810.

## Allocation accounting (sys)

Python-visible byte accounting for the allocator, in two generations. The second
is a redesign of the first.

### [`sys__getallocatedbytes`](https://github.com/Kronuz/cpython/tree/sys__getallocatedbytes), the original (3.12, historical)

`sys.getallocatedbytes()` backed by one per-interpreter atomic counter
(`raw_allocated_bytes`): an atomic read-modify-write on a single shared counter
on every allocation and free. Simple, but that one contended counter is the cost
the per-thread redesign below exists to avoid. One reader, live bytes.

### [`3.14-allocated-bytes`](https://github.com/Kronuz/cpython/tree/3.14-allocated-bytes), the optimized descendant (v3.14.7, single-feature)

- **What.** Three readers, `getallocatedbytes()` (live),
  `gettotalallocatedbytes()` (cumulative), and `_current_allocated_bytes()`
  (per-thread), backed by per-thread allocated and freed byte counters in the
  private `_PyThreadStateImpl`, each charged once from the pymalloc, mimalloc and
  raw paths in `obmalloc.c`. Blocks aren't counted: once the raw domain is
  charged, a counted block isn't one `getallocatedblocks()`'s walk can see.
- **Threads.** One writer per counter, the owning thread. The exception is the
  no-thread-state accumulator that detached threads share, charged with a relaxed
  fetch-add, because a plain add on a counter with more than one writer loses
  increments. The summed total is a sample, not a snapshot, unsynchronized on
  purpose, exactly as upstream's shared `raw_allocated_blocks` already is.
- **ABI.** No field offset moves. Three struct sizes grow by 16 bytes at the tail
  (`_PyThreadStateImpl` 936 to 952, `PyInterpreterState` 225912 to 225928,
  `_PyRuntimeState` 316056 to 316072 on 3.14.7); a free-threaded build grows only
  `_PyThreadStateImpl`. Nothing shifts.
- **Cost.** Within noise: -0.12% median over ten interleaved benchmark rounds
  against a build identical but for this patch, where the control itself moved
  +0.41%. (An unoptimized build of an earlier line showed a few percent. That
  figure predates this per-thread, single-write version.)
- **Remove when.** CPython grows equivalent counters upstream. Nothing is
  proposed today.

## Runtime-monitoring backports (clean single-feature)

Each is a release tag plus one commit.

### GC statistics: [`3.12-gc-stats`](https://github.com/Kronuz/cpython/tree/3.12-gc-stats), [`3.13-gc-stats`](https://github.com/Kronuz/cpython/tree/3.13-gc-stats), [`3.14-gc-stats`](https://github.com/Kronuz/cpython/tree/3.14-gc-stats)

Bases v3.12.13, v3.13.15, v3.14.7.

- **What.** A preallocated ring of recent collections (generation, start and stop
  timestamps, objects examined and collected, live heap size), `candidates` and
  `duration` keys on `gc.get_stats()`, and a reader to pull the ring out of
  process.
- **Provenance.** A backport of upstream's gcmon work (`gh-146527`, first ships
  in 3.15), tracked through `gh-151646` (the free-threaded `gc.get_stats()`
  lock).
- **ABI.** Identical to a stock build. The ring pointer reuses 3.14's spare slot
  in `_gc_runtime_state` rather than appending, which would move every member
  after it, and the free-threaded lock lands in the struct's trailing padding. No
  member moves, even under a free-threaded build.
- **Remove when.** This line reaches 3.15, which ships gcmon.

### asyncio loops: [`3.14-current-loops`](https://github.com/Kronuz/cpython/tree/3.14-current-loops)

Base v3.14.7.

- **What.** `sys._current_loops()`, a dict mapping each thread id to the asyncio
  loop running on it, read from `_PyThreadStateImpl.asyncio_running_loop` (where
  3.13+ keeps the running loop), with the thread-state walk it needs.
- **Why.** An event-loop monitor has to know which loop each thread runs. Keying
  by thread id, the way `sys._current_frames()` keys its own, lets the two
  snapshots join: one says where a thread is, the other says which loop it
  belongs to.
- **Provenance.** Original to this fork's downstream line.
- **Remove when.** CPython grows a supported way to enumerate running loops.
  Nothing is proposed today.

## Removed branches

I pruned two branches that never carried the feature their name promised, and one
empty predecessor. Recorded here so the deletions have provenance too.

| Branch | Why removed | When |
| --- | --- | --- |
| `lazy_imports_3_13`, `lazy_imports_3_14` | Never carried lazy imports. Stock CPython trees; the only "lazy" content was unrelated upstream code. | 2026-09-06 |
| `getallocatedbytes` | An empty predecessor of `sys__getallocatedbytes`: no byte-counter work ever landed (only stock `raw_allocated_blocks`), and no `sys` reader. Restore point `af6e5fa718`. | 2026-09-06 |

## Conventions

- `<version>-<feature>` branches are a release tag plus one commit.
- The historical `lazy_imports*` and `sys__getallocatedbytes` branches stay
  as-is. Don't rebase or squash them; their history is the point.
- Upstream issue numbers (`gh-...`) and PEP 810 are the public anchors for
  provenance. Nothing here leans on downstream-internal references.
