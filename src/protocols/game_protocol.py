from typing import List, Optional, Protocol, runtime_checkable

@runtime_checkable
class GameProtocol(Protocol):
    board: List[int]
    """The game board as a list of integers"""
    current_player: int
    """the player to move: 1 or -1"""

    def get_legal_moves(self) -> List[int]:
        """Returns a list of legal moves."""
        ...

    def get_game_state(self) -> List[int]:
        """Returns the current game state as a list."""
        ...

    def make_move(self, move: int) -> "GameProtocol":
        """Returns a new GameProtocol object after making the move."""
        ...

    def check_win(self) -> Optional[int]:
        """Returns 1 if player 1 wins, -1 if player -1 wins, 0 if draw, None if ongoing."""
        ...

    def is_game_over(self) -> bool:
        """Returns True if the game is over (win or draw), False otherwise."""
        ...
