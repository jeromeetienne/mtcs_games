from abc import ABC, abstractmethod
from . game_base import GameBase
from typing import Any


class PlayerBase(ABC):
    """
    Abstract base class for any TicTacToe player (Human or AI).

    Subclasses are expected to provide the attributes `player_id` (int)
    and `marker` (str), and implement `get_move`.
    """

    # Concrete implementations should set these attributes in their __init__
    player_id: int
    marker: str

    @abstractmethod
    def get_move(self, game: GameBase) -> int:
        """Calculate and return the player's chosen move (index 0-8)."""
        raise NotImplementedError
