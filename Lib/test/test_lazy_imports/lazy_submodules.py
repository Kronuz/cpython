"""
Test the status of submodules
"""
import self
import sys

import test.test_lazy_imports.data.metasyntactic
import test.test_lazy_imports.data.metasyntactic.foo.bar as bar
import test.test_lazy_imports.data.metasyntactic.foo.ack as ack

bar.Bar

self.assertIn("test.test_lazy_imports.data.metasyntactic.foo.bar", set(sys.modules))
if self._lazy_imports:
    self.assertNotIn("test.test_lazy_imports.data.metasyntactic.foo.ack", set(sys.modules))
else:
    self.assertIn("test.test_lazy_imports.data.metasyntactic.foo.ack", set(sys.modules))

import test.test_lazy_imports.data.metasyntactic.waldo.fred as fred

self.assertEqual(test.test_lazy_imports.data.metasyntactic.waldo.Waldo, "Waldo")
