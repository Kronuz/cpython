"""Tests for _remote_debugging.get_gc_stats() and get_child_pids().

Adapted from upstream 3.15's Lib/test/test_gc_stats.py (GH-148071).  The
upstream file drives targets through
test.test_profiling.test_sampling_profiler.helpers and gates itself on
test.support.requires_remote_subprocess_debugging(); neither exists on 3.14,
so the subprocess plumbing here follows the conventions of this branch's
test_external_inspection instead.  The assertions are upstream's.
"""

import contextlib
import os
import subprocess
import sys
import textwrap
import time
import unittest

from test.support import (
    Py_GIL_DISABLED,
    SHORT_TIMEOUT,
    busy_retry,
    requires_gil_enabled,
    requires_subprocess,
)
from test.support import os_helper
from test.support.script_helper import make_script

try:
    import _remote_debugging
except ImportError:
    raise unittest.SkipTest(
        "Test only runs when _remote_debugging is available"
    )


GC_STATS_FIELDS = (
    "gen", "iid", "ts_start", "ts_stop", "collections", "collected",
    "uncollectable", "candidates", "heap_size", "duration")

# The GIL build keeps a ring per generation (11 slots for gen 0, 3 each for
# gens 1 and 2).  The free-threaded build keeps a single slot per generation,
# so it reports one record each.
EXPECTED_RECORD_COUNT = 3 if Py_GIL_DISABLED else 17


def has_local_process_debugging():
    """True when this platform lets us read our own process memory.

    macOS needs root or the com.apple.system-task-ports entitlement even for
    the calling process, so the whole module is skipped there rather than
    reporting spurious failures.
    """
    try:
        _remote_debugging.get_gc_stats(os.getpid(), all_interpreters=False)
    except Exception:
        return False
    return True


def has_remote_process_debugging():
    """True when this platform lets us read *another* process's memory.

    Reading our own task port and reading a child's are different privileges
    on macOS: task_for_pid() on any other pid needs root or the
    com.apple.system-task-ports entitlement, so a plain developer build
    passes has_local_process_debugging() and still cannot attach to a child.
    Linux with ptrace_scope 0 and Windows allow both.
    """
    if not has_local_process_debugging():
        return False
    proc = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(30)"])
    try:
        for _ in busy_retry(SHORT_TIMEOUT, error=False):
            try:
                _remote_debugging.get_gc_stats(proc.pid, all_interpreters=False)
            except PermissionError:
                return False
            except Exception:
                continue
            return True
        return False
    finally:
        proc.terminate()
        proc.wait()


def get_generations(gc_stats):
    return tuple(sorted({s.gen for s in gc_stats}))


def get_interpreter_identifiers(gc_stats):
    return tuple(sorted({s.iid for s in gc_stats}))


def get_last_item(gc_stats, generation, iid):
    item = None
    for s in gc_stats:
        if s.gen == generation and s.iid == iid:
            if item is None or item.ts_start < s.ts_start:
                item = s
    return item


def check_gc_stats_fields(testcase, stats):
    testcase.assertIsInstance(stats, list)
    testcase.assertGreater(len(stats), 0)
    for item in stats:
        testcase.assertIsInstance(item, _remote_debugging.GCStatsInfo)
        testcase.assertEqual(type(item).__match_args__, GC_STATS_FIELDS)
        testcase.assertEqual(len(item), len(GC_STATS_FIELDS))


@unittest.skipUnless(
    has_local_process_debugging(), "requires local process debugging")
class TestGetGCStats(unittest.TestCase):

    def test_fields(self):
        stats = _remote_debugging.get_gc_stats(
            os.getpid(), all_interpreters=False)
        check_gc_stats_fields(self, stats)

    def test_all_generations_reported(self):
        stats = _remote_debugging.get_gc_stats(
            os.getpid(), all_interpreters=False)
        self.assertEqual(get_generations(stats), (0, 1, 2))

    def test_record_count_is_the_whole_ring(self):
        # get_gc_stats() returns every slot, not just the written ones: the
        # caller de-duplicates on `collections`.
        stats = _remote_debugging.get_gc_stats(
            os.getpid(), all_interpreters=False)
        self.assertEqual(len(stats), EXPECTED_RECORD_COUNT)

    def test_main_interpreter_only_by_default(self):
        stats = _remote_debugging.get_gc_stats(
            os.getpid(), all_interpreters=False)
        self.assertEqual(get_interpreter_identifiers(stats), (0,))

    def test_incomplete_slots_are_identifiable(self):
        # A slot that was never written has ts_start == ts_stop == 0, which
        # is how a reader tells it apart from a finished collection.
        stats = _remote_debugging.get_gc_stats(
            os.getpid(), all_interpreters=False)
        for item in stats:
            self.assertLessEqual(item.ts_start, item.ts_stop)

    @requires_gil_enabled("needs a multi-slot ring")
    def test_completed_records_are_ordered_and_cumulative(self):
        import gc
        gc.collect(0)
        gc.collect(0)
        stats = _remote_debugging.get_gc_stats(
            os.getpid(), all_interpreters=False)
        gen0 = sorted(
            (s for s in stats if s.gen == 0 and s.ts_start < s.ts_stop),
            key=lambda s: s.ts_start,
        )
        self.assertGreaterEqual(len(gen0), 2)
        for earlier, later in zip(gen0, gen0[1:]):
            # The counters accumulate, so a later record never goes backwards.
            self.assertLess(earlier.ts_start, later.ts_start)
            self.assertLess(earlier.collections, later.collections)
            self.assertLessEqual(earlier.collected, later.collected)
            self.assertLessEqual(earlier.candidates, later.candidates)
            self.assertLessEqual(earlier.duration, later.duration)

    def test_counters_advance_after_collections(self):
        import gc
        before = _remote_debugging.get_gc_stats(
            os.getpid(), all_interpreters=False)
        for _ in range(20):
            a = {}
            b = {"a": a}
            a["b"] = b
            del a, b
        gc.collect(0)
        after = _remote_debugging.get_gc_stats(
            os.getpid(), all_interpreters=False)

        before_item = get_last_item(before, 0, 0)
        after_item = get_last_item(after, 0, 0)
        self.assertIsNotNone(before_item)
        self.assertIsNotNone(after_item)
        self.assertGreater(after_item.collections, before_item.collections)
        self.assertGreater(after_item.candidates, before_item.candidates)
        self.assertGreater(after_item.duration, before_item.duration)

    def test_heap_size_is_zero_by_design_on_313(self):
        # This patch adds no hooks to object tracking or untracking, so
        # there is no running live-object count to publish; keeping the
        # ring's cost confined to collection boundaries is what makes it
        # unmeasurable. gc.get_stats() does not expose heap_size at all;
        # this asserts the ring field is present and zero rather than
        # absent or garbage.
        stats = _remote_debugging.get_gc_stats(
            os.getpid(), all_interpreters=False)
        item = get_last_item(stats, 0, 0)
        self.assertIsNotNone(item)
        self.assertEqual(item.heap_size, 0)

    def test_bad_pid_raises(self):
        # PID 0 is never a Python process we can inspect.
        with self.assertRaises((RuntimeError, PermissionError, OSError,
                                ValueError)):
            _remote_debugging.get_gc_stats(0, all_interpreters=False)


