# stdlib imports
import random

# local imports
from src.bases.move import Move
from src.bases.player_base import PlayerBase
from src.bases.game_base import GameBase

class PlayerRandom(PlayerBase):
    """
    Represents an AI player that chooses a move randomly from legal options.
    """
    def __init__(self, player_id: int):
        self.player_id: int = player_id
        self.marker: str = 'X' if player_id == 1 else 'O'

    def get_move(self, game: GameBase) -> Move:
        """
        Picks a random move from the list of legal moves.
        """
        print(f"🤖 AI's Turn ({self.marker}). Thinking...")
        legal_moves = game.get_legal_moves()
        if legal_moves:
            ai_move = random.choice(legal_moves)
            print(f"AI chooses move: {ai_move}")
            return ai_move
        
        # This should ideally not be reached if is_game_over is checked first
        raise Exception("AI attempted to move when no legal moves were available (Draw state).")

    def copy(self) -> 'PlayerRandom':
        """Create and return a copy of this player instance."""
        return PlayerRandom(self.player_id)
