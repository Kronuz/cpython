import self
import importlib
from test.lazyimports.importlib_apis.customized_modules import module_excluded_sub

self.assertFalse(importlib.is_lazy_import(globals(), "module_excluded_sub"))  # should be eager
