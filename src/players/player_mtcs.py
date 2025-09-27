# stdlib imports
import math
import random
import typing
from typing import Dict, List, Optional, Tuple

# local imports
from src.bases.move import Move
from src.bases.types import PlayerID, PlayerMarker, player_id_to_marker
from src.bases.base_player import BasePlayer
from src.bases.base_game import BaseGame

###############################################################################
#   MCTS Tree Node
#
class MCTSNode:
    """
    Represents a single node in the Monte Carlo Tree Search tree.
    """
    def __init__(self, game_state: BaseGame, parent: Optional['MCTSNode'] = None, parent_move: Optional[int] = None):
        self.game_state: BaseGame = game_state
        self.parent: Optional['MCTSNode'] = parent
        self.parent_move: Optional[int] = parent_move # The move that led to this state
        self.children: Dict[int, 'MCTSNode'] = {}    # Maps move (int) to child node
        self.wins: float = 0.0                      # Total wins from this node's perspective (1 for win, 0.5 for draw, 0 for loss)
        self.visits: int = 0                        # Total number of times this node has been visited
    
    def is_fully_expanded(self) -> bool:
        """Checks if all legal moves from this state have corresponding child nodes."""
        return len(self.children) == len(self.game_state.get_legal_moves())

    def unexpanded_moves(self) -> List[int]:
        """Returns a list of legal moves that do not yet have a child node."""
        all_move_index = set(int(move) for move in self.game_state.get_legal_moves())
        expanded_move_indices = set(self.children.keys())
        return list(all_move_index - expanded_move_indices)

    def best_uct_child(self, c_param: float = 1.4) -> Tuple[int, 'MCTSNode']:
        """
        Selects the child node with the highest UCT1 (Upper Confidence Bound 1 applied to trees) value.
        UCT1 formula: (wins / visits) + c * sqrt(ln(parent_visits) / visits)
        """
        log_parent_visits = math.log(self.visits)
        
        # We want to maximize the UCT score
        best_score = -float('inf')
        best_move_node: Optional[Tuple[int, MCTSNode]] = None

        for move, child in self.children.items():
            if child.visits == 0:
                # Prioritize unvisited nodes for expansion
                score = float('inf') 
            else:
                # The win rate is from the perspective of the player *who just played* to reach this node.
                # When we are selecting, we are choosing the move for the *current* player (game_state.current_player).
                
                # UCT calculation: win_rate + exploration_term
                win_rate = child.wins / child.visits
                exploration_term = c_param * math.sqrt(log_parent_visits / child.visits)
                score = win_rate + exploration_term
            
            if score > best_score:
                best_score = score
                best_move_node = (move, child)
        
        if best_move_node is None:
             raise Exception("No children found for UCT selection, this should not happen in a non-terminal node.")

        return best_move_node
    
###############################################################################
#   MCTS Player Implementation
#
class PlayerMCTS(BasePlayer):
    """
    An AI player that uses Monte Carlo Tree Search to determine the best move.
    """
    def __init__(self, player_id: PlayerID, simulations: int = 1000, c_param: float = 1.4, seed: int | None = None):
        self.player_id: PlayerID = player_id
        self.marker: PlayerMarker = player_id_to_marker(player_id)
        self.simulations: int = simulations
        self.c_param: float = c_param # Exploration constant for UCT
        self.rnd_generator = random.Random()
        if seed is not None:
            self.rnd_generator.seed(seed)


    def get_move(self, game: BaseGame) -> Move:
        """
        Runs the MCTS algorithm for a fixed number of simulations and returns the
        best move based on the most visited child node.
        """
        if game.is_game_over():
            raise Exception("Cannot get move from a terminal game state.")

        # 1. Initialize the root of the MCTS tree
        root = MCTSNode(game)
        
        for _ in range(self.simulations):
            # A. Selection: Traverse down the tree using UCT until an unexpanded node
            node = self._select_node(root)
            
            # B. Expansion: Add a new child node (if not terminal)
            if not node.game_state.is_game_over():
                node = self._expand_node(node)

            # C. Simulation: Playout a random game from the new node
            score = self._simulate(node.game_state)
            
            # D. Backpropagation: Update wins/visits up the tree
            self._backpropagate(node, score)

        # 5. Final Move Decision: Choose the move that leads to the most visited child
        return self._best_move(root)

    def _select_node(self, node: MCTSNode) -> MCTSNode:
        """The Selection phase: Traverse the tree using UCT."""
        while node.is_fully_expanded() and not node.game_state.is_game_over():
            _, node = node.best_uct_child(self.c_param)
        return node

    def _expand_node(self, node: MCTSNode) -> MCTSNode:
        """The Expansion phase: Select an unexpanded move and create a new child."""
        unexpanded_moves = node.unexpanded_moves()
        random_move_idx = self.rnd_generator.choice(unexpanded_moves)
        
        random_move = Move(random_move_idx)
        new_game_state = node.game_state.make_move(random_move)
        new_node = MCTSNode(new_game_state, parent=node, parent_move=random_move_idx)
        node.children[random_move_idx] = new_node
        
        return new_node

    def _simulate(self, game: BaseGame) -> int:
        """
        The Simulation (or Playout) phase: Play a random game until a terminal state.
        Returns the winner (1, -1, or 0 for draw).
        """
        current_game = game
        while not current_game.is_game_over():
            legal_moves = current_game.get_legal_moves()
            if not legal_moves: # Should be handled by is_game_over but good for safety
                return 0
            move = self.rnd_generator.choice(legal_moves)
            current_game = current_game.make_move(move)

        # winner  = typing.cast(int, current_game.check_win())

        return typing.cast(int, current_game.get_winner())   

    def _backpropagate(self, node: MCTSNode, result: int) -> None:
        """The Backpropagation phase: Update visits and wins up to the root."""
        current_node = node
        while current_node is not None:
            current_node.visits += 1
            
            # Score is from the perspective of the player *who just played* to reach the current_node's state
            # This player is current_node.game_state.current_player * -1
            
            # The result is the final winner (1, -1, or 0)
            if result == 0:
                score = 0.5 # Draw
            elif result == current_node.game_state.current_player * -1:
                score = 1.0 # Win
            else:
                score = 0.0 # Loss

            current_node.wins += score
            current_node = current_node.parent

    def _best_move(self, root: MCTSNode) -> Move:
        """
        The final decision: Choose the move corresponding to the child with the most visits.
        """
        # We look for the most visited child, which is often more stable than the one with the highest win rate.
        best_visits = -1
        best_move_idx = -1
        
        for move, child in root.children.items():
            if child.visits > best_visits:
                best_visits = child.visits
                best_move_idx = move
                
        if best_move_idx == -1:
            raise Exception("MCTS failed to find a move for the current state.")
            
        return Move(best_move_idx)

    def copy(self) -> 'PlayerMCTS':
        """Create and return a copy of this player instance."""
        new_player = PlayerMCTS(self.player_id, simulations=self.simulations, c_param=self.c_param)
        # Preserve the random generator state
        new_player.rnd_generator.setstate(self.rnd_generator.getstate())
        return new_player