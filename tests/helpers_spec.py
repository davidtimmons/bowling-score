"""Exercise code from <app/helpers.py>."""

import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.helpers import read_only, restrict_bounds


class HelpersTestCase(unittest.TestCase):

    def setUp(self):
        """Instantiate basic test object."""

        class TestClass(object):
            @read_only
            def MY_CONST(self): return 42

        self.t = TestClass()


    def tearDown(self):
        """Destroy test object."""
        self.t = None


    def test_read_only_get(self):
        """It should return a value."""
        self.assertEqual(self.t.MY_CONST, 42)


    def test_read_only_set(self):
        """It should raise an error when attempting to change the value."""
        def cause_error(): self.t.MY_CONST = 50
        self.assertRaises(TypeError, cause_error)


    def test_restrict_bounds_is_number(self):
        """It should return True if this is a number or False if not."""
        r = restrict_bounds(None, None)
        self.assertTrue(r.is_number(-42))
        self.assertTrue(r.is_number(0))
        self.assertTrue(r.is_number(int(5)))
        self.assertTrue(r.is_number(float(5)))
        self.assertTrue(r.is_number(complex(5)))
        self.assertTrue(r.is_number(True)) ## Evaluates to 1.
        self.assertFalse(r.is_number('apple'))
        self.assertFalse(r.is_number({}))
        self.assertFalse(r.is_number([]))
        self.assertFalse(r.is_number(None))


    def test_restrict_bounds_error(self):
        """It should raise a ValueError when the argument is outside the bounds."""
        @restrict_bounds(1, 5)
        def fn(arg): return arg
        def cause_error_1(): fn(0)
        def cause_error_2(): fn(6)
        self.assertRaises(ValueError, cause_error_1)
        self.assertRaises(ValueError, cause_error_2)


    def test_restrict_bounds_success(self):
        """It should call the function if the argument is inside or at the bounds."""
        @restrict_bounds(1, 5)
        def fn(arg): return arg
        self.assertEqual(fn(1), 1)
        self.assertEqual(fn(3), 3)
        self.assertEqual(fn(5), 5)


    def test_restrict_bounds_class(self):
        """It should work correctly with class functions."""
        class TestClass2(object):
            @restrict_bounds(1, 5)
            def fn(self, arg): return arg
        t2 = TestClass2()
        def cause_error_1(): t2.fn(0)
        def cause_error_2(): t2.fn(6)
        self.assertEqual(t2.fn(1), 1)
        self.assertEqual(t2.fn(3), 3)
        self.assertEqual(t2.fn(5), 5)

        
if __name__ == '__main__':
    unittest.main()
