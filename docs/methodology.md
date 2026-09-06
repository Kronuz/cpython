# ABI and performance methodology

Two checks gate every patch here: it must not move a C struct field offset, and it
must not cost measurable time. Both are easy to get wrong by reasoning instead of
measuring, so both have a tool and a discipline.

## ABI: why a moved offset is silent and dangerous

The patches are meant to run with prebuilt extension wheels installed from PyPI and
never rebuilt. An extension that uses CPython's internal headers reads a struct
field as a byte offset fixed at compile time. There is no symbol and no relocation
on that access. So if the interpreter's layout differs from the one the wheel was
compiled against:

- nothing fails at import,
- nothing appears in a log,
- no tool can scan a wheel and find the mismatch,
- the wrong bytes are simply used, and the value is not even stable between runs (it
  can land in part of a pointer).

Insert one field into `PyInterpreterState` and everything after it moves; every
prebuilt wheel that reads any of those fields starts returning garbage. Extensions
that use only the public or limited API are unaffected; the exposure is to
internal-header users, and you cannot enumerate which wheels those are.

CPython's own stable-ABI test does not cover this: `PyInterpreterState` is declared
`opaque` in `Misc/stable_abi.toml`, so its layout is deliberately unchecked. Grepping
the patch does not work either: a patch can name a struct all over and change no
layout, or move a layout with one innocuous line. Measure, don't read.

### The check

```
tools/abi-check.py <stock-tree> <patched-tree>
```

Compiles the same generated probe against both trees' headers and diffs sizes and
offsets. Exit 0 identical, 1 differs (naming each moved field), 2 error. Neither tree
needs to be built, only configured, because it reads headers, so it is fast enough to
run on every revision.

Getting it right:

- **Compare against a pristine tree at the same commit**, not "3.14 from somewhere".
  A layout difference between two versions is expected and proves nothing.
  `git worktree add --detach <dir> <the-commit>`.
- **Same configure flags on both.** `--with-pydebug`, `--disable-gil` and
  `--with-trace-refs` each change layout on their own.
- **Check the free-threaded build separately** if the patch touches thread state.
  `Py_GIL_DISABLED` selects different members, so a patch can be clean on one build
  and not the other.

A changed size is not a moved offset. The tool exits non-zero for both, so read the
report: a struct that grew at its tail moved nothing and is safe for a prebuilt
wheel; a moved offset is the failure.

### The consequence, when you need to show it

```
tools/abi-witness.py <build-tree> <interpreter> [<interpreter> ...]
```

compiles a small extension against one tree's headers and imports it into each
interpreter, printing what it reads. One binary, several interpreters, disagreeing
answers: that is the misread a wheel would suffer, made visible.

## Performance: why a raw percentage is not a result

Two separately-linked binaries differ in speed before you change a line. Code layout,
function alignment and instruction-cache placement are worth several percent in
either direction and have nothing to do with the patch. Measured across 97
`pyperformance` benchmarks, a pure counter-adding patch (which can only add work)
showed 46 slower, 50 faster, geometric mean 1.00x. The 50 faster results are the size
of the noise, and they say exactly how much to discount the 46 slower ones.

The discipline:

1. **Measure the noise floor every time.** Compare the stock binary against itself,
   same run, same machine, same moment. A signal at or below that floor is not a
   signal. `tools/perf-compare.py` does this automatically and prints the floor next
   to the result; a healthy floor is well under 1%.
2. **Alternate the binaries in fresh processes.** Stock, patched, stock, patched, not
   all of one then the other, so drift spreads across both sides. Fresh process per
   repetition, take the median, at least seven repetitions.
3. **An idle machine, or no measurement.** A run alongside a build reported a 6-14%
   floor with 66-105% spread; every number from it was garbage that looked like a
   regression. Read the floor first; if it is high, stop and re-run later.
4. **pyperformance decides.** `perf-compare.py` is the fast loop while iterating.
   Before claiming neutrality, run the real suite and read the geometric mean, the
   per-tag groups (a group all moving one way is real; one benchmark alone is noise),
   and the faster count as the error bar.
5. **Report a unit that transfers.** A percentage on one workload does not transfer to
   a service with a different shape. Prefer cost per operation plus the operation's
   rate. For allocation counters the transferable pair was cost per allocator call and
   calls per second, not bytes: a float-heavy loop pays because floats are small and
   the call rate is what is charged. Be willing to conclude "below the machine's noise
   floor" rather than report a confident wrong number.
6. **Measure memory at the shapes you care about** (bare, after realistic imports,
   under thread load), on an idle machine, median of several runs. A static
   reservation is not resident memory: a 256 KB BSS table measured 0 kB RSS on a bare
   interpreter because BSS faults lazily and many slots share a page.
7. **One machine is one data point.** Confirm anything above the floor on a second,
   independently built pair before believing it.
