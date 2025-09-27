# stdlib imports
import sys
import typing
# pip imports
from simple_term_menu import TerminalMenu

# local imports
from src.bases.move import Move
from src.bases.player_base import PlayerBase
from src.bases.game_base import GameBase

###############################################################################
#   Human Player
#
class PlayerHuman(PlayerBase):
    """
    Represents a player whose moves are decided by human input.
    """
    def __init__(self, player_id: int):
        self.player_id: int = player_id
        self.marker: str = 'X' if player_id == 1 else 'O'

    def get_move(self, game: GameBase) -> int:
        """
        Prompts the human for a move and validates the input.
        """
        legal_moves = game.get_legal_moves()
        print(f"👤 Your Turn ({self.marker}). Legal moves are: {[int(move) for move in legal_moves]}")
        while True:
            try:
                legal_moves = game.get_legal_moves()
                # sort the legal moves for better display
                legal_moves.sort(key=lambda move: int(move))

                # Show a terminal menu for move selection
                menu_options = [str(move) for move in legal_moves]
                terminal_menu = TerminalMenu(menu_options, title="Select your move:")
                menu_entry_index = terminal_menu.show()
                assert menu_entry_index is not None, "No move selected."
                menu_entry_index = typing.cast(int, menu_entry_index)
                # Get the move from the selected menu option
                move_idx: int = int(menu_options[menu_entry_index])

                # Check for EOF/Ctrl+D and exit gracefully
                if move_idx is None:
                    raise EOFError()
                
                move = Move(move_idx)
                legal_moves = game.get_legal_moves()
                
                if move in legal_moves:
                    return int(move)
                else:
                    print(f"❌ Invalid move: {move} is not an empty cell or is outside the board range.")
            except ValueError:
                print("❌ Invalid input. Please enter a number.")
            except EOFError:
                print("\nGame aborted by user.")
                sys.exit(0) # Exit the program cleanly

    def copy(self) -> 'PlayerHuman':
        """Create and return a copy of this player instance."""
        return PlayerHuman(self.player_id)
