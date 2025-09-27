# stdlib imports
from typing import List, Optional

# pip imports
import colorama

# local imports
from src.bases.game_base import GameBase



class GameOthello(GameBase):
    """
    Represents the state and rules of an Othello game.
    """
    def __init__(self, size: int = 8) -> None:
        self.size: int = size
        # The board is a flattened list for easy representation,
        # where 0=Empty, 1='X' (Player 1), -1='O' (Player -1)
        self.board: List[int] = [0] * (size * size)
        # Initialize the starting position
        mid = size // 2
        self.board[(mid - 1) * size + (mid - 1)] = -1
        self.board[(mid - 1) * size + mid] = 1
        self.board[mid * size + (mid - 1)] = 1
        self.board[mid * size + mid] = -1
        # 1: 'X', -1: 'O'
        self.current_player: int = 1

    def __repr__(self) -> str:
        """Prints a human-readable board representation, showing move indices on empty cells which are legal moves."""
        output: str = ""
        legal_moves = self.get_legal_moves()
        for row_index in range(self.size):
            row = self.board[row_index * self.size : (row_index + 1) * self.size]
            row_strs = []
            for col_index, cell in enumerate(row):
                if cell == 1:
                    row_strs.append(colorama.Fore.GREEN + "X " + colorama.Style.RESET_ALL)
                elif cell == -1:
                    row_strs.append(colorama.Fore.MAGENTA + "O " + colorama.Style.RESET_ALL)
                else:
                    square_index = row_index * self.size + col_index
                    square_str = str(square_index).rjust(2)
                    if square_index in legal_moves:
                        row_strs.append(colorama.Fore.YELLOW + square_str + colorama.Style.RESET_ALL)
                    else:
                        row_strs.append("  ")
            output += " | ".join(row_strs)
            output += "\n"
            if row_index < self.size - 1:
                output += "---" + "+----" * (self.size - 1) + "\n"
        return output

    def get_legal_moves(self) -> List[int]:
        """Returns a list of indices where moves can be made."""
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1),          (0, 1),
                      (1, -1), (1, 0), (1, 1)]
        legal_moves = set()
        
        for idx, cell in enumerate(self.board):
            if cell != 0:
                continue
            row, col = divmod(idx, self.size)
            for dr, dc in directions:
                r, c = row + dr, col + dc
                found_opponent = False
                while 0 <= r < self.size and 0 <= c < self.size:
                    neighbor_idx = r * self.size + c
                    if self.board[neighbor_idx] == -self.current_player:
                        found_opponent = True
                    elif self.board[neighbor_idx] == self.current_player:
                        if found_opponent:
                            legal_moves.add(idx)
                        break
                    else:
                        break
                    r += dr
                    c += dc
        return list(legal_moves)
    
    def copy(self) -> "GameOthello":
        """Returns a deep copy of the game."""
        new_game = GameOthello(self.size)
        new_game.board = list(self.board)
        new_game.current_player = self.current_player
        return new_game
    
    def make_move(self, move: int) -> "GameOthello":
        """
        Creates and returns a new GameOthello object after making the move.
        Assumes the move is valid.
        """
        if self.board[move] != 0:
            raise ValueError("Invalid move attempted on a non-empty cell.")
        
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1),          (0, 1),
                      (1, -1), (1, 0), (1, 1)]
        
        new_game = self.copy()
        new_game.board[move] = self.current_player
        
        row, col = divmod(move, self.size)
        for dr, dc in directions:
            r, c = row + dr, col + dc
            to_flip = []
            while 0 <= r < self.size and 0 <= c < self.size:
                neighbor_idx = r * self.size + c
                if new_game.board[neighbor_idx] == -self.current_player:
                    to_flip.append(neighbor_idx)
                elif new_game.board[neighbor_idx] == self.current_player:
                    for flip_idx in to_flip:
                        new_game.board[flip_idx] = self.current_player
                    break
                else:
                    break
                r += dr
                c += dc
        
        new_game.current_player = -self.current_player  # Switch player
        return new_game
    
    def check_win(self) -> Optional[int]:
        """
        Checks for a win. Returns 1 if 'X' wins, -1 if 'O' wins, 0 if no winner (draw),
        and None if the game is still ongoing.
        """
        if self.get_legal_moves():
            return None  # Game is still ongoing
        
        count_x = sum(1 for cell in self.board if cell == 1)
        count_o = sum(1 for cell in self.board if cell == -1)
        
        if count_x > count_o:
            return 1  # 'X' wins
        elif count_o > count_x:
            return -1 # 'O' wins
        else:
            return 0  # Draw
        
    def is_game_over(self) -> bool:
        """Returns True if the game is over (win or draw), else False."""
        return self.check_win() is not None

###############################################################################
#   --- Example Usage (Unchanged) ---
#
if __name__ == "__main__":
    game = GameOthello()
    print("Initial Game State:")
    print(game)
    print("Legal Moves:", game.get_legal_moves())
    while not game.is_game_over():
        legal_moves = game.get_legal_moves()
        move = legal_moves[0] if legal_moves else -1
        if move == -1:
            print("No legal moves available. Passing turn.")
            game.current_player = -game.current_player
            continue
        print(f"Player {'X' if game.current_player == 1 else 'O'} plays move at index {move}")
        game = game.make_move(move)
        print(game)
        print("Legal Moves:", game.get_legal_moves())
    
    print("Game Over!")
    result = game.check_win()
    if result == 1:
        print("Player X wins!")
    elif result == -1:
        print("Player O wins!")
    else:
        print("It's a draw!")