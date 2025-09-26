
# define a type Square as an integer
class SquareProtocol:
    def __int__(self) -> int:
        ...

    def copy(self) -> "SquareProtocol":
        ...

    def to_string(self) -> str:
        ...

    @classmethod
    def from_int(cls, square_index: int) -> "SquareProtocol":
        ...

class Square(SquareProtocol):
    def __init__(self, square_index: int):
        self.__square_index = square_index

    def __int__(self) -> int:
        return self.__square_index
    
    def copy(self) -> "Square":
        return Square(self.__square_index)

    def to_string(self) -> str:
        return str(self.__square_index)

    @classmethod
    def from_int(cls, square_index: int) -> "Square":
        return Square(square_index)

###############################################################################
#   Move Protocol
#
class MoveProtocol:
    def __int__(self) -> int:
        ...

    def copy(self) -> "MoveProtocol":
        ...

    def to_string(self) -> str:
        ...

    @classmethod
    def from_string(cls, value: str) -> "MoveProtocol":
        ...

class Move1sqr(MoveProtocol):
    def __init__(self, square: SquareProtocol):
        self.__square = square

    def __int__(self) -> int:
        return int(self.__square)
    
    def copy(self) -> "Move1sqr":
        return Move1sqr(self.__square.copy())
    
    def to_string(self) -> str:
        return str(int(self.__square))

    @classmethod
    def from_int(cls, value: int) -> "Move1sqr":
        square = Square(value)
        return Move1sqr(square)
    
    @classmethod
    def from_string(cls, value: str) -> "Move1sqr":
        square = Square(int(value))
        return Move1sqr(square)

class Move2sqr(MoveProtocol):
    def __init__(self, square_from: Square, square_to: Square):
        self.__square_from = square_from
        self.__square_to = square_to

    def __int__(self) -> int:
        encoded_move = int(self.__square_from) * 100 + int(self.__square_to)
        return encoded_move
    
    def copy(self) -> "Move2sqr":
        return Move2sqr(self.__square_from.copy(), self.__square_to.copy())

    def to_string(self) -> str:
        return f"{int(self.__square_from)},{int(self.__square_to)}"

    # allow conversion from int to Move2sqr
    @classmethod
    def from_int(cls, encoded_move: int) -> "Move2sqr":
        square_from = Square(encoded_move // 100)
        square_to = Square(encoded_move % 100)
        return Move2sqr(square_from, square_to)
    
    @classmethod
    def from_string(cls, value: str) -> "Move2sqr":
        parts = value.split(',')
        if len(parts) != 2:
            raise ValueError("Invalid move string format. Expected 'from,to'.")
        square_from = Square(int(parts[0]))
        square_to = Square(int(parts[1]))
        return Move2sqr(square_from, square_to)

class PieceProtocol:
    def __int__(self) -> int:
        ...

    def copy(self) -> "PieceProtocol":
        ...

    def to_string(self) -> str:
        ...        
    
    


###############################################################################
#   Validation functions (for demonstration purposes)
#
def is_valid_square(square: int) -> bool:
    print(f"Validating square: {square}")
    return True

if __name__ == "__main__":
    test_square = Square(5)
    print(f"Is {test_square} a valid square? {is_valid_square(int(test_square))}")

    move = Move1sqr(test_square)

    print(f"Created move with square: {int(move)}")

    move = Move2sqr(Square(3), Square(7))
    print(f"Created move with from-to squares: {int(move)}")
