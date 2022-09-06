"""
Test the behavior when a module has a sub-module and a variable with the same namings
Different import/define orderings will expect different results
"""
import self
import sys

from test.test_lazy_imports.data import module_same_name_var_order1
self.assertEqual(module_same_name_var_order1.bar, "Blah")

from test.test_lazy_imports.data import module_same_name_var_order2
self.assertEqual(module_same_name_var_order2.bar, sys.modules["test.test_lazy_imports.data.module_same_name_var_order2.bar"])
