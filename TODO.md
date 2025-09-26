# TODO
- do gif of games played
- MTCS make it possible to reuse the tree between moves
  - currently the tree is discarded after each move
  - this would require to keep track of the root node and its children
  - and to update the root node after each move
- make the move an actual `Move` type, and a `Square` type for chess
  - currently it's just an int
- add checkers game ?
- try to make it play chess too
  - how would that work with MTCS ?
- how to get the move representation for chess ?
  - e.g. uci

## DONE
- DONE Do a better UI
  - color in the output
- DONE in game_protocol, add a .copy() method to clone a game state
  - PRO it will be clearer
- DONE make it possible to select the legal moves by arrow keys
- DONE add a way to set the number of simulations for MTCS
  - add a --simulations argument to play_game.py
- DONE add a way to set the exploration parameter for MTCS
  - add a --exploration argument to play_game.py
- DONE make it possible to pick the random player too
- DONE make it possible to play MTCS vs MTCS
  - add a --second argument to play_game.py
