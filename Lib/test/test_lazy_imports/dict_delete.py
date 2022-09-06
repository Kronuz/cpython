"""
Test deleting a module from the dict
"""
import self
import sys
import importlib

import test.test_lazy_imports.data.metasyntactic.waldo
test.test_lazy_imports.data.metasyntactic.waldo
import test.test_lazy_imports.data.metasyntactic.waldo.fred

del sys.modules["test.test_lazy_imports.data.metasyntactic.waldo"]

import test.test_lazy_imports.data.metasyntactic.waldo
test.test_lazy_imports.data.metasyntactic.waldo
import test.test_lazy_imports.data.metasyntactic.waldo.fred

self.assertIs(test.test_lazy_imports.data.metasyntactic.waldo, sys.modules["test.test_lazy_imports.data.metasyntactic.waldo"])

if self._lazy_imports:
    self.assertTrue(importlib.is_lazy_import(test.test_lazy_imports.data.metasyntactic.waldo.__dict__, "fred"))
else:
    self.assertNotIn("fred", dir(test.test_lazy_imports.data.metasyntactic.waldo))
