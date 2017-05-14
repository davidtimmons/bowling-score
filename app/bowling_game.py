"""bowling_game.py

xyz
"""

from .helpers import read_only


class BowlingGame(object):
    """TODO"""

    def __init__(self, num_pins=10, num_frames=10, game_state=[]):
        """Configure the bowling game.

        The game state consists of a linked list implemented using dictionary objects all enclosed
        within an outer list. This structure has two advantages: (1) Retrieve data from any desired
        frame in O(1) time, and (2) Use linked objects for extra clarity when calculating the
        forward score for special game outcomes including spare balls and strike balls.

        Args:
            num_pins: Integer representing the number of pins set up in each frame.
            num_frames: Integer representing the number of frames in this game.
            game_state: List that stores frame dictionary objects as the game progresses.
        """
        self.__num_pins = num_pins
        self.__num_frames = num_frames
        self.__game_state = game_state


    @read_only
    def NUM_PINS(self):
        return self.__num_pins


    @read_only
    def NUM_FRAMES(self):
        return self.__num_frames


    @read_only
    def current_frame(self):
        return len(self.__game_state)


    # TODO
    # add_ball_score =>
    #     is_complete_frame ? store_frames(link_frames(frame, build_frame())) : build_frame

    # TODO: Calculate running score, get scores from a particular frame (no > 10)

    # TODO: Add multiple players, REST-like API, README, master test file

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


    def calculate_forward_score(self, i):
        """Mutate a frame object from the game state to add a calculated frame score.

        Given a frame i, calculate the frame score starting up to two frames back in order to
        incorporate special scoring rules for spares and strikes. If the current game state
        is empty, do nothing. If there are not enough frames to calculate a spare or a strike
        and one exists in the calculated frame, do nothing.

        Args:
            i: Integer representing the one-indexed frame from which to calculate the frame score.
        """
        # There is nothing to do if the game has not started.
        if self.current_frame <= 0:
            return

        # Ensure n does not calculate a non-existant frame.
        n = i - 1 ## Shift i to be zero-indexed so it pulls the correct value from the game state.
        n = 0 if n - 2 <= 0 else n - 2 ## Calculate the score for up to two frames behind.
        frame_start = self.__game_state[n] or {}
        frame_next = frame_start.get('next_frame', {})
        frame_last = frame_next.get('next_frame', {})

        # Only proceed if this frame does not have an existing frame score.
        if not frame_start.get('frame_score'):

            # Extract relevant data from the frame objects for clarity.
            is_spare = frame_start.get('is_spare', False)
            is_strike = frame_start.get('is_strike', False)
            open_frame = not (is_spare or is_strike)

            ball_1_score = frame_start.get('ball_1_score', 0)
            ball_2_score = frame_start.get('ball_2_score', 0)
            ball_3_score = frame_next.get('ball_1_score', 0)
            ball_4_score = frame_next.get('ball_2_score', 0)
            ball_5_score = frame_last.get('ball_1_score', 0)

            score = ball_1_score + ball_2_score
            score_next = ball_3_score + ball_4_score

            # Calculate the frame score for one of these frames: i=1, i=2, i=i-2.
            if open_frame:
                frame_start.update(frame_score=score)
            elif is_spare and frame_next:
                frame_start.update(frame_score=score + ball_3_score)
            elif is_strike and frame_next:
                if frame_next.get('is_strike') and frame_last:
                    frame_start.update(frame_score=score + score_next + ball_5_score)
                else:
                    frame_start.update(frame_score=score + score_next)


    def build_frame(self, ball_1_score=None, ball_2_score=None):
        """Build a dictionary containing ball score data that describes this frame.

        Args:
            ball_1_score: Integer representing the number of pins knocked down on the first ball.
            ball_2_score: Integer representing the number of pins knocked down on the second ball.

        Raises:
            ValueError if the total score is greater than the number of pins in a frame.
            ValueError if there is a ball_2_score with no ball_1_score.

        Returns:
            Dictionary containing the data that describes this frame. Example:
            {'ball_1_score': 4, 'ball_2_score': 6, 'is_spare': True, 'is_strike': False}
        """
        # The total score should be less than the number of pins.
        if ball_1_score and ball_2_score and ball_1_score + ball_2_score > self.NUM_PINS:
            raise ValueError('The total frame score should be no more than {num} pins!' \
                .format(num=repr(self.NUM_PINS)))

        # The ball_2_score should only be given when there is a ball_1_score.
        elif ball_1_score is None and ball_2_score is not None:
            raise ValueError('The total frame score should be no more than {num} pins!' \
                .format(num=repr(self.NUM_PINS)))

        # Construct the frame dictionary object.
        frame = {}
        is_strike = False
        is_spare = False

        if ball_1_score:
            is_strike = ball_1_score == self.NUM_PINS
            frame.update(ball_1_score=ball_1_score)

        if ball_2_score:
            is_spare = ball_1_score < self.NUM_PINS and ball_1_score + ball_2_score == self.NUM_PINS
            frame.update(ball_2_score=ball_2_score)

        frame.update(is_spare=is_spare, is_strike=is_strike)
        return frame


    def link_frames(self, frame_1, frame_2=None):
        """Mutate a frame object to add a link to another frame object.

        Args:
            frame_1: Dictionary object representing the frame before frame_2.
            frame_2: Dictionary object representing the frame after frame_1.

        Returns:
            New frame_1 dictionary object linked to frame_2.
        """
        frame_1.update(next_frame=frame_2)
        return frame_1


    def is_incomplete_frame(self, frame):
        """Determine whether this frame has a remaining ball.

        Args:
            frame: Dictionary containing frame data; see <BowlingGame#build_frame>.

        Returns:
            Boolean value indicating whether the frame should continue.
        """
        if frame.get('ball_1_score') is None or frame.get('ball_2_score') is None:
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

        # Test the game state status.
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
