from abc import ABC, abstractmethod

from .square_base import SquareBase


class MoveBase(ABC):
    """
    Abstract base class for a move in a board game.
    Encodes the move as an integer index in a 1D array representing possible moves.
    Does not encode move content or result.
    """

    def __init__(self, index: int):
        self._index = index

    def __int__(self):
        """Return the integer index of the move."""
        return self._index
    
    @abstractmethod
    def __str__(self) -> str:
        """Return a string representation of the move."""
        pass

    @staticmethod
    @abstractmethod
    def from_string(move_str: str) -> "MoveBase":
        """Create a MoveBase object from a string representation."""
        pass


class MoveOneSqr(MoveBase):
    """
    Move for games where a move is defined by a single square (e.g., Othello, TicTacToe).
    """

    def __init__(self, square: "SquareBase"):
        super().__init__(int(square))
        self._square = square

    def __str__(self):
        return f"{int(self._square)}"

    @staticmethod
    def from_string(move_str: str) -> "MoveOneSqr":
        """Create a MoveOneSqr from a string representation of the square index."""
        square_index = int(move_str)
        square = SquareBase(square_index)
        return MoveOneSqr(square)

class MoveTwoSqr(MoveBase):
    """
    Move for games where a move is defined by two squares (e.g., Chess: from_square to to_square).
    """

    def __init__(self, from_square: "SquareBase", to_square: "SquareBase", board_size: int = 1000):
        self._from_square = from_square
        self._to_square = to_square
        # Encode the move as a unique int: from_index * board_size + to_index
        move_index = int(from_square) * board_size + int(to_square)
        super().__init__(move_index)

    def __str__(self):
        return f"{int(self._from_square)},{int(self._to_square)}"

    @staticmethod
    def from_string(move_str: str, board_size: int = 1000) -> "MoveTwoSqr":
        """Create a MoveTwoSqr from a string representation 'from_index,to_index'."""
        from_index, to_index = map(int, move_str.split(","))
        from_square = SquareBase(from_index)
        to_square = SquareBase(to_index)
        return MoveTwoSqr(from_square, to_square, board_size)