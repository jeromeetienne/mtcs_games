# stdlib imports
from typing import List, Optional
from abc import ABC, abstractmethod

# local imports
from .move import Move
from .types import PlayerID, GameResult

class BaseGame(ABC):
    board: List[int]
    """The game board as a list of integers"""
    current_player: PlayerID
    """the player to move: 1 or -1"""

    @abstractmethod
    def get_legal_moves(self) -> List[Move]:
        """Returns a list of legal moves."""
        pass

    @abstractmethod
    def copy(self) -> "BaseGame":
        """Returns a deep copy of the game."""
        pass

    @abstractmethod
    def make_move(self, move: Move) -> "BaseGame":
        """Returns a new GameBase object after making the move."""
        pass

    @abstractmethod
    def get_winner(self) -> GameResult | None:
        """Returns 1 if player 1 wins, -1 if player -1 wins, 0 if draw, None if ongoing."""
        pass

    def is_game_over(self) -> bool:
        """Returns True if the game is over (win or draw), else False."""
        return self.get_winner() is not None
