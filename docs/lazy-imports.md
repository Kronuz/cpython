# Lazy Imports

Two implementations live in this fork, and the split is the interesting provenance.

## The original (`lazy_imports*`, historical)

The lazy-imports work that predates and motivated the standard: the
`Objects/lazyimportobject.c` implementation, on 3.8, 3.10 and 3.12 bases, plus two
experiment branches (a `lazy_imports` flag on `_PyInterpreterFrame`, and a branch that
committed `pyperformance` results). These are historical working branches, preserved
as they happened. `lazy_imports` is a squashed single-commit share of the 3.12 work;
`lazy_imports_3_12` is the full working branch carried to current 3.12 maintenance.
Same feature code, different base. `README.md` has the table.

## PEP 810 backport (`3.14-lazy-imports`)

The standard itself, PEP 810 (Explicit Lazy Imports), as it landed upstream,
backported to 3.14.

**What.** The full upstream implementation: the `lazy import` grammar and AST, the
`LAZY_IMPORT_NAME` and `LAZY_IMPORT_FROM` opcodes and their specializations, lazy dict
values in `Objects/dictobject.c` and `Objects/moduleobject.c`,
`sys.set_lazy_imports()` and `-X lazy_imports`, plus the docs and tests.

**Why.** Import time dominates startup for larger Python services, and lazy imports
cut it without every service hand-rolling module-level deferral.

**Provenance.** A faithful backport of upstream's PEP 810 (`gh-142349`), first shipped
in 3.15. The feature landed in `GH-142351`, and this carries its follow-ups
(`GH-150126`, `GH-144856`, `GH-154688`), confirmed against the tree by the markers
those commits introduced.

**ABI.** No structure changes; sizes and offsets match a stock build. The lazy state is
heap-allocated behind the existing unused `PyInterpreterState._malloced`, and
`PyConfig.lazy_imports` is omitted, so `-X lazy_imports` and `PYTHON_LAZY_IMPORTS`
still work. That is the local change that keeps the backport ABI-neutral where a naive
port would add a config field and move offsets.

**A backported test carries its fixture.** The upstream suggestion tests depend on a
data package whose `__init__` is a single `lazy from . import bar`. A backport has to
carry that fixture in rather than repoint the tests at a similar-looking existing
package (which silently inverts what they measure), and it has to register any new test
data directory in the build's installed test set, or the test passes in the build tree
and fails on the installed interpreter.

**Remove when.** This line reaches 3.15, which ships PEP 810.

## Upstream parity

Last checked 2026-09-27 against the **3.15 branch tip** `5985fcbb43d1` (90 commits
past the previous check `5e19ff32`; the latest tag is still `v3.15.0rc2`, no rc3 or
final yet). Check the branch, not the tag.

**One core fix needs pulling.** `gh-157757` (`1a2d24e3`, 2026-09-26, make
`lazy import a.b as c` import the module `a.b`) is a behavioral bug fix in the
lazy-import core: it corrects dotted `lazy import ... as` to match the eager
statement, and stops accessing one lazy name from importing the other names'
submodules. It touches `Objects/lazyimportobject.c`, `Python/ceval.c`, and
`Python/import.c`, all carried by this backport, so the 3.14 backport (and the 3.15
scaffold) should pull it.

Outside this patch's file scope, noted but not required: `gh-156924` (`013c4ae5`,
annotationlib reifies lazy imports in `ForwardRef.evaluate()`, `Lib/annotationlib.py`,
a consumer of the lazy API rather than the core) and the docs-only `gh-142349`
(`8bcee873`, document `LazyImportType.resolve()` in `Doc/library/types.rst`). The
previously-noted `GH-155547` and `GH-156624` remain outstanding and non-behavioral.
Next check starts from `5985fcbb43d1`.
