import self
if self._lazy_imports:
    self.skipTest("Test relevant only when running with global lazy imports disabled")

import importlib
from contextlib import contextmanager


from test.test_lazy_imports.data.metasyntactic import foo
self.assertFalse(importlib.is_lazy_import(globals(), "foo"))  # should be eager


importlib.set_lazy_imports()  # enable lazy imports
self.assertTrue(importlib.is_lazy_imports_enabled())


from test.test_lazy_imports.data.metasyntactic import plugh
self.assertTrue(importlib.is_lazy_import(globals(), "plugh"))  # should be lazy


try:
    from test.test_lazy_imports.data.metasyntactic import waldo
finally:
    pass
self.assertFalse(importlib.is_lazy_import(globals(), "waldo"))  # should be eager


@contextmanager
def eager_imports():
    yield

with eager_imports():
    from test.test_lazy_imports.data.metasyntactic.foo import bar
self.assertFalse(importlib.is_lazy_import(globals(), "bar"))  # should be eager
