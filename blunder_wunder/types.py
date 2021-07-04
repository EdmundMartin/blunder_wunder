from enum import IntEnum, Enum


class MoveClassification(IntEnum):
    TOP_ENGINE_MOVE = 0
    EXCELLENT_MOVE = 1
    GOOD_MOVE = 2
    INACCURACY = 3
    MISTAKE = 4
    BLUNDER = 5

    def to_friendly_string(self):
        return {
            MoveClassification.TOP_ENGINE_MOVE: "Top Engine Move",
            MoveClassification.EXCELLENT_MOVE: "Excellent Move",
            MoveClassification.GOOD_MOVE: "Good Move",
            MoveClassification.INACCURACY: "Inaccuracy",
            MoveClassification.MISTAKE: "Mistake",
            MoveClassification.BLUNDER: "Blunder"
        }[self]


class Color(Enum):
    WHITE = "WHITE"
    BLACK = "BLACK"
