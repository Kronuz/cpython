# Working in this repository

A personal fork of CPython. The code is on the feature branches; `master` carries
only documentation. If you are an agent sent here to understand or extend the work:
read `README.md` for the branch map, read the relevant `docs/<feature>.md` for the
decisions behind a branch, and use `tools/` to verify any change. This file is how
the repository is meant to be worked in.

## Layout

- `README.md`: the branch map. What each branch is, its base, a one-line why.
- `docs/`: the depth. `docs/methodology.md` is the shared ABI-and-performance
  discipline; the rest are per-feature (`allocated-bytes.md`, `gc-stats.md`,
  `current-loops.md`, `lazy-imports.md`).
- `tools/`: small scripts to check a change. `abi-check.py`, `abi-witness.py`,
  `perf-compare.py`. They depend on nothing outside this repository.
- The branches: the actual patches. Each `<version>-<feature>` branch is a release
  tag plus one commit, so the patch is the diff.

## The constraint that shapes everything: ABI

These patches are meant to drop onto a released CPython and run with **prebuilt
extension wheels installed from PyPI, not rebuilt**. A wheel that uses CPython's
internal headers (Cython-generated code, greenlet, gevent, and a long tail) reads a
struct field as a byte offset baked in at compile time. No symbol, no relocation on
that access.

So if a patch moves a field offset in one of those internal structs, nothing fails
at import, nothing is logged, and the wheel silently reads the wrong bytes. "It
builds and the tests pass" is not evidence that a patch is ABI-safe.

The rule for every patch here: **no field offset may move.** A struct may grow at
its tail (that changes `sizeof` but shifts nothing after the addition); a moved
offset is the one failure this repository is organized to avoid. Prefer keeping new
state out of CPython's structures entirely: `3.14-allocated-bytes` is a worked
example of state that lives at the tail of a private struct so no offset moves.

Verify it, don't reason about it:

```
tools/abi-check.py <stock-tree> <patched-tree>
```

against a pristine tree at the **same commit** with the **same configure flags**,
and again with `--disable-gil` if the patch touches thread state. `docs/methodology.md`
explains why, and `tools/abi-witness.py` shows what a moved offset does to a wheel.

## Verifying a branch

1. The branch is already its release tag plus one commit; the base tag is in
   `README.md`.
2. Build it. On macOS a stock `./configure && make` links; nothing here needs a
   special toolchain.
3. Run the feature's own tests (each feature branch ships them).
4. `tools/abi-check.py` against a stock tree at the same tag: expect IDENTICAL
   offsets. Sizes may grow at the tail; that is fine.
5. If the change could cost time, `tools/perf-compare.py` against a stock build from
   the same commit, and read the noise floor before the result.

## Performance, honestly

Two separately-linked binaries differ in speed before you change a line, by several
percent, from code layout alone. A raw "+3%" is not a result. Measure a noise floor
(the stock binary against itself), alternate the two binaries in fresh processes,
take medians on an idle machine, and confirm anything above the floor with
`pyperformance`. The count of benchmarks that came out faster is your error bar.
`docs/methodology.md` has the full discipline.

## What not to do

- **Don't move a struct field offset.** The one hard rule; see above.
- **Don't rebase or squash the historical branches** (`lazy_imports*`,
  `sys__getallocatedbytes`). Their history is the artifact; rewriting it destroys the
  provenance.
- **Don't trust a fuzzy patch apply.** Apply with zero fuzz (`patch -F0` or
  `git apply`); a fuzzy apply can land a hunk in the wrong place and still look clean.
- **Don't judge a full test run against zero.** CPython's suite has environment-flaky
  tests that fail on a stock build too. Compare against the same stock build, not
  against an expectation of all-green.

## Conventions

- `<version>-<feature>` branches: a release tag plus one commit.
- Upstream issue numbers (`gh-...`) and PEP 810 are the anchors for provenance.
- Each patch carries its own rationale in a header comment; `docs/` is the expanded
  version of those headers.
