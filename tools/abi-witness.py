#!/usr/bin/env python3
"""Prove what a layout change does to a prebuilt extension.

    abi-witness.py <build-tree> [<run-interpreter> ...]

`abi-check.py` compares headers and tells you a field moved. This shows the
consequence: it compiles a small extension against one tree's headers, then
imports it into other interpreters and prints what it reads. Values that differ
between interpreters are exactly the misreads a PyPI wheel would suffer.

Why this matters more than it sounds: a direct field access compiles to an
offset with no relocation and no symbol. There is nothing to scan for, nothing
fails at import, and the wrong value is simply used. This makes that visible.

The extension reads a type's version tag through internal headers -- the same
thing Cython-generated code and greenlet do -- so the number it prints is a
proxy for every internal-header read in the wild.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SOURCE = r"""
#define Py_BUILD_CORE 1
#include <Python.h>
#include "internal/pycore_interp.h"
#include "internal/pycore_runtime.h"

/* Reached through PyInterpreterState, so the offset of that member is baked in
   at compile time. If the interpreter running this has a different layout, the
   read lands somewhere else entirely -- silently. */
static PyObject *
probe(PyObject *self, PyObject *args)
{
    PyInterpreterState *interp = PyInterpreterState_Get();
    unsigned int tag = 0;

#if PY_VERSION_HEX >= 0x030C0000
    tag = interp->types.next_version_tag;
#endif
    return Py_BuildValue("(kK)", (unsigned long)tag,
                         (unsigned long long)(uintptr_t)interp);
}

static PyMethodDef methods[] = {
    {"probe", probe, METH_NOARGS, "read a field through internal headers"},
    {NULL, NULL, 0, NULL},
};

static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT, "abi_witness", NULL, -1, methods,
};

PyMODINIT_FUNC
PyInit_abi_witness(void)
{
    return PyModule_Create(&moduledef);
}
"""


def die(msg: str) -> None:
    print(f"abi-witness: {msg}", file=sys.stderr)
    raise SystemExit(2)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Show what a prebuilt extension reads on different interpreters."
    )
    ap.add_argument(
        "build_tree", help="configured tree whose headers to compile against"
    )
    ap.add_argument(
        "interpreters",
        nargs="*",
        help="interpreters to import the extension into (default: the build tree's own)",
    )
    args = ap.parse_args()

    tree = Path(args.build_tree).resolve()
    if not (tree / "Include" / "internal").is_dir():
        die(f"{tree} is not a CPython source tree")
    if not (tree / "pyconfig.h").is_file():
        die(f"{tree} is not configured (no pyconfig.h)")

    interps = args.interpreters or [str(tree / "python")]
    for i in interps:
        if not os.access(i, os.X_OK):
            die(f"not executable: {i}")

    cc = os.environ.get("CC") or shutil.which("cc") or shutil.which("gcc")
    if not cc:
        die("no C compiler found; set CC")

    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        src = work / "abi_witness.c"
        src.write_text(SOURCE)
        so = work / "abi_witness.so"

        cmd = [
            cc,
            "-shared",
            "-fPIC",
            f"-I{tree}",
            f"-I{tree / 'Include'}",
            f"-I{tree / 'Include' / 'internal'}",
            str(src),
            "-o",
            str(so),
        ]
        if sys.platform == "darwin":
            cmd[1:1] = ["-bundle", "-undefined", "dynamic_lookup"]
            cmd.remove("-shared")

        r = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if r.returncode != 0:
            die(f"extension failed to build against {tree}\n{r.stderr}")

        print(f"  extension built against: {tree}\n")
        print(f"    {'INTERPRETER':<52} {'READS':>12}")

        seen = {}
        snippet = (
            f"import sys; sys.path.insert(0, {str(work)!r})\n"
            "import abi_witness\n"
            "tag, _ = abi_witness.probe()\n"
            "print(tag)"
        )
        for interp in interps:
            out = subprocess.run(
                [interp, "-c", snippet],
                capture_output=True,
                text=True,
                check=False,
            )
            if out.returncode != 0:
                value = "IMPORT FAILED"
            else:
                value = out.stdout.strip()
            label = interp if len(interp) <= 50 else "..." + interp[-47:]
            print(f"    {label:<52} {value:>12}")
            seen.setdefault(value, []).append(interp)

    if len(seen) > 1:
        print(
            "\n  Different values from one binary: the interpreters disagree about\n"
            "  where that field lives. Nothing raised, nothing logged -- the wrong\n"
            "  number was simply used, which is what a PyPI wheel would do."
        )
        return 1

    print("\n  Every interpreter read the same value: compatible layout.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
