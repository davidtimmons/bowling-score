"""Exercise code from <app/bowling_controller.py>."""

import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# from app.bowling_game import BowlingGame


class BowlingControllerTestCase(unittest.TestCase):

    # def setUp(self):
    #     """Instantiate a basic test object."""
    #     self.b = BowlingGame(10, 10, [])


    # def tearDown(self):
    #     """Destroy test object."""
    #     self.b = None


    # def test_current_frame(self):
    #     """It should return a value between 0 and NUM_FRAMES."""
    #     # Zero frames.
    #     game_state = []
    #     for i in range(self.b.NUM_FRAMES+2):
    #         n = i if i <= self.b.NUM_FRAMES else self.b.NUM_FRAMES
    #         b2 = BowlingGame(game_state=game_state)
    #         self.assertEqual(b2.current_frame, n)
    #         game_state.append({})


if __name__ == '__main__':
    unittest.main()