@unittest.skipUnless(
    has_remote_process_debugging(), "requires remote process debugging")
@requires_subprocess()
class TestGetGCStatsRemote(unittest.TestCase):

    def test_reads_another_process(self):
        with os_helper.temp_dir() as work_dir:
            script = make_script(work_dir, "gcworkload", textwrap.dedent("""
                import time
                class N:
                    def __init__(self):
                        self.ref = None
                while True:
                    for _ in range(500):
                        a, b = N(), N()
                        a.ref = b
                        b.ref = a
                    time.sleep(0.005)
            """))
            proc = subprocess.Popen([sys.executable, script])
            try:
                # A process that has not finished initializing has no
                # interpreter state to walk yet, so get_gc_stats() raises
                # RuntimeError.  That is transient, and a monitor is expected
                # to retry rather than give up; gcmon maps it to a
                # not-yet-pollable status.
                collections = None
                for _ in busy_retry(SHORT_TIMEOUT, error=False):
                    try:
                        stats = _remote_debugging.get_gc_stats(
                            proc.pid, all_interpreters=True)
                    except RuntimeError:
                        continue
                    check_gc_stats_fields(self, stats)
                    done = [s for s in stats
                            if s.gen == 0 and s.ts_start < s.ts_stop]
                    if done:
                        collections = max(s.collections for s in done)
                        break
                self.assertIsNotNone(
                    collections, "target never reported a gen 0 collection")

                # The target keeps allocating, so the counter must advance.
                for _ in busy_retry(SHORT_TIMEOUT, error=False):
                    stats = _remote_debugging.get_gc_stats(
                        proc.pid, all_interpreters=True)
                    done = [s for s in stats
                            if s.gen == 0 and s.ts_start < s.ts_stop]
                    if done and max(s.collections for s in done) > collections:
                        break
                else:
                    self.fail("gen 0 collections never advanced")
            finally:
                proc.terminate()
                proc.wait()

    def test_exited_process_fails_cleanly(self):
        proc = subprocess.Popen([sys.executable, "-c", "pass"])
        proc.wait()
        with self.assertRaises((RuntimeError, PermissionError, OSError)):
            _remote_debugging.get_gc_stats(proc.pid, all_interpreters=True)


@requires_subprocess()
class TestGetChildPids(unittest.TestCase):

    def test_no_children(self):
        pids = _remote_debugging.get_child_pids(os.getpid(), recursive=True)
        self.assertIsInstance(pids, list)

    def test_direct_child_is_reported(self):
        proc = subprocess.Popen(
            [sys.executable, "-c", "import time; time.sleep(30)"])
        try:
            for _ in busy_retry(SHORT_TIMEOUT, error=False):
                pids = _remote_debugging.get_child_pids(
                    os.getpid(), recursive=False)
                if proc.pid in pids:
                    break
            else:
                self.fail(f"child {proc.pid} never appeared in {pids}")
        finally:
            proc.terminate()
            proc.wait()

    def test_recursive_finds_grandchild(self):
        code = textwrap.dedent("""
            import subprocess, sys, time
            p = subprocess.Popen(
                [sys.executable, '-c', 'import time; time.sleep(30)'])
            print(p.pid, flush=True)
            time.sleep(30)
        """)
        proc = subprocess.Popen([sys.executable, "-c", code],
                                stdout=subprocess.PIPE, text=True)
        try:
            grandchild = int(proc.stdout.readline().strip())
            for _ in busy_retry(SHORT_TIMEOUT, error=False):
                pids = _remote_debugging.get_child_pids(
                    os.getpid(), recursive=True)
                if grandchild in pids:
                    break
            else:
                self.fail(f"grandchild {grandchild} not in {pids}")

            shallow = _remote_debugging.get_child_pids(
                os.getpid(), recursive=False)
            self.assertNotIn(grandchild, shallow)
        finally:
            proc.terminate()
            proc.wait()
            with contextlib.suppress(Exception):
                proc.stdout.close()


if __name__ == "__main__":
    unittest.main()
