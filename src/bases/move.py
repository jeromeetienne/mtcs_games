from functools import total_ordering

@total_ordering
class Move():
    """
    class to represent a move in a game.
    Encodes the move as an integer index in a 1D array representing the board.
    """

    def __init__(self, index: int):
        self._index = index

    def __int__(self):
        """Return the integer index of the move."""
        return self._index
    
    def __str__(self) -> str:
        return f"{self._index}"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Move):
            return False
        return int(self) == int(other)

    def __lt__(self, other) -> bool:
        if not isinstance(other, Move):
            return NotImplemented
        return int(self) < int(other)