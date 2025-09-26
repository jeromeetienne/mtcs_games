
# define a type Square as an integer
class SquareProtocol:
    def __int__(self) -> int:
        ...

class Square(SquareProtocol):
    def __init__(self, square_index: int):
        self.square_index = square_index

    def __int__(self) -> int:
        return self.square_index


class MoveProtocol:
    def __int__(self) -> int:
        ...

class Move1sqr(MoveProtocol):
    def __init__(self, square: Square):
        self.square = square

    def __int__(self) -> int:
        return self.square.square_index
    
    @classmethod
    def from_int(cls, value: int) -> "Move1sqr":
        square = Square(value)
        return cls(square)

class Move2sqr(MoveProtocol):
    def __init__(self, square_from: Square, square_to: Square):
        self.square_from = square_from
        self.square_to = square_to

    def __int__(self) -> int:
        return self.square_from.square_index * 100 + self.square_to.square_index

    # allow conversion from int to Move2sqr
    @classmethod
    def from_int(cls, value: int) -> "Move2sqr":
        square_from = Square(value // 100)
        square_to = Square(value % 100)
        return cls(square_from, square_to)


###############################################################################
#   Validation functions (for demonstration purposes)
#
def is_valid_square(square: SquareProtocol) -> bool:
    print(f"Validating square: {square}")
    return True

if __name__ == "__main__":
    test_square = Square(5)
    print(f"Is {test_square} a valid square? {is_valid_square(test_square)}")

    move = Move1sqr(test_square)

    print(f"Created move with square: {int(move)}")