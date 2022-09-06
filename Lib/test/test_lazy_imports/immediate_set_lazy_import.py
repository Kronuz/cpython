"""
Validate the status of imported modules before and after running `importlib.set_lazy_imports`
"""
import self
if not self._lazy_imports:
    self.skipTest("Test relevant only when running with lazy imports enabled")

import importlib

from test.test_lazy_imports.data.metasyntactic import foo

importlib.set_lazy_imports(eager=["test.test_lazy_imports.data.metasyntactic.plugh"])

from test.test_lazy_imports.data.metasyntactic import plugh

self.assertTrue(importlib.is_lazy_import(globals(), "foo"))
self.assertFalse(importlib.is_lazy_import(globals(), "plugh"))
