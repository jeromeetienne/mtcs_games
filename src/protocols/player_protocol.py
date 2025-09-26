from ..games.game_tictactoe import GameTicTacToe
from typing import List, Optional, Protocol, runtime_checkable
from ..protocols.game_protocol import GameProtocol

@runtime_checkable
class PlayerProtocol(Protocol):
    """
    Protocol/Interface for any TicTacToe player (Human or AI).
    A player must have a player_id (1 or -1) and a get_move method.
    """

    player_id: int
    """1 for player 1 (X), -1 for player 2 (O)"""

    marker: str
    """'X' for player 1 (X), 'O' for player 2 (O)"""

    def get_move(self, game: GameProtocol) -> int:
        """
        Calculates and returns the player's chosen move (index 0-8).
        """
        ...
