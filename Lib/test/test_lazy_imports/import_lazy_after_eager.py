import self
import importlib

importlib.set_lazy_imports(
    eager=["test.test_lazy_imports.data.module_same_name_aliased.foo.foo"]
)

from test.test_lazy_imports.data.module_same_name_aliased import foo

self.assertEqual(foo, 42)


importlib.set_lazy_imports(eager=[])

from test.test_lazy_imports.data.module_same_name_aliased.foo import foo

self.assertEqual(foo, 42)


from test.test_lazy_imports.data.module_same_name_aliased import foo

self.assertEqual(foo, 42)
