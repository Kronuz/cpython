"""
Test the behavior when using the syntax `from xxx import ooo`
"""
import self
import sys
import importlib
from test.lazyimports.customized_modules import foo, waldo

foo  # trigger loading of `foo`

self.assertIn("test.lazyimports.customized_modules.foo", set(sys.modules))

if self._lazy_imports:
    self.assertNotIn("test.lazyimports.customized_modules.waldo", set(sys.modules))
else:
    self.assertIn("test.lazyimports.customized_modules.waldo", set(sys.modules))
