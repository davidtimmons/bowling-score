"""Exercise code from <app/bowling_controller.py>."""

import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.bowling_controller import BowlingController


class BowlingControllerTestCase(unittest.TestCase):

    # def setUp(self):
    #     """Instantiate a basic test object."""
    #     self.b = BowlingGame(10, 10, [])


    # def tearDown(self):
    #     """Destroy test object."""
    #     self.b = None

    def test_get_all_game_state(self):
        """It should"""
        pass


    def test_get_all_frame_data(self):
        """It should"""
        pass


    def test_get_current_player(self):
        """It should return the current player."""
        b = BowlingController(2, 10, 10, [])
        self.assertEqual(b.get_current_player(), 1)


    def test_get_frame_data(self):
        """It should return the ith frame data object for the current player."""
        b = BowlingController(1, 10, 10, [])
        for i in range(10): b.post_new_score(1)
        self.assertEqual(b.get_current_player(), 1)


    def test_get_game_state(self):
        """It should"""
        pass


    def test_post_new_score(self):
        """It should add a ball score to the current player's frame."""
        game_states = []
        b = BowlingController(2, 10, 10, game_states)
        b.post_new_score(5)
        player_1_frame_1 = game_states[0].get_frame_data(1)
        self.assertEqual(player_1_frame_1.get('ball_1_score'), 5)


    def test_post_new_score_players(self):
        """It should change the current player after posting a score."""
        b = BowlingController(3, 10, 10, [])
        self.assertEqual(b.get_current_player(), 1)
        b.post_new_score(5)
        self.assertEqual(b.get_current_player(), 2)
        b.post_new_score(5)
        self.assertEqual(b.get_current_player(), 3)
        b.post_new_score(5)
        self.assertEqual(b.get_current_player(), 1)


    def test_match_the_bowling_example(self):
        """It should match the example at the scoring tutorial website."""
        # URL: http://bowling.about.com/od/rulesofthegame/a/bowlingscoring.htm
        pass


if __name__ == '__main__':
    unittest.main()
