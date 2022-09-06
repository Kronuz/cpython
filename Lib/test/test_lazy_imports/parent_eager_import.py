import self
if not self._lazy_imports:
    self.skipTest("Test relevant only when running with lazy imports enabled")

import importlib

importlib.set_lazy_imports(eager=["test.test_lazy_imports.data.metasyntactic.foo.bar.baz"])

import test.test_lazy_imports.data.metasyntactic.foo.bar as bar
import test.test_lazy_imports.data.metasyntactic.foo.bar.baz as baz

self.assertTrue(importlib.is_lazy_import(globals(), "bar"))
self.assertFalse(importlib.is_lazy_import(globals(), "baz"))
self.assertFalse(importlib.is_lazy_import(bar.__dict__, "baz"))
