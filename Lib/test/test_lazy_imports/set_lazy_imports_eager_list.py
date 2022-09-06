import self
if self._lazy_imports:
    self.skipTest("Test relevant only when running with global lazy imports disabled")

import importlib

importlib.set_lazy_imports(eager=["test.test_lazy_imports.data.metasyntactic.foo.bar.Bar"])

from test.test_lazy_imports.data.metasyntactic.foo import Foo
self.assertTrue(importlib.is_lazy_import(globals(), "Foo"))  # should be lazy

import test.test_lazy_imports.data.metasyntactic.foo.bar as bar
self.assertTrue(importlib.is_lazy_import(globals(), "bar"))  # should be lazy

from test.test_lazy_imports.data.metasyntactic.foo.bar import Bar
self.assertFalse(importlib.is_lazy_import(globals(), "Bar"))  # should be loaded because full path to Bar is eager

self.assertEqual(Foo, "Foo")  # force load
self.assertFalse(importlib.is_lazy_import(globals(), "Foo"))  # should be loaded now
