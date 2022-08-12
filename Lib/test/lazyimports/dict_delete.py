"""
Test deleting a module from the dict
"""
import self
import sys
import importlib

import test.lazyimports.customized_modules.module_delete
test.lazyimports.customized_modules.module_delete
import test.lazyimports.customized_modules.module_delete.module_delete_sub

del sys.modules["test.lazyimports.customized_modules.module_delete"]

import test.lazyimports.customized_modules.module_delete
test.lazyimports.customized_modules.module_delete
import test.lazyimports.customized_modules.module_delete.module_delete_sub

self.assertIs(test.lazyimports.customized_modules.module_delete, sys.modules["test.lazyimports.customized_modules.module_delete"])

if self._lazy_imports:
    self.assertTrue(importlib.is_lazy_import(test.lazyimports.customized_modules.module_delete.__dict__, "module_delete_sub"))
else:
    self.assertNotIn("module_delete_sub", dir(test.lazyimports.customized_modules.module_delete))
