import random
from typing import runtime_checkable
from ..protocols.player_protocol import PlayerProtocol
from ..protocols.game_protocol import GameProtocol

class PlayerRandom(PlayerProtocol):
    """
    Represents an AI player that chooses a move randomly from legal options.
    """
    def __init__(self, player_id: int):
        self.player_id: int = player_id
        self.marker: str = 'X' if player_id == 1 else 'O'

    def get_move(self, game: GameProtocol) -> int:
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
