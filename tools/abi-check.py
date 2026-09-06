#!/usr/bin/env python3
"""Compare the C-level structure layout of two CPython source trees.

    abi-check.py <stock-tree> <patched-tree>

Exit 0 when the layouts are identical, so an extension compiled against one
works on the other. Exit 1 naming every field that moved. Exit 2 on a usage or
build error.

Neither tree needs to be built -- only configured, because this reads headers.

Why this is generated rather than a fixed probe: CPython moves fields between
versions, so a hardcoded list compiles on 3.14 and fails on 3.12. Every
candidate below is feature-tested against both trees with a trial compile, and
only fields present in both are measured. A field that exists in one tree and
not the other is reported separately rather than silently counted as a
difference.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# Public ABI. Movement here breaks every extension ever compiled, including
# ones using only the limited API.
PUBLIC_SIZES = [
    "PyObject",
    "PyVarObject",
    "PyTypeObject",
    "PyThreadState",
    "PyASCIIObject",
    "PyCompactUnicodeObject",
]

# Internal, reached directly by anything built with Py_BUILD_CORE: Cython
# output, greenlet, gevent, and CPython's own extension modules.
INTERNAL_SIZES = [
    "_PyRuntimeState",
    "PyInterpreterState",
    "_PyThreadStateImpl",
    "_PyGC_Head",
    "PyGC_Head",
]

# Members whose offsets shift when anything is inserted ahead of them. These
# are what a monitoring, allocator, or GC patch tends to disturb.
OFFSETS = [
    ("PyInterpreterState", "ceval"),
    ("PyInterpreterState", "gc"),
    ("PyInterpreterState", "imports"),
    ("PyInterpreterState", "sysdict"),
    ("PyInterpreterState", "builtins"),
    ("PyInterpreterState", "obmalloc"),
    ("PyInterpreterState", "threads"),
    ("PyInterpreterState", "types"),
    ("PyInterpreterState", "dtoa"),
    ("PyInterpreterState", "monitoring_callables"),
    # Tail members, after the embedded _initial_thread. Everything above sits
    # ahead of it and cannot move when a patch grows the thread state, so
    # these are the only PyInterpreterState offsets a counters-in-tstate patch
    # can actually disturb. 3.13 is the version where it does: _initial_thread
    # is last on 3.12 and 3.14, but not there. Absent members are feature
    # tested away, so listing them costs nothing on the versions without them.
    ("PyInterpreterState", "_interactive_src_count"),
    ("PyInterpreterState", "threads_preallocated"),
    ("_PyRuntimeState", "gilstate"),
    ("_PyRuntimeState", "interpreters"),
    ("_PyRuntimeState", "_finalizing"),
    ("_PyRuntimeState", "debug_offsets"),
    ("_PyThreadStateImpl", "refcount"),
    ("_PyThreadStateImpl", "types"),
    ("PyThreadState", "interp"),
    ("PyThreadState", "current_frame"),
    ("PyThreadState", "thread_id"),
    ("PyThreadState", "native_thread_id"),
    ("PyThreadState", "py_recursion_remaining"),
    ("PyThreadState", "exc_info"),
    ("PyThreadState", "asyncio_running_loop"),
    ("PyTypeObject", "tp_basicsize"),
    ("PyTypeObject", "tp_dealloc"),
    ("PyTypeObject", "tp_getattro"),
    ("PyTypeObject", "tp_version_tag"),
]

PRELUDE = """#define Py_BUILD_CORE 1
#include <Python.h>
#include <stddef.h>
#include <stdio.h>
#include "internal/pycore_interp.h"
#include "internal/pycore_runtime.h"
#include "internal/pycore_gc.h"
#if PY_VERSION_HEX >= 0x030D0000
#  include "internal/pycore_tstate.h"
#endif
"""


class Tree:
    """A configured CPython source tree."""

    def __init__(self, path: str, label: str, cc: str) -> None:
        self.path = Path(path).resolve()
        self.label = label
        self.cc = cc

        if not self.path.is_dir():
            die(f"no such tree: {self.path}")
        if not (self.path / "Include" / "internal").is_dir():
            die(f"{self.path} has no Include/internal; not a CPython source tree")
        if not (self.path / "pyconfig.h").is_file():
            die(f"{self.path} is not configured (no pyconfig.h): run ./configure in it")

    @property
    def includes(self) -> list[str]:
        # The tree's own pyconfig.h must win, so its root comes first.
        return [
            f"-I{self.path}",
            f"-I{self.path / 'Include'}",
            f"-I{self.path / 'Include' / 'internal'}",
        ]

    def compiles(self, body: str, workdir: Path) -> bool:
        src = workdir / "probe_test.c"
        src.write_text(PRELUDE + "\nint main(void) {\n" + body + "\n    return 0;\n}\n")
        r = subprocess.run(
            [self.cc, *self.includes, "-fsyntax-only", str(src)],
            capture_output=True,
            text=True,
            check=False,
        )
        return r.returncode == 0

    def run_probe(self, source: str, workdir: Path) -> str:
        src = workdir / f"probe_{self.label}.c"
        exe = workdir / f"probe_{self.label}"
        src.write_text(source)
        r = subprocess.run(
            [self.cc, *self.includes, "-o", str(exe), str(src)],
            capture_output=True,
            text=True,
            check=False,
        )
        if r.returncode != 0:
            die(f"probe failed to compile against {self.path}\n{r.stderr}")
        out = subprocess.run([str(exe)], capture_output=True, text=True, check=False)
        if out.returncode != 0:
            die(f"probe crashed for {self.path}")
        return out.stdout

    def version(self, workdir: Path) -> str:
        src = workdir / "ver.c"
        exe = workdir / "ver"
        src.write_text(
            PRELUDE + '\nint main(void) { printf("%s\\n", PY_VERSION); return 0; }\n'
        )
        r = subprocess.run(
            [self.cc, *self.includes, "-o", str(exe), str(src)],
            capture_output=True,
            text=True,
            check=False,
        )
        if r.returncode != 0:
            return "unknown"
        return subprocess.run(
            [str(exe)], capture_output=True, text=True, check=False
        ).stdout.strip()


def die(msg: str) -> None:
    print(f"abi-check: {msg}", file=sys.stderr)
    raise SystemExit(2)


def probe_source(sizes: list[str], offsets: list[tuple[str, str]]) -> str:
    lines = [PRELUDE, "\nint main(void)\n{"]
    for t in sizes:
        lines.append(f'    printf("sizeof  %-38s %zu\\n", "{t}", sizeof({t}));')
    for struct, member in offsets:
        lines.append(
            f'    printf("offset  %-38s %zu\\n", "{struct}.{member}", '
            f"(size_t)offsetof({struct}, {member}));"
        )
    lines.append("    return 0;\n}")
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Compare the C structure layout of two CPython source trees.",
        epilog="Exit 0 identical, 1 differs, 2 error.",
    )
    ap.add_argument("stock", help="reference tree (configured, unpatched)")
    ap.add_argument("patched", help="tree to check against it")
    ap.add_argument(
        "-v", "--verbose", action="store_true", help="list every field compared"
    )
    args = ap.parse_args()

    cc = os.environ.get("CC") or shutil.which("cc") or shutil.which("gcc")
    if not cc:
        die("no C compiler found; set CC")

    stock = Tree(args.stock, "stock", cc)
    patched = Tree(args.patched, "patched", cc)

    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)

        sv, pv = stock.version(work), patched.version(work)
        if sv != pv and "unknown" not in (sv, pv):
            print(
                f"abi-check: warning: comparing Python {sv} against {pv}. "
                "A layout difference between versions is expected and says nothing "
                "about a patch; compare a patched tree against a pristine one of "
                "the same commit.",
                file=sys.stderr,
            )

        # Feature-test every candidate against both trees, so the tool works on
        # any version without a per-version field list.
        sizes, offsets, skipped = [], [], []
        for t in PUBLIC_SIZES + INTERNAL_SIZES:
            body = f"    (void)sizeof({t});"
            in_s, in_p = stock.compiles(body, work), patched.compiles(body, work)
            if in_s and in_p:
                sizes.append(t)
            elif in_s != in_p:
                skipped.append(
                    (t, "present only in " + ("stock" if in_s else "patched"))
                )
        for struct, member in offsets_candidates(sizes):
            body = f"    (void)offsetof({struct}, {member});"
            in_s, in_p = stock.compiles(body, work), patched.compiles(body, work)
            if in_s and in_p:
                offsets.append((struct, member))
            elif in_s != in_p:
                skipped.append(
                    (
                        f"{struct}.{member}",
                        "present only in " + ("stock" if in_s else "patched"),
                    )
                )

        if not sizes and not offsets:
            die("no probe fields compiled against either tree; are both configured?")

        src = probe_source(sizes, offsets)
        out_s = stock.run_probe(src, work).splitlines()
        out_p = patched.run_probe(src, work).splitlines()

    moved = [(s, p) for s, p in zip(out_s, out_p) if s != p]
    total = len(out_s)

    print(f"  stock:   {stock.path}  (Python {sv})")
    print(f"  patched: {patched.path}  (Python {pv})")

    if args.verbose:
        print()
        for line in out_s:
            print(f"    {line}")

    if skipped:
        print("\n  fields present in only one tree (not compared):")
        for name, why in skipped:
            print(f"    {name:40s} {why}")

    if not moved:
        print(f"\nABI IDENTICAL  ({total} fields compared)")
        return 0

    print(f"\nABI DIFFERS  ({len(moved)} of {total} fields moved)\n")
    print(f"    {'FIELD':<40} {'STOCK':>10}  {'PATCHED':>10}")
    for s, p in moved:
        _kind, field, sval = s.split(None, 2)
        pval = p.split(None, 2)[2]
        print(f"    {field:<40} {sval:>10}  {pval:>10}")
    print(
        "\n  An extension compiled against one of these misreads the other, and a\n"
        "  direct field access carries no symbol, so nothing can detect it at\n"
        "  import time or repair it afterwards."
    )
    return 1


def offsets_candidates(available_sizes: list[str]) -> list[tuple[str, str]]:
    """Only probe offsets in structs that exist, to keep the trial compiles cheap."""
    return [(s, m) for s, m in OFFSETS if s in available_sizes or s == "PyTypeObject"]


if __name__ == "__main__":
    sys.exit(main())
