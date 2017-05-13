"""bowling_game.py

xyz
"""

from .helpers import constant


class BowlingGame(object):
    """TODO"""
    # TODO: Add function/constant list?

    def __init__(self, num_pins=10, num_frames=10, num_players=2):
        """Configure the bowling game.

        Args:
            max_pins: Integer representing the max pins set up in each frame.
            num_frames: Integer representing the max frames in this game.
        """
        self.__num_pins = num_pins
        self.__num_frames = num_frames
        self.__game_state = [] ## Stores frame dictionary objects as the game progresses.
        self.__temp_state = [] ## Temporary storage for frame objects before moving to game_state.


    @constant
    def NUM_PINS(self):
        return self.__num_pins


    @constant
    def NUM_FRAMES(self):
        return self.__num_frames


    @constant
    def NUM_PLAYERS(self):
        return self.__num_players

        
    # TODO
    # add_ball_score => get_temp_frames =>
    #     is_complete_frame ? store_frames(link_frames(frame, build_frame())) : build_frame

    # TODO: Store temp frames, crunch frames, add frames to game state, calculate scores

    # TODO: Add multiple players, REST API, documentation.

    def add_ball_score(self, frame, score):
        """TODO"""
        if self.is_game_over():
            pass
        elif self.is_complete_frame(frame):
            frame_2 = self.build_frame(score)
            self.link_frames(frame, frame_2)
        else:
            ball_1_score = frame.get('ball_1_score', -1)
            ball_2_score = frame.get('ball_2_score', -1)
            self.build_frame(ball_1_score, ball_2_score)


    def build_frame(self, ball_1_score=-1, ball_2_score=-1, next_frame=None):
        """Build a dictionary containing all the data that describes this frame.

        Args:
            ball_1_score: Integer representing the number of pins knocked down on the first ball.
            ball_2_score: Integer representing the number of pins knocked down on the second ball.
            next_frame: Reference to the next frame object.

        Returns:
            Dictionary containing the data that describes this frame.
        """

        return {
            'ball_1_score': ball_1_score,
            'ball_2_score': ball_2_score,
            'next_frame': next_frame,
            'is_spare': ball_1_score != self.NUM_PINS and
                ball_1_score + ball_2_score == self.NUM_PINS,
            'is_strike': ball_1_score == self.NUM_PINS,
        }


    def link_frames(self, frame_1, frame_2=None):
        """Link two frame dictionaries.

        Args:
            frame_1: Dictionary object representing the frame before frame_2.
            frame_2: Dictionary object representing the frame after frame_1.

        Returns:
            New frame_1 dictionary object linked to frame_2.
        """

        return self.build_frame( frame_1.get('ball_1_score', -1) \
                               , frame_1.get('ball_2_score', -1) \
                               , frame_2 )


    def calculate_frame_score(self, frame):
        """TODO"""
        frame_score = ball_1_score + ball_2_score

        if next_frame:
            if is_spare:
                frame_score = frame_score + next_frame.get('ball_1_score', 0)
            if is_strike:
                frame_score = frame_score + next_frame.get('ball_2_score', 0)
                if next_frame.get('is_strike', False):
                    next_next_frame = next_frame.get('next_frame', None)
                    if next_next_frame:
                        frame_score = frame_score + next_next_frame.get('ball_1_score', 0)


    def is_incomplete_frame(self, frame):
        """Determine whether this frame has a remaining ball.

        Args:
            frame: Dictionary containing frame data; see <BowlingGame#build_frame>.

        Returns:
            Boolean value indicating whether the frame should continue.
        """
        if frame.get('ball_1_score', -1) < 0 or frame.get('ball_2_score', -1) < 0:
            return True
        return False


    def is_game_over(self, _game_state=[]):
        """Determine whether the game is over.

        Args:
            _game_state: Private list data used to override game state and test this function.

        Returns:
            Boolean value representing whether the game should continue.
        """

        # Create easy references to the appropriate data.
        _game_state = _game_state or self.__game_state
        frame = _game_state[-1]
        prev_frame = _game_state[-2]
        frame_count = len(_game_state)

        # Test the game state.
        if frame_count < self.NUM_FRAMES:
            return False ## The game is not in the last frame.

        elif frame_count == self.NUM_FRAMES and self.is_incomplete_frame(frame):
            return False ## The last frame is incomplete.

        elif frame_count == self.NUM_FRAMES and \
            (frame.get('is_spare', False) or frame.get('is_strike', False)):
                return False ## The tenth frame gets bonus ball(s).

        elif frame_count == self.NUM_FRAMES + 1:
            if prev_frame.get('is_spare', False) and frame.get('ball_1_score', -1) < 0:
                return False ## There is one final spare ball.
            elif prev_frame.get('is_strike', False) and frame.get('ball_2_score', -1) < 0:
                return False ## There is another strike ball.

        elif frame_count == self.NUM_FRAMES + 2 and frame.get('ball_1_score', -1) < 0:
            return False ## There is one final strike ball.

        return True


if __name__ == '__main__':
    pass
