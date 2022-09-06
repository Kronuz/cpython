import self

if not self._lazy_imports:
    self.skipTest("Test relevant only when running with global lazy imports enabled")

import importlib

import test.test_lazy_imports.data.metasyntactic as metasyntactic

metasyntactic  # force loading

from test.test_lazy_imports.data.metasyntactic import foo

self.assertTrue(importlib.is_lazy_import(globals(), "foo"))  # should be lazy
