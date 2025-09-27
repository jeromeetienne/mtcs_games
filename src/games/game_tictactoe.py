# stdlib imports
import random
from typing import List, Optional

# pip imports
import colorama

# local imports
from src.bases.game_base import GameBase
from src.bases.move import Move



# --- TicTacToe Class (Unchanged) ---
class GameTicTacToe(GameBase):
    """
    Represents the state and rules of a Tic-Tac-Toe game. 
    """
    def __init__(self, size: int = 3) -> None:
        self.size: int = size
        # The board is a flattened list for easy representation,
        # where 0=Empty, 1='X' (Player 1), -1='O' (Player -1)
        self.board: List[int] = [0] * (size * size)
        # 1: 'X', -1: 'O'
        self.current_player: int = 1

    def __repr__(self) -> str:
        """Prints a human-readable board representation, showing move indices on empty cells."""
        output: str = ""
        for row_index in range(self.size):
            row = self.board[row_index * self.size : (row_index + 1) * self.size]
            row_display = []
            for col_index, cell in enumerate(row):
                if cell == 1:
                    row_display.append(colorama.Fore.GREEN +"X" + colorama.Style.RESET_ALL)
                elif cell == -1:
                    row_display.append(colorama.Fore.RED +"O" + colorama.Style.RESET_ALL)
                else:
                    square_index = row_index * self.size + col_index
                    row_display.append(str(square_index))
            output += " | ".join(row_display)
            output += "\n"
            if row_index < self.size - 1:
                output += "--" + "+---" * (self.size - 1) + "\n"
        return output

    def get_legal_moves(self) -> List[Move]:
        """Returns a list of indices (0-8) where moves can be made."""
        return [Move(i) for i, cell in enumerate(self.board) if cell == 0]
    
    def copy(self) -> "GameTicTacToe":
        """Returns a deep copy of the current game state."""
        new_game = GameTicTacToe(self.size)
        new_game.board = list(self.board)  # Deep copy the board
        new_game.current_player = self.current_player
        return new_game

    def make_move(self, move: Move) -> "GameTicTacToe":
        """
        Creates and returns a new TicTacToe object after making the move.
        Assumes the move is valid.
        """
        move_idx = int(move)
        if self.board[move_idx] != 0:
            raise ValueError("Invalid move attempted on a non-empty cell.")
            
        # Create a new game state
        new_game = self.copy()
        # Play the move
        new_game.board[move_idx] = self.current_player
        # Switch player
        new_game.current_player = -self.current_player  
        return new_game

    def check_win(self) -> Optional[int]:
        """
        Checks for a win. Returns 1 if 'X' wins, -1 if 'O' wins, 0 if no winner,
        and None if the game is still ongoing.
        """
        
        # Check rows, columns, and diagonals
        lines: List[List[int]] = []
        # Rows
        for i in range(self.size):
            lines.append(self.board[i * self.size : (i + 1) * self.size])
        # Columns
        for i in range(self.size):
            lines.append(self.board[i::self.size])
        # Diagonals (Specific logic for 3x3, but robust for the standard case)
        diag1 = self.board[::self.size + 1]
        diag2 = self.board[self.size - 1: self.size * self.size - 1: self.size - 1]
            
        lines.append(diag1)
        lines.append(diag2)
        
        for line in lines:
            if sum(line) == self.size:
                return 1  # 'X' wins
            if sum(line) == -self.size:
                return -1 # 'O' wins

        # Check for draw (if no moves left)
        if not self.get_legal_moves():
            return 0  # Draw

        return None # Game is still ongoing

    def is_game_over(self) -> bool:
        """True if there's a winner or a draw."""
        return self.check_win() is not None

###############################################################################
#   --- Example Usage (Unchanged) ---
#
if __name__ == "__main__":
    game = GameTicTacToe()
    print("Initial Game State:")
    print(game)
    while not game.is_game_over():
        legal_moves = game.get_legal_moves()
        move = random.choice(legal_moves)
        game = game.make_move(move)
        print(f"Player {'X' if game.current_player == -1 else 'O'} made move at index {move}")
        print(game)
    
    result = game.check_win()
    if result == 1:
        print("Player X wins!")
    elif result == -1:
        print("Player O wins!")
    else:
        print("It's a draw!")