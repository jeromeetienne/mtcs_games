from typing import NewType, Literal

PlayerID = NewType('PlayerID', int)  # +1 for player 1 (X), -1 for player 2 (O)

PlayerMarker = Literal['X', 'O']

def player_id_to_marker(player_id: PlayerID) -> PlayerMarker:
    return 'X' if player_id == 1 else 'O'