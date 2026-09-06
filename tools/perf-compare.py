#!/usr/bin/env python3
"""Compare two Python builds on a workload, honestly.

    perf-compare.py <stock-python> <patched-python> [-w WORKLOAD] [-n REPS]

Runs each workload alternately in fresh processes, reports medians and a
percentage difference -- and, crucially, reports a **noise floor** measured by
comparing the stock binary against itself.

The noise floor is the point. Two separately-linked binaries differ by code
layout and alignment alone, worth several percent in either direction, so a
"+3%" result means nothing until you know what 0% looks like on that machine at
that moment. A run whose noise floor is comparable to its signal has measured
nothing.

Exit 0 when every workload's difference is within the noise floor, 1 when any
exceeds it, 2 on error. Treat exit 1 as "look closer", not as "regression":
confirm it on a second, independently built pair before believing it.
"""

from __future__ import annotations

import argparse
import statistics
import subprocess
import sys
from pathlib import Path

# Each workload prints one float: seconds for its own timed section. Keeping
# the timing inside the child avoids charging interpreter startup to the
# measurement, except in the startup workload where startup *is* the subject.
WORKLOADS: dict[str, str] = {
    "alloc": """
import time
t = time.perf_counter()
for _ in range(300):
    x = [bytearray(1024) for _ in range(2000)]
    del x
print(time.perf_counter() - t)
""",
    "dict": """
import time
t = time.perf_counter()
d = {}
for i in range(120000):
    k = "key%d" % i
    d[k] = {"i": i, "s": k * 2, "l": [i, i + 1, i + 2]}
s = sum(v["i"] for v in d.values())
out = sorted(d)[:100]
print(time.perf_counter() - t)
""",
    "regex": r"""
import re, time
p = re.compile(r"(\w+)@(\w+)\.com")
txt = " ".join("user%d@example.com" % i for i in range(2000))
t = time.perf_counter()
for _ in range(60):
    p.findall(txt)
print(time.perf_counter() - t)
""",
    "gc": """
import gc, time
class Node:
    __slots__ = ("next", "prev", "payload")
t = time.perf_counter()
for _ in range(40):
    ns = [Node() for _ in range(20000)]
    for i, n in enumerate(ns):
        n.next = ns[(i + 1) % len(ns)]
        n.prev = ns[i - 1]
        n.payload = str(i)
    del ns
    gc.collect()
print(time.perf_counter() - t)
""",
    "imports": """
import subprocess, sys, time
t = time.perf_counter()
for _ in range(20):
    subprocess.run([sys.executable, "-c",
                    "import json, re, logging, email, decimal, asyncio"],
                   capture_output=True)
print(time.perf_counter() - t)
""",
}


def die(msg: str) -> None:
    print(f"perf-compare: {msg}", file=sys.stderr)
    raise SystemExit(2)


def run_once(binary: str, code: str) -> float:
    r = subprocess.run(
        [binary, "-c", code], capture_output=True, text=True, check=False
    )
    if r.returncode != 0:
        die(f"{binary} failed:\n{r.stderr[-500:]}")
    try:
        return float(r.stdout.strip().splitlines()[-1])
    except (ValueError, IndexError):
        die(f"{binary} printed no timing:\n{r.stdout[-300:]}")
        raise  # unreachable; keeps type checkers happy


def measure(a: str, b: str, code: str, reps: int) -> tuple[float, float, float, float]:
    """Alternate a and b so drift hits both equally. Returns medians and spreads."""
    ta: list[float] = []
    tb: list[float] = []
    for _ in range(reps):
        ta.append(run_once(a, code))
        tb.append(run_once(b, code))
    ma, mb = statistics.median(ta), statistics.median(tb)
    return ma, mb, (max(ta) - min(ta)) / ma * 100, (max(tb) - min(tb)) / mb * 100


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Compare two Python builds with a measured noise floor."
    )
    ap.add_argument("stock")
    ap.add_argument("patched")
    ap.add_argument(
        "-w",
        "--workload",
        action="append",
        choices=sorted(WORKLOADS),
        help="workload to run (repeatable; default: all)",
    )
    ap.add_argument(
        "-n", "--reps", type=int, default=9, help="repetitions per binary (default 9)"
    )
    args = ap.parse_args()

    for p in (args.stock, args.patched):
        if not Path(p).is_file():
            die(f"not a file: {p}")
    if args.reps < 5:
        die("use at least 5 repetitions; fewer cannot separate signal from noise")

    names = args.workload or sorted(WORKLOADS)

    print(f"  stock:   {args.stock}")
    print(f"  patched: {args.patched}")
    print(f"  {args.reps} alternating repetitions per binary, median reported\n")

    print(f"    {'WORKLOAD':<10} {'NOISE FLOOR':>12}  {'MEASURED':>10}   VERDICT")

    worst = 0.0
    exceeded = []
    for name in names:
        code = WORKLOADS[name]
        # Noise floor: the same binary against itself. Anything at or below
        # this is indistinguishable from nothing.
        n_a, n_b, _, _ = measure(args.stock, args.stock, code, args.reps)
        floor = abs(n_b - n_a) / n_a * 100

        m_a, m_b, sa, sb = measure(args.stock, args.patched, code, args.reps)
        delta = (m_b - m_a) / m_a * 100

        verdict = "within noise" if abs(delta) <= max(floor, 1.0) else "EXCEEDS NOISE"
        if verdict != "within noise":
            exceeded.append((name, delta))
        worst = max(worst, abs(delta))

        print(
            f"    {name:<10} {floor:>11.2f}%  {delta:>+9.2f}%   {verdict}"
            f"   (spread {sa:.1f}%/{sb:.1f}%)"
        )

    print()
    if not exceeded:
        print(f"  Every workload within its noise floor (worst {worst:+.2f}%).")
        return 0

    for name, delta in exceeded:
        print(f"  {name}: {delta:+.2f}% exceeds the noise floor.")
    print(
        "\n  Before believing it: rebuild both binaries and re-run. A difference that\n"
        "  does not survive an independent pair of builds was code layout, not the\n"
        "  patch. If it does survive, confirm with pyperformance -- see\n"
        "  PERF-TESTING.md."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
