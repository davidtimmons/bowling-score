"""bowling_game.py

Provides a low-level class used to manage bowling game state. Do not use this directly for
managing a bowling scoring service. Instead, use the <bowling_controller.py> module.
"""

import copy
from .helpers import read_only, restrict_bounds


class BowlingGame(object):
    """Manage bowling game scores and state.

    The game state consists of a linked list implemented using dictionary objects all enclosed
    within an outer list. This structure has two advantages: (1) Retrieve data from any desired
    frame in O(1) time, and (2) Use linked objects for extra clarity when calculating the
    forward score for special game outcomes including spare balls and strike balls.

    Example:
        state = [
            {'ball_1_score': 4, 'ball_2_score': 6, 'is_spare': True, 'is_strike': False,
                'next_frame': <object reference>, 'frame_score': 20, 'running_total': 20},
            {'ball_1_score': 10, 'ball_2_score': 0, 'is_spare': False, 'is_strike': True,
                'next_frame': <object reference>, 'frame_score': 13, 'running_total': 33},
            {'ball_1_score': 1, 'ball_2_score': 2, 'is_spare': False, 'is_strike': False,
                'next_frame': <object reference>, 'frame_score': 3, 'running_total': 36},
            {'ball_1_score': 2, 'is_spare': False, 'is_strike': False, 'running_total': 36}
        ]
    """


    def __init__(self, num_pins=10, num_frames=10, game_state=[]):
        """Configure the bowling game.

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
        """Returns the total number of frame pins in this bowling game."""
        return self.__num_pins


    @read_only
    def NUM_FRAMES(self):
        """Returns the total number of frames in this bowling game."""
        return self.__num_frames


    @read_only
    def current_frame(self):
        """Returns the current frame, always between 0 and <NUM_FRAMES>."""
        game_len = len(self.__game_state) ## Zero indicates the game has not started.
        return game_len if game_len <= self.NUM_FRAMES else self.NUM_FRAMES


    ##########################
    ### INTERNAL FUNCTIONS ###
    ##########################

    def add_ball_score(self, score):
        """Add a new ball score to the game and link frame objects when appropriate.

        Args:
            score: Integer representing the number of pins knocked down.
        """
        # Only proceed if this game is still in progress.
        if self.is_game_over():
            return

        game = self.__game_state
        game_len = len(game)
        frame_prev = frame = frame_next = {}

        # This is the first ball in the game.
        if game_len == 0:
            game.append(self.build_frame(score))
            return

        # This may be frame 1, so a previous frame may not exist.
        if game_len == 1:
            frame = game[0]
            if self.is_frame_incomplete(frame):
                game[0] = self.build_frame(frame.get('ball_1_score', 0), score)
            else:
                frame_next = self.build_frame(score)
                self.link_frames(frame, frame_next)
                game.append(frame_next)
            return

        # This is frame 2+, so link the previous frame then append the new score.
        frame_prev = game[-2]
        frame = game[-1]

        if self.is_frame_incomplete(frame):
            frame = self.build_frame(frame.get('ball_1_score', 0), score)
            self.link_frames(frame_prev, frame)
            game[-1] = frame

        else:
            frame_next = self.build_frame(score)
            self.link_frames(frame, frame_next)
            game.append(frame_next)


    def build_frame(self, ball_1_score=None, ball_2_score=None):
        """Build a dictionary containing ball score data that describes this frame.

        Args:
            ball_1_score: Integer representing the number of pins knocked down on the first ball.
            ball_2_score: Integer representing the number of pins knocked down on the second ball.

        Raises:
            ValueError if a ball score is less than 0 or greater than <NUM_PINS>.
            ValueError if the total score is greater than <NUM_PINS>.
            ValueError if there is a ball_2_score with no ball_1_score.

        Returns:
            Dictionary containing the data that describes this frame. Example:
            {'ball_1_score': 4, 'ball_2_score': 6, 'is_spare': True, 'is_strike': False}
        """
        # The score should represent an appropriate number of pins knocked down.
        if ball_1_score is not None and (ball_1_score < 0 or ball_1_score > self.NUM_PINS):
            raise ValueError('The ball 1 score should between 0 and {num} pins!' \
                .format(num=repr(self.NUM_PINS)))

        elif ball_2_score is not None and (ball_2_score < 0 or ball_2_score > self.NUM_PINS):
            raise ValueError('The ball 2 score should between 0 and {num} pins!' \
                .format(num=repr(self.NUM_PINS)))

        elif ball_1_score is not None and ball_2_score is not None and \
            ball_1_score + ball_2_score > self.NUM_PINS:
            raise ValueError('The total frame score should be no more than {num} pins!' \
                .format(num=repr(self.NUM_PINS)))

        # The ball_2_score should only be given when there is a ball_1_score.
        elif ball_1_score is None and ball_2_score is not None:
            raise ValueError('The ball 1 score should be given with the ball 2 score!')

        # Construct the frame dictionary object.
        frame = {}
        is_strike = False
        is_spare = False

        if ball_1_score is not None:
            is_strike = ball_1_score == self.NUM_PINS
            frame.update(ball_1_score=ball_1_score)
            if is_strike: frame.update(ball_2_score=0)

        if ball_2_score is not None:
            is_spare = ball_1_score < self.NUM_PINS and ball_1_score + ball_2_score == self.NUM_PINS
            frame.update(ball_2_score=ball_2_score)

        frame.update(is_spare=is_spare, is_strike=is_strike)
        return frame


    def calculate_forward_score(self, i):
        """Mutate a frame object from the game state to add a calculated <frame_score> key-value.

        Given a frame i, calculate the frame score starting up to two frames back in order to
        incorporate special scoring rules for spares and strikes. Adds the 'frame_score' key upon
        a successful frame calculation. If the current game state is empty, do nothing. If there
        are not enough frames to calculate a spare or a strike and one exists in the calculated
        frame, do nothing.

        Args:
            i: Integer representing the one-indexed frame from which to calculate the frame score.
        """
        # There is nothing to do if the game has not started.
        if self.current_frame <= 0:
            return

        # Ensure n does not calculate a non-existant frame.
        n = i - 1 ## Shift i to be zero-indexed so it pulls the correct value from the game state.
        n = 0 if n - 2 <= 0 else n - 2 ## Calculate the score for up to two frames behind.

        # Get frame data and completion status.
        frame_start = self.__game_state[n] or {}
        frame_next = frame_start.get('next_frame', {})
        frame_last = frame_next.get('next_frame', {})

        frame_is_complete = not self.is_frame_incomplete(frame_start)
        frame_next_is_complete = not self.is_frame_incomplete(frame_next)
        frame_last_is_complete = not self.is_frame_incomplete(frame_last)

        # Get special balls and scores.
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

        # Calculate frame score for one of these frames: i=1, i=2, i=i-2.
        if frame_is_complete:
            if open_frame:
                frame_start.update(frame_score=score)
            elif is_spare and frame_next:
                frame_start.update(frame_score=score + ball_3_score)
            elif is_strike and frame_next_is_complete:
                if frame_next.get('is_strike') and frame_last:
                    frame_start.update(frame_score=score + score_next + ball_5_score)
                elif not frame_next.get('is_strike'):
                    frame_start.update(frame_score=score + score_next)


    def calculate_frame_scores(self):
        """Mutate up to three frame objects from the game state to add the <frame_score> key-value.
        """
        for i in range(3):
            self.calculate_forward_score(self.current_frame + i)


    def calculate_running_total(self):
        """Mutate up to <NUM_FRAMES> fame objects to add the <running_total> key-value.
        """
        for i in range(len(self.__game_state)):
            frame_prev = self.__game_state[i-1] or {}
            running_total_prev = frame_prev.get('running_total', 0)

            frame = self.__game_state[i]
            frame_score = frame.get('frame_score', 0)

            frame.update(running_total=running_total_prev + frame_score)


    def is_frame_incomplete(self, frame):
        """Determine whether this frame has a remaining ball.

        Args:
            frame: Dictionary containing frame data with ball_1_score and ball_2_score keys.

        Returns:
            Boolean value indicating whether the frame is incomplete.
        """
        ball_1_score = frame.get('ball_1_score')
        ball_2_score = frame.get('ball_2_score')

        # A ball has not been recorded and/or this is not a strike.
        if ball_1_score is None or (ball_1_score < self.NUM_PINS and ball_2_score is None):
            return True

        return False


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


    ########################
    ### PUBLIC FUNCTIONS ###
    ########################

    def get_frame_data(self, i):
        """Get a shallow copy of basic frame data associated with the ith frame.

        Args:
            i: Integer representing the desired frame number.

        Returns:
            Dictionary containing data from the ith frame without the next frame link.
        """
        # Return an empty dictionary for invalid frame requests.
        if i <= 0 or i > self.current_frame:
            return {}

        # Create a shallow copy of the frame to avoid recursively copying the linked objects.
        frame = copy.copy(self.__game_state[i-1])
        if 'next_frame' in frame:
            del frame['next_frame']

        # Return the basic frame data.
        return frame


    def get_game_state(self):
        """Returns a full, recursive copy of the game state.

        Returns:
            List of dictionary objects representing the state of each frame.
        """
        return copy.deepcopy(self.__game_state)


    def is_current_frame_complete(self):
        """Determine whether the current frame has ended.

        Returns:
            Boolean value representing whether the frame has ended.
        """
        return not self.is_frame_incomplete(self.get_frame_data(self.current_frame))


    def is_game_over(self):
        """Determine whether the game is over.

        Returns:
            Boolean value representing whether the game should continue.
        """
        game = self.__game_state

        if len(game) < self.NUM_FRAMES:
            return False ## The game is not in the last frame.

        prev_frame = game[-2]
        frame = game[-1]
        frame_count = len(game)

        # Test the game status at the last frame and beyond.
        if frame_count == self.NUM_FRAMES and self.is_frame_incomplete(frame):
            return False ## The last frame is incomplete.

        # The last frame gets bonus ball(s).
        elif frame_count == self.NUM_FRAMES and (frame.get('is_spare') or frame.get('is_strike')):
            return False

        # There is another bonus ball.
        elif frame_count == self.NUM_FRAMES + 1 and \
            ((prev_frame.get('is_spare') and frame.get('ball_1_score') is None) or \
            (prev_frame.get('is_strike') and frame.get('ball_2_score') is None) or \
            frame.get('is_strike')):
            return False

        # There is one final strike ball.
        elif frame_count == self.NUM_FRAMES + 2 and \
            (prev_frame.get('is_strike') and frame.get('ball_1_score') is None):
            return False

        return True


    @restrict_bounds(0, lambda self: self.__num_pins)
    def post_new_score(self, score):
        """Add a new ball score, update frame scores, then update the running total scores.

        Args:
            score: Integer representing the number of pins knocked down between [0, NUM_PINS].
        """
        self.add_ball_score(score)
        self.calculate_frame_scores()
        self.calculate_running_total()


if __name__ == '__main__':
    pass
