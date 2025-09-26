from src.protocols.game_protocol import GameProtocol
from typing import List, Optional


class GameOthello(GameProtocol):
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
        """Prints a human-readable board representation, showing move indices on empty cells."""
        output: str = ""
        for i in range(self.size):
            row = self.board[i * self.size : (i + 1) * self.size]
            output += " | ".join(["X " if cell == 1 else "O " if cell == -1 else str(i * self.size + j).rjust(2) for j, cell in enumerate(row)])
            output += "\n"
            if i < self.size - 1:
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
    
    def get_game_state(self) -> List[int]:
        """Returns the current game state as a list."""
        return list(self.board)
    
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
