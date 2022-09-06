import self
import sys

import test.test_lazy_imports.data.metasyntactic.foo as foo

import test.test_lazy_imports.data.metasyntactic.foo.bar.baz

first_bar = test.test_lazy_imports.data.metasyntactic.foo.bar

del sys.modules["test.test_lazy_imports.data.metasyntactic.foo.bar"]

import test.test_lazy_imports.data.metasyntactic.foo.bar.thud

second_bar = test.test_lazy_imports.data.metasyntactic.foo.bar

self.assertIn("test.test_lazy_imports.data.metasyntactic.foo.bar", set(sys.modules))
sys_modules_bar = sys.modules["test.test_lazy_imports.data.metasyntactic.foo.bar"]

self.assertIsNot(first_bar, second_bar)
self.assertIsNot(sys_modules_bar, first_bar)
self.assertIs(sys_modules_bar, second_bar)

self.assertIn("baz", dir(first_bar))
self.assertNotIn("thud", dir(first_bar))

self.assertNotIn("baz", dir(second_bar))
self.assertIn("thud", dir(second_bar))
