"""
Validate the status of imported modules before and after the module-loaded-triggered `importlib.set_lazy_imports`
"""
import self
if not self._lazy_imports:
    self.skipTest("Test relevant only when running with lazy imports enabled")

import importlib

from . import set_lazy_imports

set_lazy_imports  # trigger loading of `set_lazy_imports`

from test.test_lazy_imports.data.metasyntactic import foo
from test.test_lazy_imports.data.metasyntactic import waldo

self.assertTrue(importlib.is_lazy_import(globals(), "foo"))
self.assertFalse(importlib.is_lazy_import(globals(), "waldo"))
