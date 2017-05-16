"""Exercise all code found in the tests directory."""

import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tests.bowling_controller_spec import BowlingControllerTestCase
from tests.bowling_game_spec import BowlingGameTestCase
from tests.helpers_spec import HelpersTestCase


if __name__ == '__main__':
    unittest.main()
