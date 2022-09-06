import self
import importlib

from test.lazyimports.data.metasyntactic import foo
self.assertFalse(importlib.is_lazy_import(globals(), "foo"))  # should be eager

importlib.set_lazy_imports()  # enable lazy imports
self.assertTrue(importlib.is_lazy_imports_enabled())

from test.lazyimports.data.metasyntactic import plugh
self.assertTrue(importlib.is_lazy_import(globals(), "plugh"))  # should be lazy

with importlib.eager_imports():
    from test.lazyimports.data.metasyntactic import waldo
self.assertFalse(importlib.is_lazy_import(globals(), "waldo"))  # should be eager
