import self
import test.lazyimports.attribute_side_effect.main as main

expected_version = "1.0"
expected_copyright = "Copyright (c) 2001-2022 Python Software Foundation."

"""
When the package `requests` made use of submodule `__version__`,
it would trigger the side effect of overwriting `requests` module's own `__version__`

Test this trigger doesn't happen
"""
self.assertEqual(main.__copyright__, expected_copyright)
self.assertEqual(main.__version__, expected_version)
