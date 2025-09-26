# stdlib imports
from typing import List, Optional

# pip imports
import colorama

# local imports
from src.protocols.game_protocol import GameProtocol


class GameConnect4(GameProtocol):
    """
    Represents the state and rules of a Connect 4 game.
    """
    def __init__(self, rows: int = 6, cols: int = 7) -> None:
        self.rows: int = rows
        self.cols: int = cols
        # The board is a flattened list for easy representation,
        # where 0=Empty, 1='X' (Player 1), -1='O' (Player -1)
        self.board: List[int] = [0] * (rows * cols)
        # 1: 'X', -1: 'O'
        self.current_player: int = 1

    def __repr__(self) -> str:
        """Prints a human-readable board representation, showing move indices on empty cells."""
        output: str = ""
        output += "   ".join([str(j) for j in range(self.cols)]) + "\n"  # Column indices
        for row_index in range(self.rows):
            row = self.board[row_index * self.cols : (row_index + 1) * self.cols]
            row_symbols = []
            for col_index, cell in enumerate(row):
                if cell == 1:
                    symbol = colorama.Fore.GREEN + "X" + colorama.Style.RESET_ALL
                elif cell == -1:
                    symbol = colorama.Fore.RED + "O" + colorama.Style.RESET_ALL
                else:
                    symbol = " "
                row_symbols.append(symbol)
            output += " | ".join(row_symbols)
            output += "\n"
            if row_index < self.rows - 1:
                output += "--" + "+---" * (self.cols - 1) + "\n"
        return output

    def get_legal_moves(self) -> List[int]:
        """Returns a list of column indices (0 to cols-1) where moves can be made."""
        legal_moves = []
        for col in range(self.cols):
            if self.board[col] == 0:  # If the top cell of the column is empty
                legal_moves.append(col)
        return legal_moves
    
    def get_game_state(self) -> List[int]:
        """Returns the current game state as a list."""
        return list(self.board)
    
    def copy(self) -> "GameConnect4":
        """Returns a deep copy of the current game state."""
        new_game = GameConnect4(self.rows, self.cols)
        new_game.board = list(self.board)  # Deep copy the board
        new_game.current_player = self.current_player
        return new_game

    def make_move(self, move: int) -> "GameConnect4":
        """
        Creates and returns a new Connect4 object after making the move.
        Assumes the move is valid (i.e., the column is not full).
        """
        if move < 0 or move >= self.cols or self.board[move] != 0:
            raise ValueError("Invalid move attempted on a full or out-of-bounds column.")

        # Create a new game state
        new_game = self.copy()
        
        # Play the move in the lowest available row in the specified column
        for row in range(self.rows - 1, -1, -1):
            square_idx = row * self.cols + move
            if new_game.board[square_idx] == 0:
                new_game.board[square_idx] = self.current_player
                break

        # Switch player
        new_game.current_player = -self.current_player  
        return new_game
    
    def check_win(self) -> Optional[int]:
        """
        Checks for a win. Returns 1 if 'X' wins, -1 if 'O' wins, 0 if no winner,
        and None if the game is still ongoing.
        """
        # Check horizontal, vertical, and diagonal (both directions) for a connect 4
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # right, down, down-right, down-left
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row * self.cols + col] == 0:
                    continue
                player = self.board[row * self.cols + col]
                for dr, dc in directions:
                    count = 0
                    r, c = row, col
                    while 0 <= r < self.rows and 0 <= c < self.cols and self.board[r * self.cols + c] == player:
                        count += 1
                        if count == 4:
                            return player
                        r += dr
                        c += dc
        
        if all(cell != 0 for cell in self.board):
            return 0  # Draw
        
        return None  # Game is still ongoing
    
    def is_game_over(self) -> bool:
        """Returns True if the game is over (win or draw), else False."""
        return self.check_win() is not None
    
if __name__ == "__main__":
    game = GameConnect4()
    print(game)
    game = game.make_move(3)
    print(game)
    game = game.make_move(3)
    print(game)
    game = game.make_move(2)
    print(game)
    game = game.make_move(2)
    print(game)
    game = game.make_move(1)
    print(game)
    game = game.make_move(1)
    print(game)
    game = game.make_move(0)
    print(game)
    print("Winner:", game.check_win())