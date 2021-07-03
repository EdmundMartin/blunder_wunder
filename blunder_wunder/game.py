from dataclasses import dataclass
from typing import List, Optional

from blunder_wunder.types import MoveClassification, Color


@dataclass
class AnalysedMove:
    start_fen: str
    end_fen: str
    color: Color
    played_move: str
    engine_move: str
    classification: MoveClassification


class AnalysedGame:

    def __init__(self, game_metadata):
        self.metadata = game_metadata
        self.moves: List[AnalysedMove] = []

    def _color_from_player_name(self, player_name: str) -> Color:
        if self.metadata["White"] == player_name:
            return Color.WHITE
        return Color.BLACK

    def list_mistakes(self, player_name: Optional[str] = None) -> List[AnalysedMove]:
        matched_color = (
            None if not player_name else self._color_from_player_name(player_name)
        )
        mistakes: List[AnalysedMove] = []
        for move in self.moves:
            if matched_color and matched_color != move.color:
                continue
            if move.classification == MoveClassification.MISTAKE:
                mistakes.append(move)
        return mistakes

    def accuracy(self):
        # TODO - Implement accuracy for player and opponent
        return


if __name__ == "__main__":
    import chess.pgn as pgn

    with open(
        "/Users/edmundmartin/PycharmProjects/blunder_wunder/test_pgn", "r"
    ) as pgn_file:
        game = pgn.read_game(pgn_file)
    res = AnalysedGame(game.headers)
    print(res._color_from_player_name("WhySoBad909"))
    results = res.list_mistakes("WhySoBad909")
    print(results)
