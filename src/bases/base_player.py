# stdlib imports
from abc import ABC, abstractmethod
from typing import Any

# local imports
from .move import Move
from .base_game import BaseGame


class BasePlayer(ABC):
    """
    Abstract base class for any TicTacToe player (Human or AI).

    Subclasses are expected to provide the attributes `player_id` (int)
    and `marker` (str), and implement `get_move`.
    """

    # Concrete implementations should set these attributes in their __init__
    player_id: int
    marker: str

    def __init__(self, player_id: int):
        self.player_id = player_id
        self.marker = 'X' if player_id == 1 else 'O'

    @abstractmethod
    def get_move(self, game: BaseGame) -> Move:
        """Calculate and return the player's chosen move (index 0-8)."""
        raise NotImplementedError

    @abstractmethod
    def copy(self) -> 'BasePlayer':
        """Create and return a copy of this player instance."""
        raise NotImplementedError

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.marker})"
