# mtcs games
This repository contains implementations of various two-player games using the Monte Carlo Tree Search (MCTS) algorithm. The games included are:
- Tic-Tac-Toe
- Connect4
- Othello

Each game is implemented with a common interface defined in the `protocols` module, allowing for easy integration with different player strategies, including human players and AI players using MCTS.

The UI is console-based, providing a simple way to interact with the games. Players can choose to play as 'X' or 'O' and can select which game to play via command-line arguments.

MCTS doesn't need to know the rules of the game, it just needs to be able to simulate games and get the result. 
No heuristics are used, just pure random simulations.
MCTS is implemented in the `players` module, with a dedicated class for the MCTS player.

## MCTS Algorithm
Here is a short summary of the MCTS algorithm:
- [paper](https://arxiv.org/abs/2103.04931)
- [wikipedia](https://en.wikipedia.org/wiki/Monte_Carlo_tree_search)
- [detailed video explanation](https://www.youtube.com/watch?v=Fbs4lnGLS8M)


## Remarks
- no models (nothing to train)
- if you code the rules of the game, you can play it with MCTS.
   - just need to be able to play the game, and simulate it (playing randomly)
- Crazy good when considering it is just play randomly
- No heuristics, no knowledge of the game, just pure random simulations
## Games

Screenshots of each game. Ascii Art for the win ! 🎮


### Tic-Tac-Toe
A simple implementation of the classic Tic-Tac-Toe game.

![Tic-Tac-Toe Example](https://github.com/user-attachments/assets/32e8b47d-a4a5-4828-8041-00aa3ad284a4)
### Connect4
A Connect4 game where players take turns dropping discs into a 7-column, 6-row vertically suspended grid.

![Connect4 Example](https://github.com/user-attachments/assets/39b73d2e-d7d3-49ab-aedd-c41455707169)
### Othello
An implementation of the Othello game, also known as Reversi, played on an 8x8 board.

![Othello Example](https://github.com/user-attachments/assets/5302edb5-4a1a-43e3-a0df-6a2ca2d4484a)

## How to install

Create a virtual environment and install the required packages:

```bash
python3.10 -m venv .venv
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
» ./bin/play_game.py -h                                                                                                 1 ↵
usage: play_game.py [-h] [--game {tictactoe,connect4,othello}] [--first {human,ai,random}] [--second {human,ai,random}] [--simulations SIMULATIONS] [--exploration EXPLORATION]

Play a game of Tic-Tac-Toe, Connect4, or Othello against an AI.

options:
  -h, --help            show this help message and exit
  --game {tictactoe,connect4,othello}, -g {tictactoe,connect4,othello}
                        Choose the game to play. (default: tictactoe)
  --first {human,ai,random}, -f {human,ai,random}
                        Choose who plays first. (default: human)
  --second {human,ai,random}, -s {human,ai,random}
                        Choose who plays second. (default: ai)
  --simulations SIMULATIONS, -sim SIMULATIONS
                        Number of simulations for MCTS. (default: 1000)
  --exploration EXPLORATION, -exp EXPLORATION
                        Exploration parameter for MCTS. (default: 1.4)
```