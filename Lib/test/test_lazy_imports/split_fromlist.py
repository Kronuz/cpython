"""
Test the behavior when using the syntax `from xxx import ooo`
"""
import self
import sys

from test.test_lazy_imports.data.metasyntactic import foo, waldo

foo  # trigger loading of `foo`

self.assertIn("test.test_lazy_imports.data.metasyntactic.foo", set(sys.modules))

if self._lazy_imports:
    self.assertNotIn("test.test_lazy_imports.data.metasyntactic.waldo", set(sys.modules))
else:
    self.assertIn("test.test_lazy_imports.data.metasyntactic.waldo", set(sys.modules))
