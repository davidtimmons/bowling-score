"""Exercise code from <app/helpers.py>."""

import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.helpers import read_only


class HelpersTestCase(unittest.TestCase):

    def setUp(self):
        """Create a class to test the constant decorator."""

        class TestClass(object):
            @read_only
            def MY_CONST(self): return 42

        self.t = TestClass()


    def test_constant_get(self):
        """It should return a value."""
        self.assertEqual(self.t.MY_CONST, 42)


    def test_constant_set(self):
        """It should raise an error when attempting to change the value."""
        def change_constant(): self.t.MY_CONST = 50
        self.assertRaises(TypeError, change_constant)


if __name__ == '__main__':
    unittest.main()
