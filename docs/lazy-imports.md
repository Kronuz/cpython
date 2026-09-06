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

Last checked 2026-09-06 against the **3.15 branch tip** `5e19ff32` (ahead of the
`v3.15.0rc2` tag `435c9e5a`). Check the branch, not the tag: new work lands
between tags, so the tag alone misses in-flight commits. The feature core
(`Objects/lazyimportobject.c`, `Include/internal/pycore_lazyimportobject.h`) is
unchanged on the 3.15 branch and main since the backport point `57dface7588a`
(2026-08-19). Two later 3.15 commits are outstanding, both non-behavioral and
3.15-only: `GH-155547` (`0ca288a8`, clarify that `sys.lazy_modules` may contain
extra items, `Doc/library/sys.rst`, 2026-09-04) and `GH-156624` (enable linting
of the lazy-import tests, 2026-08-30). Next check starts from `5e19ff32`.
