# stdlib imports
from typing import List, Optional
from abc import ABC, abstractmethod

# local imports
from .move import Move

class GameBase(ABC):
    board: List[int]
    """The game board as a list of integers"""
    current_player: int
    """the player to move: 1 or -1"""

    @abstractmethod
    def get_legal_moves(self) -> List[Move]:
        """Returns a list of legal moves."""
        pass

    @abstractmethod
    def copy(self) -> "GameBase":
        """Returns a deep copy of the game."""
        pass

    @abstractmethod
    def make_move(self, move: Move) -> "GameBase":
        """Returns a new GameBase object after making the move."""
        pass

    @abstractmethod
    def check_win(self) -> Optional[int]:
        """Returns 1 if player 1 wins, -1 if player -1 wins, 0 if draw, None if ongoing."""
        pass

    @abstractmethod
    def is_game_over(self) -> bool:
        """Returns True if the game is over (win or draw), False otherwise."""
        pass
