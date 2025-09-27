# stdlib imports
from functools import total_ordering

@total_ordering
class Move():
    """
    class to represent a move in a game.
    Encodes the move as an integer index in a 1D array representing the board.
    """

    def __init__(self, move_idx: int):
        self._index: int = move_idx

    def __int__(self) -> int:
        """Return the integer index of the move."""
        return self._index
    
    def __str__(self) -> str:
        return f"{self._index}"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Move):
            return False
        return int(self) == int(other)

    def __lt__(self, other) -> bool:
        """
        Define less-than for ordering moves.
        This allows moves to be sorted or compared.

        It leverages @total_ordering to fill in the other comparison methods.
        """
        if not isinstance(other, Move):
            return NotImplemented
        return int(self) < int(other)