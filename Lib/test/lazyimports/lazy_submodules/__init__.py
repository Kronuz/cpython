"""
Test the status of submodules
"""
import self
import sys

import test.lazyimports.customized_modules
import test.lazyimports.customized_modules.foo.bar as bar
import test.lazyimports.customized_modules.foo.ack as ack

bar.Bar

self.assertIn("test.lazyimports.customized_modules.foo.bar", set(sys.modules))
if self._lazy_imports:
    self.assertNotIn("test.lazyimports.customized_modules.foo.ack", set(sys.modules))
else:
    self.assertIn("test.lazyimports.customized_modules.foo.ack", set(sys.modules))

import test.lazyimports.customized_modules.waldo.fred as fred

self.assertEqual(test.lazyimports.customized_modules.waldo.Waldo, "Waldo")
