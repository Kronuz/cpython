import _imp
import importlib
import os
import sys
import unittest


class LazyImportsTest(unittest.TestCase):
    """Dynamically generated tests for modules in `test.test_lazy_imports`."""


def run_test_case(self, module_name: str, use_lazy_imports: bool):
    # Save the original import-related state
    original_lazy_modules = sys.lazy_modules.copy()
    original_modules = sys.modules.copy()

    try:
        sys.lazy_modules.clear()

        # Remove any previously loaded test modules to ensure a clean import
        for modname in list(sys.modules):
            if modname == "test" or modname.startswith("test."):
                del sys.modules[modname]

        # Set test-specific attributes to make them available to tests (using `self`)
        self._test_name = module_name
        self._lazy_imports = use_lazy_imports
        sys.modules["self"] = self  # allow test modules to access the test instance

        previous_state = _imp._set_lazy_imports(use_lazy_imports)
        try:
            importlib.import_module(module_name)
        finally:
            _imp._set_lazy_imports(*previous_state)
            del self._test_name
            del self._lazy_imports

    finally:
        sys.lazy_modules.clear()
        sys.lazy_modules.update(original_lazy_modules)
        sys.modules.clear()
        sys.modules.update(original_modules)


def make_test_case(module_name: str, use_lazy_imports: bool):
    def test(self):
        run_test_case(self, module_name, use_lazy_imports)

    return test


def discover_and_register_tests():
    base = os.path.dirname(__file__)
    for path in os.listdir(base):
        if path == "data" or path.startswith(("_", ".")):
            continue
        path = path.removesuffix(".py")
        test_name = path.replace(os.sep, "_")
        module_import_path = "test.test_lazy_imports." + path.replace(os.sep, ".")
        for use_lazy in (True, False):
            test_func_name = f"test_{test_name}{'_lazy' if use_lazy else '_eager'}"
            test_func = make_test_case(module_import_path, use_lazy)
            setattr(LazyImportsTest, test_func_name, test_func)


discover_and_register_tests()
