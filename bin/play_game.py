#! /usr/bin/env python3
"""
A simple script to play a game of Tic-Tac-Toe or Connect4 between a human player
and an AI player (Random or MCTS).
"""

# pip imports
import argparse

# local imports
from src.bases.types import PlayerID
from src.bases.move import Move
from src.games.game_tictactoe import GameTicTacToe
from src.games.game_connect4 import GameConnect4
from src.games.game_othello import GameOthello
from src.players.player_human import PlayerHuman
from src.players.player_mtcs import PlayerMCTS
from src.players.player_random import PlayerRandom
from src.bases.base_player import BasePlayer
from src.bases.base_game import BaseGame


###############################################################################
#   Game Loop
#
def play_game(game: BaseGame, player1: BasePlayer, player2: BasePlayer) -> int:
    """
    Plays a game of Tic-Tac-Toe between a HumanPlayer and a RandomPlayer.

    Args:
        game (GameBase): The game instance to play.
        player1 (PlayerBase): The player for 'X' (player_id=1).
        player2 (PlayerBase): The player for 'O' (player_id=-1).
    """

    players: dict[int, BasePlayer] = {1: player1, -1: player2}

    # Display the initial board with move indices
    print("🤖 Welcome to Tic-Tac-Toe! The board indices are as follows:")
    print(game)  # The __repr__ now includes indices on empty cells

    print("-" * 30)
    print(f"Player X is: {type(players[1]).__name__}")
    print(f"Player O is: {type(players[-1]).__name__}")
    print("-" * 30)

    while not game.is_game_over():
        current_player = players[game.current_player]

        print(f"\n✨ Current Board:\n{game}")

        # Get the move from the current player object
        move = current_player.get_move(game)

        # Log the move
        print(f"Player {current_player.marker} ({type(current_player).__name__}) picked move: {move}")

        # Make the move and update the game state
        game = game.make_move(move)

    # Game Over
    print("\n--- Game Over ---")
    print(game)
    result = game.get_winner()

    if result == 1:
        print(f"🎉 **Player X ({players[1].marker}) Wins!** 🎉")
    elif result == -1:
        print(f"💔 **Player O ({players[-1].marker}) Wins!** 💔")
    elif result == 0:
        print("🤝 **It's a Draw!** 🤝")
    else:
        assert False, "Unexpected game result."

    return result


###############################################################################
#   Main function to parse arguments and start the game
#
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Play a game of Tic-Tac-Toe, Connect4, or Othello against an AI.", formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--game", "-g", choices=["tictactoe", "connect4", "othello"], default="tictactoe", help="Choose the game to play.")
    parser.add_argument("--games_per_match", "-gpm", type=int, default=1, help="Number of games to play in a match.")
    parser.add_argument("--first", "-f", choices=["human", "ai", "random"], default="human", help="Choose who plays first.")
    parser.add_argument("--second", "-s", choices=["human", "ai", "random"], default="ai", help="Choose who plays second.")
    parser.add_argument("--simulations", "-sim", type=int, default=1000, help="Number of simulations for MCTS.")
    parser.add_argument("--exploration", "-exp", type=float, default=1.4, help="Exploration parameter for MCTS.")
    parser.add_argument("--seed", type=int, help="Random seed for reproducibility.")
    args = parser.parse_args()  # Example args for testing

    # init player1
    if args.first == "human":
        player1 = PlayerHuman(PlayerID(1))
    elif args.first == "ai":
        player1 = PlayerMCTS(PlayerID(1), simulations=args.simulations, c_param=args.exploration, seed=args.seed)
    elif args.first == "random":
        player1 = PlayerRandom(PlayerID(1))
    else:
        assert False, "Invalid first player choice."

    # init player2
    if args.second == "human":
        player2 = PlayerHuman(PlayerID(-1))
    elif args.second == "ai":
        player2 = PlayerMCTS(PlayerID(-1), simulations=args.simulations, c_param=args.exploration, seed=args.seed)
    elif args.second == "random":
        player2 = PlayerRandom(PlayerID(-1))
    else:
        assert False, "Invalid second player choice."

    # Play the match
    game_count = args.games_per_match
    match_score = 0
    for game_index in range(game_count):
        # Create a fresh game for each match
        if args.game == "tictactoe":
            game = GameTicTacToe()
        elif args.game == "connect4":
            game = GameConnect4()
        elif args.game == "othello":
            game = GameOthello()
        else:
            assert False, "Invalid game choice."
        # start the game
        game_result = play_game(game, player1, player2)
        print(f"Game {game_index + 1}th result: {game_result}")

        match_score += game_result

    print("\n=== Tournament Summary ===")
    print(f"Total Games Played: {game_count}")
    print(f"Tournament Score: {match_score}")
