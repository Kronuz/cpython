"""
Validate the status of imported modules before and after running `importlib.set_lazy_imports`
"""
import self
if not self._lazy_imports:
    self.skipTest("Test relevant only when running with lazy imports enabled")

import importlib

from test.lazyimports.customized_modules import foo

importlib.set_lazy_imports(excluding=["test.lazyimports.immediate_set_lazy_import"])

from test.lazyimports.customized_modules import waldo

self.assertTrue(importlib.is_lazy_import(globals(), "foo"))
self.assertFalse(importlib.is_lazy_import(globals(), "waldo"))
