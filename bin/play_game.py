#! /usr/bin/env python3
"""
A simple script to play a game of Tic-Tac-Toe or Connect4 between a human player
and an AI player (Random or MCTS).
"""

# pip imports
import argparse


from src.games.game_tictactoe import GameTicTacToe
from src.games.game_connect4 import GameConnect4
from src.games.game_othello import GameOthello
from src.players.player_human import PlayerHuman
from src.players.player_mtcs import PlayerMCTS
from src.protocols.player_protocol import PlayerProtocol
from src.protocols.game_protocol import GameProtocol

def play_game(game: GameProtocol, human_starts: bool = True) -> None:
    """
    Plays a game of Tic-Tac-Toe between a HumanPlayer and a RandomPlayer.

    :param human_starts: If True, HumanPlayer is 'X' (1); otherwise, RandomPlayer is 'X'.
    """

    if human_starts:
        player1 = PlayerHuman(1) # X
        # player2 = RandomPlayer(-1) # O
        player2 = PlayerMCTS(-1) # O
    else:
        # player1 = RandomPlayer(1) # X
        player1 = PlayerMCTS(1) # X
        player2 = PlayerHuman(-1) # O

    players: dict[int, PlayerProtocol] = {1: player1, -1: player2}

    # Display the initial board with move indices
    print("🤖 Welcome to Tic-Tac-Toe! The board indices are as follows:")
    print(game) # The __repr__ now includes indices on empty cells
    
    print("-" * 30)
    print(f"Player X is: {type(players[1]).__name__}")
    print(f"Player O is: {type(players[-1]).__name__}")
    print("-" * 30)
    
    while not game.is_game_over():
        current_player_obj = players[game.current_player]
        
        print(f"\n✨ Current Board:\n{game}")
        
        # Get the move from the current player object
        move = current_player_obj.get_move(game)
        
        # Make the move and update the game state
        game = game.make_move(move)
            
    # Game Over
    print("\n--- Game Over ---")
    print(game)
    result = game.check_win()
    
    if result == 1:
        print(f"🎉 **Player X ({players[1].marker}) Wins!** 🎉")
    elif result == -1:
        print(f"💔 **Player O ({players[-1].marker}) Wins!** 💔")
    else: # result == 0
        print("🤝 **It's a Draw!** 🤝")

# --- Example of How to Play ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Play a game of Tic-Tac-Toe, Connect4, or Othello against an AI.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('--game', '-g', choices=['tictactoe', 'connect4', 'othello'], default='tictactoe', help="Choose the game to play.")
    parser.add_argument('--first', '-f', choices=['human', 'ai'], default='human', help="Choose who plays first.")
    args = parser.parse_args()

    if args.game == 'tictactoe':
        game = GameTicTacToe()
    elif args.game == 'connect4':
        game = GameConnect4()
    elif args.game == 'othello':
        game = GameOthello()
    else:
        assert False, "Invalid game choice."

    if args.first == 'human':
        play_game(game,human_starts=True)
    else:
        play_game(game,human_starts=False)
