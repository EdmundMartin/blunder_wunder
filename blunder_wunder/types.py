from enum import Enum


class MoveClassification(Enum):
    TOP_ENGINE_MOVE = "TOP_ENGINE_MOVE"
    GOOD_MOVE = "GOOD_MOVE"
    INACCURACY = "INACCURACY"
    MISTAKE = "MISTAKE"
    BLUNDER = "BLUNDER"


class Color(Enum):
    WHITE = "WHITE"
    BLACK = "BLACK"
