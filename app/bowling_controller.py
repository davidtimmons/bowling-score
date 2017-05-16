#!/usr/bin/env python3

"""bowling_controller.py

Provides a class used to manage bowling game state for each player. Relies on the <BowlingGame>
class to provide scoring functionality.
"""

from .bowling_game import BowlingGame
from .helpers import read_only, restrict_bounds


class BowlingController(object):
    """Manage bowling game scores and state for all players."""


    def __init__(self, num_players=2, num_pins=10, num_frames=10, game_states=[]):
        """Create a bowling game scoring object for each player.

        Args:
            num_players: Integer representing the number of players in this game.
            num_pins: Integer representing the number of pins set up in each frame.
            num_frames: Integer representing the number of frames in this game.
            game_states: List that stores one BowlingGame objects for each player.
        """
        self.__num_players = num_players
        self.__num_pins = num_pins
        self.__num_frames = num_frames

        # Create bowling game objects for each player to track scores.
        if not game_states:
            for i in range(num_players):
                game_states.append(BowlingGame(num_pins, num_frames, []))

        self.__game_states = game_states
        self.__player_turn = 0 ## A pointer to the current player's bowling game object.


    ########################
    ### PUBLIC FUNCTIONS ###
    ########################

    def get_current_player(self):
        """Returns the one-indexed number representing the current player.

        Returns:
            Integer representing the current player.
        """
        return self.__player_turn + 1


    @restrict_bounds(1, lambda self: self.__num_players)
    def get_current_score(self, player):
        """Returns the current score for this player.

        Args:
            player: Integer representing the desired player (one-indexed).

        Returns:
            The latest score for this player.
        """
        games = self.__game_states
        player = player - 1 ## Shift the argument to be zero-indexed.
        frame = games[player].current_frame
        return games[player].get_frame_data(frame).get('running_total')


    def get_current_scores(self):
        """Returns the current score for all players.

        Returns:
            List of the latest scores for all players in order of player number.
        """
        data = []
        games = self.__game_states
        for p in range(self.__num_players):
            frame = games[p].current_frame
            data.append(games[p].get_frame_data(frame).get('running_total'))
        return data


    def get_frame_data(self, i, player):
        """Get a shallow copy of basic frame data associated with the ith frame for this player.

        Note that <BowlingGame> returns an empty dictionary for an out of bounds frame number.

        Args:
            i: Integer representing the desired frame number.
            player: Integer representing the desired player (one-indexed).

        Returns:
            Dictionary containing data from the ith frame.
        """
        if player < 1 or player > self.__num_players:
            return {}

        games = self.__game_states
        player = player - 1 ## Shift the argument to be zero-indexed.
        return games[player].get_frame_data(i)


    def get_frames(self, i):
        """Get ith frame data for all players.

        Note that <BowlingGame> returns an empty dictionary for an out of bounds frame number.

        Args:
            i: Integer representing the desired frame number.

        Returns:
            List of dictionary objects containing data from the ith frame in order by player.
        """
        data = []
        games = self.__game_states
        for p in range(self.__num_players):
            data.append(games[p].get_frame_data(i))
        return data


    @restrict_bounds(1, lambda self: self.__num_players)
    def get_game_state(self, player):
        """Returns a full, recursive copy of the game state for this player.

        Args:
            player: Integer representing the desired player (one-indexed).

        Returns:
            List of dictionary objects representing the state of each frame.
        """
        games = self.__game_states
        player = player - 1 ## Shift the argument to be zero-indexed.
        return games[player].get_game_state()


    def get_game_states(self):
        """Returns a full, recursive copy of the game state for all players.

        Returns:
            List of dictionary objects representing the state of each frame in order by player.
        """
        data = []
        games = self.__game_states
        for p in range(self.__num_players):
            data.append(games[p].get_game_state())
        return data


    @restrict_bounds(1, lambda self: self.__num_players)
    def is_game_over(self, player):
        """Determine whether the game is over for this player.

        Args:
            player: Integer representing the desired player (one-indexed).

        Returns:
            Boolean value representing whether the game should continue for this player.
        """
        games = self.__game_states
        player = player - 1 ## Shift the argument to be zero-indexed.
        return games[player].is_game_over()


    @restrict_bounds(0, lambda self: self.__num_pins)
    def post_new_score(self, score):
        """Add a new ball score, update scores for the current player, then switch to next player.

        Args:
            score: Integer representing the number of pins knocked down.
        """
        # Post the score.
        games = self.__game_states
        player = self.__player_turn
        games[player].post_new_score(score)

        # Switch to the next player if the frame is complete.
        if games[player].is_current_frame_complete():
            num_players = self.__num_players
            self.__player_turn = (player + 1) % num_players


if __name__ == '__main__':
    pass
