# stdlib imports
import sys
import typing
# pip imports
from simple_term_menu import TerminalMenu

# local imports
from ..protocols.player_protocol import PlayerProtocol
from ..protocols.game_protocol import GameProtocol

class PlayerHuman(PlayerProtocol):
    """
    Represents a player whose moves are decided by human input.
    """
    def __init__(self, player_id: int):
        self.player_id: int = player_id
        self.marker: str = 'X' if player_id == 1 else 'O'

    def get_move(self, game: GameProtocol) -> int:
        """
        Prompts the human for a move and validates the input.
        """
        print(f"👤 Your Turn ({self.marker}). Legal moves are: {game.get_legal_moves()}")
        while True:
            try:
                legal_moves = game.get_legal_moves()
                legal_moves.sort()

                # Show a terminal menu for move selection
                menu_options = [str(move) for move in legal_moves]
                terminal_menu = TerminalMenu(menu_options, title="Select your move:")
                menu_entry_index = terminal_menu.show()
                assert menu_entry_index is not None, "No move selected."
                menu_entry_index = typing.cast(int, menu_entry_index)
                # Get the move from the selected menu option
                move_input: int = int(menu_options[menu_entry_index])

                # Check for EOF/Ctrl+D and exit gracefully
                if move_input is None:
                    raise EOFError()
                
                move = int(move_input)
                legal_moves = game.get_legal_moves()
                
                if move in legal_moves:
                    return move
                else:
                    print(f"❌ Invalid move: {move} is not an empty cell or is outside the board range.")
            except ValueError:
                print("❌ Invalid input. Please enter a number.")
            except EOFError:
                print("\nGame aborted by user.")
                sys.exit(0) # Exit the program cleanly
