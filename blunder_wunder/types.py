from enum import IntEnum, Enum


class MoveClassification(IntEnum):
    TOP_ENGINE_MOVE = 0
    GOOD_MOVE = 1
    INACCURACY = 2
    MISTAKE = 3
    BLUNDER = 4

    def to_friendly_string(self):
        return {
            MoveClassification.TOP_ENGINE_MOVE: "Top Engine Move",
            MoveClassification.GOOD_MOVE: "Good Move",
            MoveClassification.INACCURACY: "Inaccuracy",
            MoveClassification.MISTAKE: "Mistake",
            MoveClassification.BLUNDER: "Blunder"
        }[self]


class Color(Enum):
    WHITE = "WHITE"
    BLACK = "BLACK"
