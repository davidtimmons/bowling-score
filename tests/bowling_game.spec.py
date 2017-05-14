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
        """It should only return keys when there is a ball score argument."""
        frame = self.b.build_frame()
        def cause_error_1(): return frame['ball_1_score']
        def cause_error_2(): return frame['ball_2_score']
        self.assertRaises(KeyError, cause_error_1)
        self.assertRaises(KeyError, cause_error_2)


    def test_build_frame_special(self):
        """It should store strikes and spares."""
        frame_spare = self.b.build_frame(1, 9)
        frame_strike = self.b.build_frame(10)
        self.assertTrue(frame_spare.get('is_spare'))
        self.assertFalse(frame_spare.get('is_strike'))
        self.assertTrue(frame_strike.get('is_strike'))
        self.assertFalse(frame_strike.get('is_spare'))


    def test_build_frame_error(self):
        """It should throw an error if the ball score arguments are incorrect."""
        def cause_error_1(): self.b.build_frame(1, self.b.NUM_PINS)
        def cause_error_2(): self.b.build_frame(ball_2_score=self.b.NUM_PINS)
        self.assertRaises(ValueError, cause_error_1)
        self.assertRaises(ValueError, cause_error_2)
        self.assertIsInstance(self.b.build_frame(0, self.b.NUM_PINS), dict)


    def test_link_frames(self):
        """It should link two frames together using an object reference."""
        frame_1 = self.b.build_frame(1, 1)
        frame_2 = self.b.build_frame(2, 2)
        frame_1 = self.b.link_frames(frame_1, frame_2)
        self.assertEqual(frame_1.get('next_frame', None), frame_2)


    def test_calculate_forward_score_no_game(self):
        """It should do nothing if the game state is empty."""
        game_state = []
        b2 = BowlingGame(game_state=game_state)
        b2.calculate_forward_score(10)
        self.assertEqual(b2.current_frame, 0)


    def test_calculate_forward_score_n_frames(self):
        """It should calculate a frame score if there are one or more frames."""
        # One frame.
        game_state = []
        game_state.append(self.b.build_frame(1, 0))
        b2 = BowlingGame(game_state=game_state)
        b2.calculate_forward_score(b2.current_frame)
        self.assertEqual(game_state[0]['frame_score'], 1)

        # Two frames.
        game_state = []
        game_state.append(self.b.build_frame(1, 0))
        game_state.append(self.b.build_frame(0, 2))
        b2 = BowlingGame(game_state=game_state)
        b2.calculate_forward_score(b2.current_frame)
        self.assertEqual(game_state[0].get('frame_score'), 1)
        self.assertEqual(game_state[1].get('frame_score'), None)

        # Three frames.
        game_state = []
        game_state.append(self.b.build_frame(1, 0))
        game_state.append(self.b.build_frame(0, 2))
        game_state.append(self.b.build_frame(1, 2))
        b2 = BowlingGame(game_state=game_state)
        b2.calculate_forward_score(b2.current_frame)
        self.assertEqual(game_state[0].get('frame_score'), 1)
        self.assertEqual(game_state[1].get('frame_score'), None)
        self.assertEqual(game_state[2].get('frame_score'), None)

        # Four frames.
        game_state = []
        game_state.append(self.b.build_frame(1, 0))
        game_state.append(self.b.build_frame(0, 2))
        game_state.append(self.b.build_frame(1, 2))
        game_state.append(self.b.build_frame(2, 2))
        b2 = BowlingGame(game_state=game_state)
        b2.calculate_forward_score(b2.current_frame)
        self.assertEqual(game_state[0].get('frame_score'), None)
        self.assertEqual(game_state[1].get('frame_score'), 2)
        self.assertEqual(game_state[2].get('frame_score'), None)
        self.assertEqual(game_state[3].get('frame_score'), None)


    def test_calculate_forward_score_spares(self):
        """It should calculate a frame score if there is a spare."""
        game_state = []
        game_state.append(self.b.build_frame(1, 9))
        game_state.append(self.b.build_frame(5, 5))
        game_state.append(self.b.build_frame(10, 0))
        for i in range(len(game_state)-1):
            game_state[i] = self.b.link_frames(game_state[i], game_state[i+1])
        b2 = BowlingGame(game_state=game_state)
        b2.calculate_forward_score(b2.current_frame)
        b2.calculate_forward_score(b2.current_frame + 1)
        self.assertEqual(game_state[0].get('frame_score'), 15)
        self.assertEqual(game_state[1].get('frame_score'), 20)


    def test_calculate_forward_score_strikes(self):
        """It should calculate a frame score if there is a strike."""
        game_state = []
        game_state.append(self.b.build_frame(10))
        game_state.append(self.b.build_frame(5, 4))
        game_state.append(self.b.build_frame(10))
        game_state.append(self.b.build_frame(10))
        game_state.append(self.b.build_frame(10))
        for i in range(len(game_state)-1):
            game_state[i] = self.b.link_frames(game_state[i], game_state[i+1])
        b2 = BowlingGame(game_state=game_state)
        b2.calculate_forward_score(b2.current_frame - 2)
        b2.calculate_forward_score(b2.current_frame)
        self.assertEqual(game_state[0].get('frame_score'), 19)
        self.assertEqual(game_state[2].get('frame_score'), 30)


    def test_calculate_forward_score_no_score(self):
        """It should not calculate a frame score if it exists or information is missing."""
        # A frame score exists.
        game_state = [self.b.build_frame(1, 0)]
        b2 = BowlingGame(game_state=game_state)
        b2.calculate_forward_score(b2.current_frame)
        game_state[0]['ball_1_score'] = 10
        b2 = BowlingGame(game_state=game_state)
        b2.calculate_forward_score(b2.current_frame)
        self.assertEqual(game_state[0].get('frame_score'), 1)

        # Strike data is missing.
        game_state = [self.b.build_frame(10)]
        game_state.append(self.b.build_frame(1))
        b2 = BowlingGame(game_state=game_state)
        b2.calculate_forward_score(b2.current_frame)
        self.assertEqual(game_state[0].get('frame_score'), None)

        # Spare data is missing.
        game_state = [self.b.build_frame(5, 5)]
        b2 = BowlingGame(game_state=game_state)
        b2.calculate_forward_score(b2.current_frame)
        self.assertEqual(game_state[0].get('frame_score'), None)


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
