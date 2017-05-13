"""Exercise code from <app/bowling_game.py>."""

import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.bowling_game import BowlingGame


class BowlingGameTestCase(unittest.TestCase):

    def setUp(self):
        """Instantiate the test object."""
        self.b = BowlingGame(10, 10)


    def test_build_frame_dict(self):
        """It should return a dictionary object."""
        frame = self.b.build_frame()
        self.assertIsInstance(frame, dict)


    def test_build_frame_defaults(self):
        """It should default the scores to -1 and next frame to None."""
        frame = self.b.build_frame()
        self.assertEqual(frame.get('ball_1_score', None), -1)
        self.assertEqual(frame.get('ball_2_score', None), -1)
        self.assertEqual(frame.get('next_frame', None), None)


    def test_build_frame_special(self):
        """It should store strikes, spares, and the next frame object reference."""
        frame_spare = self.b.build_frame(1, 9)
        frame_strike = self.b.build_frame(10)
        frame_next = self.b.build_frame(next_frame=frame_strike)
        self.assertTrue(frame_strike.get('is_strike', False))
        self.assertTrue(frame_spare.get('is_spare', False))
        self.assertFalse(frame_strike.get('is_spare', True))
        self.assertEqual(frame_next.get('next_frame', None), frame_strike)


    def test_link_frames(self):
        """It should link two frames together using an object reference."""
        frame_1 = self.b.build_frame(1, 1)
        frame_2 = self.b.build_frame(2, 2)
        frame_1 = self.b.link_frames(frame_1, frame_2)
        self.assertEqual(frame_1.get('next_frame', None), frame_2)


    def test_is_incomplete_frame(self):
        """It should indicate whether the frame is finished."""
        frame_1 = self.b.build_frame()
        frame_2 = self.b.build_frame(1)
        frame_3 = self.b.build_frame(1, 9)
        self.assertTrue(self.b.is_incomplete_frame(frame_1))
        self.assertTrue(self.b.is_incomplete_frame(frame_2))
        self.assertFalse(self.b.is_incomplete_frame(frame_3))


    def test_is_game_over(self):
        """It should indicate when the bowling game is over."""

        # Build a sample game state.
        game_state = []
        for i in range(9):
            frame = self.b.build_frame(1, 1)
            game_state.append(frame)

        # In a frame earlier than the 10th frame.
        self.assertFalse(self.b.is_game_over(game_state))

        # In the 10th frame, but the frame is incomplete.
        game_state.append(self.b.build_frame(1))
        self.assertFalse(self.b.is_game_over(game_state))

        # In the 10th frame, and there are no special balls.
        game_state.pop()
        game_state.append(self.b.build_frame(1, 1))
        self.assertTrue(self.b.is_game_over(game_state))

        # In the 10th frame, but there is a spare ball.
        game_state.pop()
        game_state.append(self.b.build_frame(1, 9))
        self.assertFalse(self.b.is_game_over(game_state))

        # In the 10th frame + 1 shot, and the 10th frame had a spare ball.
        game_state.append(self.b.build_frame(1))
        self.assertTrue(self.b.is_game_over(game_state))

        # In the 10th frame + 2 shots, and the 10th frame had a spare ball.
        game_state.pop()
        game_state.append(self.b.build_frame(1, 1))
        self.assertTrue(self.b.is_game_over(game_state))

        # In the 10th frame, but there is a strike ball.
        game_state.pop()
        game_state.pop()
        game_state.append(self.b.build_frame(10))
        self.assertFalse(self.b.is_game_over(game_state))

        # In the 10th frame + 1 shot, but the 10th frame had a strike ball.
        game_state.append(self.b.build_frame(10))
        self.assertFalse(self.b.is_game_over(game_state))

        # In the 10th frame + 2 shots, and the 10th + 1 frame had a normal ball.
        game_state.append(self.b.build_frame(1, 1))
        self.assertTrue(self.b.is_game_over(game_state))

        # In the 10th frame + 2 shots, and the 10th + 1 frame had a strike ball.
        game_state.pop()
        game_state.append(self.b.build_frame(10))
        self.assertTrue(self.b.is_game_over(game_state))


    # def test_build_frame_score(self):
    #     """It should store the number of pins knocked down."""
    #     frame_normal = self.b.build_frame(1, 1)
    #     frame_spare = self.b.build_frame(1, 9)
    #     frame_strike = self.b.build_frame(10)
    #     self.assertEqual(frame_normal.get('frame_score', None), 2)
    #     self.assertEqual(frame_spare.get('frame_score', None), 10)
    #     self.assertEqual(frame_strike.get('frame_score', None), 10)


if __name__ == '__main__':
    unittest.main()
