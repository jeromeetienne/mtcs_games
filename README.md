# mtcs games

This directory contains implementations of various two-player games using the Monte Carlo Tree Search (MCTS) algorithm. The games included are:
- Tic-Tac-Toe
- Connect4
- Othello

Each game is implemented with a common interface defined in the `protocols` module, allowing for easy integration with different player strategies, including human players and AI players using MCTS.

The UI is console-based, providing a simple way to interact with the games. Players can choose to play as 'X' or 'O' and can select which game to play via command-line arguments.

## How to install

Create a virtual environment and install the required packages:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

Install the dependencies:

```bash
pip install -e .
```

## How to play
Run the `play_game.py` script with the desired game and player options:

```bash
./bin/play_game.py --game tictactoe --first human
```

```bash
./bin/play_game.py --game connect4 --first ai
```

To get the inline help, run:

```bash
$ ./bin/play_game.py --help
usage: play_game.py [-h] [--game {tictactoe,connect4,othello}] [--first {human,ai}]

Play a game of Tic-Tac-Toe, Connect4, or Othello against an AI.

options:
  -h, --help            show this help message and exit
  --game {tictactoe,connect4,othello}, -g {tictactoe,connect4,othello}
                        Choose the game to play. (default: tictactoe)
  --first {human,ai}, -f {human,ai}
                        Choose who plays first. (default: human)
```