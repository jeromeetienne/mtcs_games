from abc import ABC

class SquareBase(ABC):
	"""
	Abstract base class for a square in a board game.
	Encodes the location of the square as an integer index in a 1D array representing the board.
	Does not encode its content.
	"""

	def __init__(self, index: int):
		self._index = index

	def __int__(self):
		"""Return the integer index of the square."""
		return self._index

