from dataclasses import dataclass
from typing import List

from blunder_wunder.types import MoveClassification


@dataclass
class Move:
    start_fen: str
    end_fen: str
    color: str
    played_move: str
    engine_move: str
    classification: MoveClassification


class Game:

    # TODO - Store meta data from PGN
    def __init__(self):
        self.moves: List[Move] = []

    def accuracy(self):
        # TODO - Implement accuracy for player and opponent
        return
