"""Exercise code from <app/bowling_controller.py>."""

import unittest
import os
import sys
from functools import reduce

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.bowling_controller import BowlingController


class BowlingControllerTestCase(unittest.TestCase):

    def test_get_current_player(self):
        """It should return the current player."""
        b = BowlingController(2, 10, 10, [])
        self.assertEqual(b.get_current_player(), 1)


    def test_get_current_score(self):
        """It should return the current score for this player."""
        b = BowlingController(1, 10, 10, [])
        for i in range(10): b.post_new_score(1)
        self.assertEqual(b.get_current_score(1), 10)


    def test_get_current_scores(self):
        """It should return the current score for all players."""
        b = BowlingController(3, 10, 10, [])
        for i in range(30): b.post_new_score(1)
        scores = b.get_current_scores()
        self.assertEqual(len(scores), 3)
        self.assertEqual(reduce(lambda x, y: x + y, scores), 30)


    def test_get_frame_data(self):
        """It should return the ith frame data object for the current player."""
        b = BowlingController(1, 10, 10, [])
        for i in range(10): b.post_new_score(1)
        self.assertEqual(b.get_current_player(), 1)


    def test_get_frames(self):
        """It should get the ith frame data for all players."""
        b = BowlingController(5, 10, 10, [])
        for i in range(5): b.post_new_score(1)
        frames = b.get_frames(1)
        self.assertEqual(len(b.get_frames(1)), 5)


    def test_get_game_state(self):
        """It should return the game state for this player."""
        b = BowlingController(1, 10, 10, [])
        for i in range(2): b.post_new_score(1)
        frames = b.get_game_state(1)
        self.assertEqual(len(frames), 1)
        self.assertEqual(frames[0].get('running_total'), 2)


    def test_get_game_states(self):
        """It should return the game state for all players."""
        b = BowlingController(5, 10, 10, [])
        self.assertEqual(len(b.get_game_states()), 5)


    def test_is_game_over(self):
        """It should return a boolean indicating if the game should continue for this player."""
        b = BowlingController(1, 10, 10, [])
        self.assertFalse(b.is_game_over(1))
        for i in range(20): b.post_new_score(1)
        self.assertTrue(b.is_game_over(1))


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
        self.assertEqual(b.get_current_player(), 1)
        b.post_new_score(5)
        self.assertEqual(b.get_current_player(), 2)
        b.post_new_score(5)
        b.post_new_score(5)
        self.assertEqual(b.get_current_player(), 3)
        b.post_new_score(10)
        self.assertEqual(b.get_current_player(), 1)


    def test_match_the_bowling_example(self):
        """It should duplicate the final scores in the bowling scoring tutorial example."""
        # URL: http://bowling.about.com/od/rulesofthegame/a/bowlingscoring.htm
        b = BowlingController(1, 10, 10, [])
        b.post_new_score(10) ## Frame 1, Ball 1-2
        b.post_new_score(7) ## Frame 2, Ball 1
        b.post_new_score(3) ## Frame 2, Ball 2
        b.post_new_score(7) ## Frame 3, Ball 1
        b.post_new_score(2) ## Frame 3, Ball 2
        b.post_new_score(9) ## Frame 4, Ball 1
        b.post_new_score(1) ## Frame 4, Ball 2
        b.post_new_score(10) ## Frame 5, Ball 1-2
        b.post_new_score(10) ## Frame 6, Ball 1-2
        b.post_new_score(10) ## Frame 7, Ball 1-2
        b.post_new_score(2) ## Frame 8, Ball 1
        b.post_new_score(3) ## Frame 8, Ball 2
        b.post_new_score(6) ## Frame 9, Ball 1
        b.post_new_score(4) ## Frame 9, Ball 2
        b.post_new_score(7) ## Frame 10, Ball 1
        b.post_new_score(3) ## Frame 10, Ball 2
        b.post_new_score(3) ## Frame 10, Ball 3
        frame_data = []
        for i in range(1, 11): frame_data.append(b.get_frame_data(i, 1))
        self.assertTrue(b.is_game_over(1))
        self.assertEqual(frame_data[0].get('frame_score'), 20)
        self.assertEqual(frame_data[0].get('running_total'), 20)
        self.assertEqual(frame_data[1].get('frame_score'), 17)
        self.assertEqual(frame_data[1].get('running_total'), 37)
        self.assertEqual(frame_data[2].get('frame_score'), 9)
        self.assertEqual(frame_data[2].get('running_total'), 46)
        self.assertEqual(frame_data[3].get('frame_score'), 20)
        self.assertEqual(frame_data[3].get('running_total'), 66)
        self.assertEqual(frame_data[4].get('frame_score'), 30)
        self.assertEqual(frame_data[4].get('running_total'), 96)
        self.assertEqual(frame_data[5].get('frame_score'), 22)
        self.assertEqual(frame_data[5].get('running_total'), 118)
        self.assertEqual(frame_data[6].get('frame_score'), 15)
        self.assertEqual(frame_data[6].get('running_total'), 133)
        self.assertEqual(frame_data[7].get('frame_score'), 5)
        self.assertEqual(frame_data[7].get('running_total'), 138)
        self.assertEqual(frame_data[8].get('frame_score'), 17)
        self.assertEqual(frame_data[8].get('running_total'), 155)
        self.assertEqual(frame_data[9].get('frame_score'), 13)
        self.assertEqual(frame_data[9].get('running_total'), 168)


    def test_match_the_bowling_example_running_frame_scores(self):
        """It should duplicate the running frame scores in the bowling scoring tutorial example."""
        # URL: http://bowling.about.com/od/rulesofthegame/a/bowlingscoring.htm
        b = BowlingController(1, 10, 10, [])
        b.post_new_score(10) ## Frame 1, Ball 1-2
        self.assertEqual(b.get_frame_data(1, 1).get('frame_score'), None)
        b.post_new_score(7) ## Frame 2, Ball 1
        self.assertEqual(b.get_frame_data(1, 1).get('frame_score'), None)
        self.assertEqual(b.get_frame_data(2, 1).get('frame_score'), None)
        b.post_new_score(3) ## Frame 2, Ball 2
        self.assertEqual(b.get_frame_data(1, 1).get('frame_score'), 20)
        self.assertEqual(b.get_frame_data(2, 1).get('frame_score'), None)
        b.post_new_score(7) ## Frame 3, Ball 1
        self.assertEqual(b.get_frame_data(1, 1).get('frame_score'), 20)
        self.assertEqual(b.get_frame_data(2, 1).get('frame_score'), 17)
        b.post_new_score(2) ## Frame 3, Ball 2
        self.assertEqual(b.get_frame_data(1, 1).get('frame_score'), 20)
        self.assertEqual(b.get_frame_data(2, 1).get('frame_score'), 17)
        self.assertEqual(b.get_frame_data(3, 1).get('frame_score'), 9)
        b.post_new_score(9) ## Frame 4, Ball 1
        self.assertEqual(b.get_frame_data(1, 1).get('frame_score'), 20)
        self.assertEqual(b.get_frame_data(2, 1).get('frame_score'), 17)
        self.assertEqual(b.get_frame_data(3, 1).get('frame_score'), 9)
        self.assertEqual(b.get_frame_data(4, 1).get('frame_score'), None)
        b.post_new_score(1) ## Frame 4, Ball 2
        self.assertEqual(b.get_frame_data(1, 1).get('frame_score'), 20)
        self.assertEqual(b.get_frame_data(2, 1).get('frame_score'), 17)
        self.assertEqual(b.get_frame_data(3, 1).get('frame_score'), 9)
        self.assertEqual(b.get_frame_data(4, 1).get('frame_score'), None)
        b.post_new_score(10) ## Frame 5, Ball 1-2
        self.assertEqual(b.get_frame_data(1, 1).get('frame_score'), 20)
        self.assertEqual(b.get_frame_data(2, 1).get('frame_score'), 17)
        self.assertEqual(b.get_frame_data(3, 1).get('frame_score'), 9)
        self.assertEqual(b.get_frame_data(4, 1).get('frame_score'), 20)
        self.assertEqual(b.get_frame_data(5, 1).get('frame_score'), None)
        b.post_new_score(10) ## Frame 6, Ball 1-2
        self.assertEqual(b.get_frame_data(1, 1).get('frame_score'), 20)
        self.assertEqual(b.get_frame_data(2, 1).get('frame_score'), 17)
        self.assertEqual(b.get_frame_data(3, 1).get('frame_score'), 9)
        self.assertEqual(b.get_frame_data(4, 1).get('frame_score'), 20)
        self.assertEqual(b.get_frame_data(5, 1).get('frame_score'), None)
        self.assertEqual(b.get_frame_data(6, 1).get('frame_score'), None)
        b.post_new_score(10) ## Frame 7, Ball 1-2
        self.assertEqual(b.get_frame_data(1, 1).get('frame_score'), 20)
        self.assertEqual(b.get_frame_data(2, 1).get('frame_score'), 17)
        self.assertEqual(b.get_frame_data(3, 1).get('frame_score'), 9)
        self.assertEqual(b.get_frame_data(4, 1).get('frame_score'), 20)
        self.assertEqual(b.get_frame_data(5, 1).get('frame_score'), 30)
        self.assertEqual(b.get_frame_data(6, 1).get('frame_score'), None)
        self.assertEqual(b.get_frame_data(7, 1).get('frame_score'), None)
        b.post_new_score(2) ## Frame 8, Ball 1
        self.assertEqual(b.get_frame_data(1, 1).get('frame_score'), 20)
        self.assertEqual(b.get_frame_data(2, 1).get('frame_score'), 17)
        self.assertEqual(b.get_frame_data(3, 1).get('frame_score'), 9)
        self.assertEqual(b.get_frame_data(4, 1).get('frame_score'), 20)
        self.assertEqual(b.get_frame_data(5, 1).get('frame_score'), 30)
        self.assertEqual(b.get_frame_data(6, 1).get('frame_score'), 22)
        self.assertEqual(b.get_frame_data(7, 1).get('frame_score'), None)
        self.assertEqual(b.get_frame_data(8, 1).get('frame_score'), None)
        b.post_new_score(3) ## Frame 8, Ball 2
        self.assertEqual(b.get_frame_data(1, 1).get('frame_score'), 20)
        self.assertEqual(b.get_frame_data(2, 1).get('frame_score'), 17)
        self.assertEqual(b.get_frame_data(3, 1).get('frame_score'), 9)
        self.assertEqual(b.get_frame_data(4, 1).get('frame_score'), 20)
        self.assertEqual(b.get_frame_data(5, 1).get('frame_score'), 30)
        self.assertEqual(b.get_frame_data(6, 1).get('frame_score'), 22)
        self.assertEqual(b.get_frame_data(7, 1).get('frame_score'), 15)
        self.assertEqual(b.get_frame_data(8, 1).get('frame_score'), 5)
        b.post_new_score(6) ## Frame 9, Ball 1
        self.assertEqual(b.get_frame_data(1, 1).get('frame_score'), 20)
        self.assertEqual(b.get_frame_data(2, 1).get('frame_score'), 17)
        self.assertEqual(b.get_frame_data(3, 1).get('frame_score'), 9)
        self.assertEqual(b.get_frame_data(4, 1).get('frame_score'), 20)
        self.assertEqual(b.get_frame_data(5, 1).get('frame_score'), 30)
        self.assertEqual(b.get_frame_data(6, 1).get('frame_score'), 22)
        self.assertEqual(b.get_frame_data(7, 1).get('frame_score'), 15)
        self.assertEqual(b.get_frame_data(8, 1).get('frame_score'), 5)
        self.assertEqual(b.get_frame_data(9, 1).get('frame_score'), None)
        b.post_new_score(4) ## Frame 9, Ball 2
        self.assertEqual(b.get_frame_data(1, 1).get('frame_score'), 20)
        self.assertEqual(b.get_frame_data(2, 1).get('frame_score'), 17)
        self.assertEqual(b.get_frame_data(3, 1).get('frame_score'), 9)
        self.assertEqual(b.get_frame_data(4, 1).get('frame_score'), 20)
        self.assertEqual(b.get_frame_data(5, 1).get('frame_score'), 30)
        self.assertEqual(b.get_frame_data(6, 1).get('frame_score'), 22)
        self.assertEqual(b.get_frame_data(7, 1).get('frame_score'), 15)
        self.assertEqual(b.get_frame_data(8, 1).get('frame_score'), 5)
        self.assertEqual(b.get_frame_data(9, 1).get('frame_score'), None)
        b.post_new_score(7) ## Frame 10, Ball 1
        self.assertEqual(b.get_frame_data(1, 1).get('frame_score'), 20)
        self.assertEqual(b.get_frame_data(2, 1).get('frame_score'), 17)
        self.assertEqual(b.get_frame_data(3, 1).get('frame_score'), 9)
        self.assertEqual(b.get_frame_data(4, 1).get('frame_score'), 20)
        self.assertEqual(b.get_frame_data(5, 1).get('frame_score'), 30)
        self.assertEqual(b.get_frame_data(6, 1).get('frame_score'), 22)
        self.assertEqual(b.get_frame_data(7, 1).get('frame_score'), 15)
        self.assertEqual(b.get_frame_data(8, 1).get('frame_score'), 5)
        self.assertEqual(b.get_frame_data(9, 1).get('frame_score'), 17)
        self.assertEqual(b.get_frame_data(10, 1).get('frame_score'), None)
        b.post_new_score(3) ## Frame 10, Ball 2
        self.assertEqual(b.get_frame_data(1, 1).get('frame_score'), 20)
        self.assertEqual(b.get_frame_data(2, 1).get('frame_score'), 17)
        self.assertEqual(b.get_frame_data(3, 1).get('frame_score'), 9)
        self.assertEqual(b.get_frame_data(4, 1).get('frame_score'), 20)
        self.assertEqual(b.get_frame_data(5, 1).get('frame_score'), 30)
        self.assertEqual(b.get_frame_data(6, 1).get('frame_score'), 22)
        self.assertEqual(b.get_frame_data(7, 1).get('frame_score'), 15)
        self.assertEqual(b.get_frame_data(8, 1).get('frame_score'), 5)
        self.assertEqual(b.get_frame_data(9, 1).get('frame_score'), 17)
        self.assertEqual(b.get_frame_data(10, 1).get('frame_score'), None)
        b.post_new_score(3) ## Frame 10, Ball 3
        self.assertEqual(b.get_frame_data(1, 1).get('frame_score'), 20)
        self.assertEqual(b.get_frame_data(2, 1).get('frame_score'), 17)
        self.assertEqual(b.get_frame_data(3, 1).get('frame_score'), 9)
        self.assertEqual(b.get_frame_data(4, 1).get('frame_score'), 20)
        self.assertEqual(b.get_frame_data(5, 1).get('frame_score'), 30)
        self.assertEqual(b.get_frame_data(6, 1).get('frame_score'), 22)
        self.assertEqual(b.get_frame_data(7, 1).get('frame_score'), 15)
        self.assertEqual(b.get_frame_data(8, 1).get('frame_score'), 5)
        self.assertEqual(b.get_frame_data(9, 1).get('frame_score'), 17)
        self.assertEqual(b.get_frame_data(10, 1).get('frame_score'), 13)


    def test_match_the_bowling_example_running_total_scores(self):
        """It should duplicate the running total scores in the bowling scoring tutorial example."""
        # URL: http://bowling.about.com/od/rulesofthegame/a/bowlingscoring.htm
        b = BowlingController(1, 10, 10, [])
        b.post_new_score(10) ## Frame 1, Ball 1-2
        self.assertEqual(b.get_frame_data(1, 1).get('running_total'), 0)
        b.post_new_score(7) ## Frame 2, Ball 1
        self.assertEqual(b.get_frame_data(1, 1).get('running_total'), 0)
        self.assertEqual(b.get_frame_data(2, 1).get('running_total'), 0)
        b.post_new_score(3) ## Frame 2, Ball 2
        self.assertEqual(b.get_frame_data(1, 1).get('running_total'), 20)
        self.assertEqual(b.get_frame_data(2, 1).get('running_total'), 20)
        b.post_new_score(7) ## Frame 3, Ball 1
        self.assertEqual(b.get_frame_data(1, 1).get('running_total'), 20)
        self.assertEqual(b.get_frame_data(2, 1).get('running_total'), 37)
        self.assertEqual(b.get_frame_data(3, 1).get('running_total'), 37)
        b.post_new_score(2) ## Frame 3, Ball 2
        self.assertEqual(b.get_frame_data(1, 1).get('running_total'), 20)
        self.assertEqual(b.get_frame_data(2, 1).get('running_total'), 37)
        self.assertEqual(b.get_frame_data(3, 1).get('running_total'), 46)
        b.post_new_score(9) ## Frame 4, Ball 1
        self.assertEqual(b.get_frame_data(1, 1).get('running_total'), 20)
        self.assertEqual(b.get_frame_data(2, 1).get('running_total'), 37)
        self.assertEqual(b.get_frame_data(3, 1).get('running_total'), 46)
        self.assertEqual(b.get_frame_data(4, 1).get('running_total'), 46)
        b.post_new_score(1) ## Frame 4, Ball 2
        self.assertEqual(b.get_frame_data(1, 1).get('running_total'), 20)
        self.assertEqual(b.get_frame_data(2, 1).get('running_total'), 37)
        self.assertEqual(b.get_frame_data(3, 1).get('running_total'), 46)
        self.assertEqual(b.get_frame_data(4, 1).get('running_total'), 46)
        b.post_new_score(10) ## Frame 5, Ball 1-2
        self.assertEqual(b.get_frame_data(1, 1).get('running_total'), 20)
        self.assertEqual(b.get_frame_data(2, 1).get('running_total'), 37)
        self.assertEqual(b.get_frame_data(3, 1).get('running_total'), 46)
        self.assertEqual(b.get_frame_data(4, 1).get('running_total'), 66)
        self.assertEqual(b.get_frame_data(5, 1).get('running_total'), 66)
        b.post_new_score(10) ## Frame 6, Ball 1-2
        self.assertEqual(b.get_frame_data(1, 1).get('running_total'), 20)
        self.assertEqual(b.get_frame_data(2, 1).get('running_total'), 37)
        self.assertEqual(b.get_frame_data(3, 1).get('running_total'), 46)
        self.assertEqual(b.get_frame_data(4, 1).get('running_total'), 66)
        self.assertEqual(b.get_frame_data(5, 1).get('running_total'), 66)
        self.assertEqual(b.get_frame_data(6, 1).get('running_total'), 66)
        b.post_new_score(10) ## Frame 7, Ball 1-2
        self.assertEqual(b.get_frame_data(1, 1).get('running_total'), 20)
        self.assertEqual(b.get_frame_data(2, 1).get('running_total'), 37)
        self.assertEqual(b.get_frame_data(3, 1).get('running_total'), 46)
        self.assertEqual(b.get_frame_data(4, 1).get('running_total'), 66)
        self.assertEqual(b.get_frame_data(5, 1).get('running_total'), 96)
        self.assertEqual(b.get_frame_data(6, 1).get('running_total'), 96)
        self.assertEqual(b.get_frame_data(7, 1).get('running_total'), 96)
        b.post_new_score(2) ## Frame 8, Ball 1
        self.assertEqual(b.get_frame_data(1, 1).get('running_total'), 20)
        self.assertEqual(b.get_frame_data(2, 1).get('running_total'), 37)
        self.assertEqual(b.get_frame_data(3, 1).get('running_total'), 46)
        self.assertEqual(b.get_frame_data(4, 1).get('running_total'), 66)
        self.assertEqual(b.get_frame_data(5, 1).get('running_total'), 96)
        self.assertEqual(b.get_frame_data(6, 1).get('running_total'), 118)
        self.assertEqual(b.get_frame_data(7, 1).get('running_total'), 118)
        self.assertEqual(b.get_frame_data(8, 1).get('running_total'), 118)
        b.post_new_score(3) ## Frame 8, Ball 2
        self.assertEqual(b.get_frame_data(1, 1).get('running_total'), 20)
        self.assertEqual(b.get_frame_data(2, 1).get('running_total'), 37)
        self.assertEqual(b.get_frame_data(3, 1).get('running_total'), 46)
        self.assertEqual(b.get_frame_data(4, 1).get('running_total'), 66)
        self.assertEqual(b.get_frame_data(5, 1).get('running_total'), 96)
        self.assertEqual(b.get_frame_data(6, 1).get('running_total'), 118)
        self.assertEqual(b.get_frame_data(7, 1).get('running_total'), 133)
        self.assertEqual(b.get_frame_data(8, 1).get('running_total'), 138)
        b.post_new_score(6) ## Frame 9, Ball 1
        self.assertEqual(b.get_frame_data(1, 1).get('running_total'), 20)
        self.assertEqual(b.get_frame_data(2, 1).get('running_total'), 37)
        self.assertEqual(b.get_frame_data(3, 1).get('running_total'), 46)
        self.assertEqual(b.get_frame_data(4, 1).get('running_total'), 66)
        self.assertEqual(b.get_frame_data(5, 1).get('running_total'), 96)
        self.assertEqual(b.get_frame_data(6, 1).get('running_total'), 118)
        self.assertEqual(b.get_frame_data(7, 1).get('running_total'), 133)
        self.assertEqual(b.get_frame_data(8, 1).get('running_total'), 138)
        self.assertEqual(b.get_frame_data(9, 1).get('running_total'), 138)
        b.post_new_score(4) ## Frame 9, Ball 2
        self.assertEqual(b.get_frame_data(1, 1).get('running_total'), 20)
        self.assertEqual(b.get_frame_data(2, 1).get('running_total'), 37)
        self.assertEqual(b.get_frame_data(3, 1).get('running_total'), 46)
        self.assertEqual(b.get_frame_data(4, 1).get('running_total'), 66)
        self.assertEqual(b.get_frame_data(5, 1).get('running_total'), 96)
        self.assertEqual(b.get_frame_data(6, 1).get('running_total'), 118)
        self.assertEqual(b.get_frame_data(7, 1).get('running_total'), 133)
        self.assertEqual(b.get_frame_data(8, 1).get('running_total'), 138)
        self.assertEqual(b.get_frame_data(9, 1).get('running_total'), 138)
        b.post_new_score(7) ## Frame 10, Ball 1
        self.assertEqual(b.get_frame_data(1, 1).get('running_total'), 20)
        self.assertEqual(b.get_frame_data(2, 1).get('running_total'), 37)
        self.assertEqual(b.get_frame_data(3, 1).get('running_total'), 46)
        self.assertEqual(b.get_frame_data(4, 1).get('running_total'), 66)
        self.assertEqual(b.get_frame_data(5, 1).get('running_total'), 96)
        self.assertEqual(b.get_frame_data(6, 1).get('running_total'), 118)
        self.assertEqual(b.get_frame_data(7, 1).get('running_total'), 133)
        self.assertEqual(b.get_frame_data(8, 1).get('running_total'), 138)
        self.assertEqual(b.get_frame_data(9, 1).get('running_total'), 155)
        b.post_new_score(3) ## Frame 10, Ball 2
        self.assertEqual(b.get_frame_data(1, 1).get('running_total'), 20)
        self.assertEqual(b.get_frame_data(2, 1).get('running_total'), 37)
        self.assertEqual(b.get_frame_data(3, 1).get('running_total'), 46)
        self.assertEqual(b.get_frame_data(4, 1).get('running_total'), 66)
        self.assertEqual(b.get_frame_data(5, 1).get('running_total'), 96)
        self.assertEqual(b.get_frame_data(6, 1).get('running_total'), 118)
        self.assertEqual(b.get_frame_data(7, 1).get('running_total'), 133)
        self.assertEqual(b.get_frame_data(8, 1).get('running_total'), 138)
        self.assertEqual(b.get_frame_data(9, 1).get('running_total'), 155)
        self.assertEqual(b.get_frame_data(10, 1).get('running_total'), 155)
        b.post_new_score(3) ## Frame 10, Ball 3
        self.assertEqual(b.get_frame_data(1, 1).get('running_total'), 20)
        self.assertEqual(b.get_frame_data(2, 1).get('running_total'), 37)
        self.assertEqual(b.get_frame_data(3, 1).get('running_total'), 46)
        self.assertEqual(b.get_frame_data(4, 1).get('running_total'), 66)
        self.assertEqual(b.get_frame_data(5, 1).get('running_total'), 96)
        self.assertEqual(b.get_frame_data(6, 1).get('running_total'), 118)
        self.assertEqual(b.get_frame_data(7, 1).get('running_total'), 133)
        self.assertEqual(b.get_frame_data(8, 1).get('running_total'), 138)
        self.assertEqual(b.get_frame_data(9, 1).get('running_total'), 155)
        self.assertEqual(b.get_frame_data(10, 1).get('running_total'), 168)


if __name__ == '__main__':
    unittest.main()
