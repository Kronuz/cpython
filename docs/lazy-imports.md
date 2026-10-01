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

Last checked 2026-10-01 (3.15 release day) against the **3.15 branch tip**
`021f634ed878` (42 commits past the previous check `5985fcbb43d1`). No `v3.15.0`
final tag is pushed yet; the latest tag is still `v3.15.0rc2`.

**The lazy-import core was substantially refactored on release day, and this
backport predates it.** `gh-142349` / `GH-158282` (`021f634`, 2026-10-01,
"Simplify lazy import resolution", co-authored by Petr Viktorin and Hugo van
Kemenade) lands a shared lazy-import resolver: it rewrites `Objects/lazyimportobject.c`
(+431/-32) and `Python/import.c` (+105/-379), changes the `PyLazyImportObject`
struct layout, changes the `_PyLazyImport_New` signature, adds `_PyLazyImport_Reify`
and `_PyLazyImport_IsResolving`, and regenerates the opcode metadata, bytecodes,
and generated-case files, also touching `Objects/dictobject.c`,
`Objects/moduleobject.c`, `pycore_interp_structs.h`, and `pycore_tstate.h`. It also
adds chained-exception-note behavior for a broken lazy import.

This is **not a clean cherry-pick**: it is a structural rewrite that changes layout
and opcode metadata, so it needs a deliberate re-sync of the 3.14 backport (and the
3.15 scaffold) to the current lazy core, verified with `abi-check.py` because it
moves internal struct members. It **subsumes** the `gh-157757` item flagged last
check: `gh-157757` (`1a2d24e`) is already in the branch below this refactor, which
rewrites the same three core files, so re-syncing to the current core carries both.
Porting it is a decision, not a drop-in, given the scope.

Still outside the patch's file scope (non-blocking): `gh-156924` (annotationlib
consumer), docs-only `gh-142349`/`8bcee873`, and the earlier non-behavioral
`GH-155547` / `GH-156624`. Next check starts from `021f634ed878`.
