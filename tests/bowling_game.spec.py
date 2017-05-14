"""Exercise code from <app/bowling_game.py>."""

import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.bowling_game import BowlingGame


class BowlingGameTestCase(unittest.TestCase):

    def setUp(self):
        """Instantiate a basic test object."""
        self.b = BowlingGame(10, 10, [])


    def tearDown(self):
        """Destroy test object."""
        self.b = None


    def test_get_game_state(self):
        """It should return a deep copy of the game state."""
        game_state = [{'a': 1, 'b': 2}, {'c': 3, 'd': 4}]
        b2 = BowlingGame(game_state=game_state)
        inner_state = b2.get_game_state()
        self.assertEqual(inner_state, game_state)
        game_state[0]['a'] = 5
        self.assertNotEqual(inner_state, game_state)


    def test_current_frame(self):
        """It should return a value between 0 and NUM_FRAMES."""
        # Zero frames.
        game_state = []
        for i in range(self.b.NUM_FRAMES+2):
            n = i if i <= self.b.NUM_FRAMES else self.b.NUM_FRAMES
            b2 = BowlingGame(game_state=game_state)
            self.assertEqual(b2.current_frame, n)
            game_state.append({})


    def test_get_frame_data(self):
        """It should return frame data without the object link."""
        game_state = [
            {'ball_1_score': 0, 'ball_2_score': 1, 'next_frame': True},
            {'ball_1_score': 2, 'is_spare': False},
        ]
        b2 = BowlingGame(game_state=game_state)
        frame_1 = b2.get_frame_data(1)
        frame_2 = b2.get_frame_data(2)
        self.assertEqual(frame_1, {'ball_1_score': 0, 'ball_2_score': 1})
        self.assertEqual(frame_2, game_state[1])
        self.assertEqual(game_state[0]['next_frame'], True)
        self.assertEqual(b2.get_frame_data(-1), {})
        self.assertEqual(b2.get_frame_data(20), {})


    def test_build_frame_dict(self):
        """It should return a dictionary object."""
        frame = self.b.build_frame()
        self.assertIsInstance(frame, dict)


    def test_build_frame_keys(self):
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
        self.assertEqual(frame_strike.get('ball_2_score'), 0)


    def test_build_frame_error(self):
        """It should throw an error if the ball score arguments are incorrect."""
        def cause_error_1(): self.b.build_frame(-1)
        def cause_error_2(): self.b.build_frame(self.b.NUM_PINS+1)
        def cause_error_3(): self.b.build_frame(0, -1)
        def cause_error_4(): self.b.build_frame(0, self.b.NUM_PINS+1)
        def cause_error_5(): self.b.build_frame(1, self.b.NUM_PINS)
        def cause_error_6(): self.b.build_frame(ball_2_score=self.b.NUM_PINS)
        self.assertRaises(ValueError, cause_error_1)
        self.assertRaises(ValueError, cause_error_2)
        self.assertRaises(ValueError, cause_error_3)
        self.assertRaises(ValueError, cause_error_4)
        self.assertRaises(ValueError, cause_error_5)
        self.assertRaises(ValueError, cause_error_6)
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


    def test_calculate_frame_scores(self):
        """It should calculate up to three frame scores."""
        # Open frames.
        game_state = [
            {'ball_1_score': 10},
            {'ball_1_score': 0, 'ball_2_score': 1},
            {'ball_1_score': 0, 'ball_2_score': 2},
            {'ball_1_score': 0, 'ball_2_score': 3},
        ]
        for i in range(len(game_state)-1):
            game_state[i] = self.b.link_frames(game_state[i], game_state[i+1])
        b2 = BowlingGame(game_state=game_state)
        b2.calculate_frame_scores()
        self.assertEqual(game_state[0].get('frame_score'), None)
        self.assertEqual(game_state[1].get('frame_score'), 1)
        self.assertEqual(game_state[2].get('frame_score'), 2)
        self.assertEqual(game_state[3].get('frame_score'), 3)

        # Spares.
        game_state = [
            {'ball_1_score': 0, 'ball_2_score': 1},
            {'ball_1_score': 5, 'ball_2_score': 5, 'is_spare': True},
            {'ball_1_score': 3, 'ball_2_score': 4},
        ]
        for i in range(len(game_state)-1):
            game_state[i] = self.b.link_frames(game_state[i], game_state[i+1])
        b2 = BowlingGame(game_state=game_state)
        b2.calculate_frame_scores()
        self.assertEqual(game_state[0].get('frame_score'), 1)
        self.assertEqual(game_state[1].get('frame_score'), 13)
        self.assertEqual(game_state[2].get('frame_score'), 7)

        # Strikes.
        game_state = [
            {'ball_1_score': 10, 'is_strike': True},
            {'ball_1_score': 10, 'is_strike': True},
            {'ball_1_score': 5, 'ball_2_score': 5, 'is_spare': True},
        ]
        for i in range(len(game_state)-1):
            game_state[i] = self.b.link_frames(game_state[i], game_state[i+1])
        b2 = BowlingGame(game_state=game_state)
        b2.calculate_frame_scores()
        self.assertEqual(game_state[0].get('frame_score'), 25)
        self.assertEqual(game_state[1].get('frame_score'), 20)
        self.assertEqual(game_state[2].get('frame_score'), None)


    def test_calculate_running_total(self):
        """It should calculate all possible running total scores."""
        game_state = [
            {'frame_score': 10, 'is_strike': True},
            {'frame_score': 8},
            {'frame_score': 3},
            {'frame_score': 9},
            {'ball_1_score': 10, 'is_strike': True},
        ]
        b2 = BowlingGame(game_state=game_state)
        b2.calculate_running_total()
        self.assertEqual(game_state[0].get('running_total'), 10)
        self.assertEqual(game_state[1].get('running_total'), 18)
        self.assertEqual(game_state[2].get('running_total'), 21)
        self.assertEqual(game_state[3].get('running_total'), 30)

        # This frame score is effectively zero until there is enough frame data.
        self.assertEqual(game_state[4].get('running_total'), 30)
        self.assertEqual(len(game_state), 5)


    def test_add_ball_score_start(self):
        """It should create a new frame if this is a new game."""
        self.b.add_ball_score(5)
        game = self.b.get_game_state()
        self.assertEqual(len(game), 1)


    def test_add_ball_score_frame_1(self):
        """It should complete the first frame or add a new frame."""
        # Complete the frame.
        game_state = [{'ball_1_score': 1}]
        b2 = BowlingGame(game_state=game_state)
        b2.add_ball_score(5)
        game = b2.get_game_state()
        self.assertEqual(len(game), 1)

        # Add the second frame.
        game_state = [{'ball_1_score': 1, 'ball_2_score': 1}]
        b2 = BowlingGame(game_state=game_state)
        b2.add_ball_score(5)
        game = b2.get_game_state()
        self.assertEqual(len(game), 2)
        self.assertEqual(game[0]['next_frame'], game[1])


    def test_add_ball_score_frame_n(self):
        """It should complete the nth frame or add a new frame."""
        # Complete the nth frame.
        game_state = [
            {'ball_1_score': 1, 'ball_2_score': 2},
            {'ball_1_score': 3, 'ball_2_score': 4},
            {'ball_1_score': 5},
        ]
        b2 = BowlingGame(game_state=game_state)
        b2.add_ball_score(5)
        game = b2.get_game_state()
        self.assertEqual(len(game), 3)
        self.assertEqual(game[1]['next_frame'], game[2])

        # Add the nth frame.
        game_state = [
            {'ball_1_score': 1, 'ball_2_score': 2},
            {'ball_1_score': 3, 'ball_2_score': 4},
            {'ball_1_score': 5, 'ball_2_score': 6},
        ]
        b2 = BowlingGame(game_state=game_state)
        b2.add_ball_score(5)
        game = b2.get_game_state()
        self.assertEqual(len(game), 4)
        self.assertEqual(game[2]['next_frame'], game[3])


    def test_post_new_score(self):
        """It should add a ball score, update frame scores, and update running total scores."""
        for i in range(10):
            self.b.post_new_score(1)
        game = self.b.get_game_state()
        self.assertEqual(len(game), 5)
        self.assertEqual(game[1].get('frame_score'), 2)
        self.assertEqual(game[-1].get('running_total'), 10)


    def test_is_incomplete_frame(self):
        """It should indicate whether the frame is finished."""
        frame_1 = self.b.build_frame()
        frame_2 = self.b.build_frame(1)
        frame_3 = self.b.build_frame(1, 9)
        frame_4 = self.b.build_frame(10)
        self.assertTrue(self.b.is_incomplete_frame(frame_1))
        self.assertTrue(self.b.is_incomplete_frame(frame_2))
        self.assertFalse(self.b.is_incomplete_frame(frame_3))
        self.assertFalse(self.b.is_incomplete_frame(frame_4))


    def test_is_game_over(self):
        """It should indicate when the bowling game is over."""
        # Build a sample game state.
        game_state = []
        for i in range(9):
            frame = self.b.build_frame(1, 1)
            game_state.append(frame)

        # In a frame earlier than the last frame.
        b2 = BowlingGame(game_state=game_state)
        self.assertFalse(b2.is_game_over())

        # In the last frame, but the frame is incomplete.
        game_state.append(self.b.build_frame(1))
        b2 = BowlingGame(game_state=game_state)
        self.assertFalse(b2.is_game_over())

        # In the last frame, and there are no special balls.
        game_state.pop()
        game_state.append(self.b.build_frame(1, 1))
        b2 = BowlingGame(game_state=game_state)
        self.assertTrue(b2.is_game_over())

        # In the last frame, but there is a spare ball.
        game_state.pop()
        game_state.append(self.b.build_frame(1, 9))
        b2 = BowlingGame(game_state=game_state)
        self.assertFalse(b2.is_game_over())

        # In the last frame + 1 shot, and the last frame had a spare ball.
        game_state.append(self.b.build_frame(1))
        b2 = BowlingGame(game_state=game_state)
        self.assertTrue(b2.is_game_over())

        # In the last frame, but there is a strike ball.
        game_state.pop()
        game_state.pop()
        game_state.append(self.b.build_frame(10))
        b2 = BowlingGame(game_state=game_state)
        self.assertFalse(b2.is_game_over())

        # In the last frame + 1 shot, but the last shot had a strike ball.
        game_state.append(self.b.build_frame(1))
        b2 = BowlingGame(game_state=game_state)
        self.assertFalse(b2.is_game_over())

        # In the last frame + 2 shots, and the last shot had a strike ball.
        game_state.pop()
        game_state.append(self.b.build_frame(1, 1))
        b2 = BowlingGame(game_state=game_state)
        self.assertTrue(b2.is_game_over())

        # In the last frame + 1 shot, but this shot has a strike ball.
        game_state.pop()
        game_state.append(self.b.build_frame(10))
        b2 = BowlingGame(game_state=game_state)
        self.assertFalse(b2.is_game_over())

        # In the last frame + 2 shots, and the last shot had a strike ball.
        game_state.append(self.b.build_frame(1, 1))
        b2 = BowlingGame(game_state=game_state)
        self.assertTrue(b2.is_game_over())


if __name__ == '__main__':
    unittest.main()
