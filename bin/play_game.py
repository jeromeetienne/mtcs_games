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
from src.players.player_random import PlayerRandom
from src.protocols.player_protocol import PlayerProtocol
from src.protocols.game_protocol import GameProtocol

def play_game(game: GameProtocol, player1: PlayerProtocol, player2: PlayerProtocol) -> None:
    """
    Plays a game of Tic-Tac-Toe between a HumanPlayer and a RandomPlayer.

    :param human_starts: If True, HumanPlayer is 'X' (1); otherwise, RandomPlayer is 'X'.
    """

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
    parser.add_argument('--first', '-f', choices=['human', 'ai', 'random'], default='human', help="Choose who plays first.")
    parser.add_argument('--second', '-s', choices=['human', 'ai', 'random'], default='ai', help="Choose who plays second.")
    parser.add_argument('--simulations', '-sim', type=int, default=1000, help="Number of simulations for MCTS.")
    parser.add_argument('--exploration', '-exp', type=float, default=1.4, help="Exploration parameter for MCTS.")
    args = parser.parse_args()

    # init game
    if args.game == 'tictactoe':
        game = GameTicTacToe()
    elif args.game == 'connect4':
        game = GameConnect4()
    elif args.game == 'othello':
        game = GameOthello()
    else:
        assert False, "Invalid game choice."

    # init player1
    if args.first == 'human':
        player1 = PlayerHuman(1)
    elif args.first == 'ai':
        player1 = PlayerMCTS(1, simulations=args.simulations, c_param=args.exploration)
    elif args.first == 'random':
        player1 = PlayerRandom(1)
    else:
        assert False, "Invalid first player choice."

    # init player2
    if args.second == 'human':
        player2 = PlayerHuman(-1)
    elif args.second == 'ai':
        player2 = PlayerMCTS(-1, simulations=args.simulations, c_param=args.exploration)
    elif args.second == 'random':
        player2 = PlayerRandom(-1)
    else:
        assert False, "Invalid second player choice."
    

    # start the game
    play_game(game, player1, player2)
