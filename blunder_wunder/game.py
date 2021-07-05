from dataclasses import dataclass
from typing import List, Optional, Callable, TypedDict

from chess.pgn import Game
from chess.engine import PovScore
import chess

from blunder_wunder.types import MoveClassification, Color
from blunder_wunder.utils import pgn_title_from_metadata


@dataclass
class AnalysedMove:
    start_fen: str
    end_fen: str
    color: Color
    played_move: str
    engine_move: str
    classification: MoveClassification
    pov: PovScore
    suggested_line: List[chess.Move]


class AccuracySummary(TypedDict):
    white: float
    black: float


ACCURACY_FUNCTION = Callable[[List[AnalysedMove]], AccuracySummary]


def _calculate_accuracy(moves: List[AnalysedMove]) -> AccuracySummary:
    move_accuracy = {
        MoveClassification.TOP_ENGINE_MOVE: 10,
        MoveClassification.EXCELLENT_MOVE: 9.5,
        MoveClassification.GOOD_MOVE: 9,
        MoveClassification.INACCURACY: 5,
        MoveClassification.MISTAKE: 2,
        MoveClassification.BLUNDER: 1
    }
    white_scores = []
    black_scores = []
    for move in moves:
        if move.color == Color.WHITE:
            white_scores.append(move_accuracy[move.classification])
        else:
            black_scores.append(move_accuracy[move.classification])
    return {"white": 100 * float(sum(white_scores)) / float(10 * len(white_scores)),
            "black": 100 * float(sum(black_scores)) / float(10 * len(black_scores))}


class AnalysedGame:

    def __init__(self, game_metadata, accuracy_function: Optional[ACCURACY_FUNCTION] = None):
        self.metadata = game_metadata
        self.moves: List[AnalysedMove] = []
        self._accuracy_func: ACCURACY_FUNCTION = _calculate_accuracy if accuracy_function is None else accuracy_function

    def _color_from_player_name(self, player_name: str) -> Color:
        if self.metadata["White"] == player_name:
            return Color.WHITE
        return Color.BLACK

    def _enrich_metadata(self, game_headers) -> None:
        game_headers["Annotator"] = "https://github.com/EdmundMartin/blunder_wunder"
        accuracy = self.accuracy()
        game_headers["Accuracy"] = f"White Accuracy Score: {accuracy['white']}%, Black Accuracy Score: {accuracy['black']}%"

    def _list_moves_of_type(self, classification: MoveClassification, player_name: Optional[str] = None):
        matched_color = (
            None if not player_name else self._color_from_player_name(player_name)
        )
        mistakes: List[AnalysedMove] = []
        for move in self.moves:
            if matched_color and matched_color != move.color:
                continue
            if move.classification == classification:
                mistakes.append(move)
        return mistakes

    def write_to_pgn(self, filename: str):
        game = node = chess.pgn.Game()
        game.headers = self.metadata
        self._enrich_metadata(game.headers)
        for move in self.moves:
            node = node.add_main_variation(chess.Move.from_uci(move.played_move))
            if move.classification >= MoveClassification.INACCURACY:
                node.comment = f"{move.played_move} was a {move.classification.to_friendly_string().lower()}, suggested engine move was {move.engine_move}"
            node.set_eval(move.pov)
        with open(filename, 'w') as outfile:
            outfile.write(str(game))

    def write_to_pgn_name_from_metadata(self):
        filename = pgn_title_from_metadata(self.metadata)
        self.write_to_pgn(filename)

    def list_inaccuracies(self, player_name: Optional[str] = None) -> List[AnalysedMove]:
        return self._list_moves_of_type(MoveClassification.INACCURACY, player_name=player_name)

    def list_mistakes(self, player_name: Optional[str] = None) -> List[AnalysedMove]:
        return self._list_moves_of_type(MoveClassification.MISTAKE, player_name=player_name)

    def list_blunders(self, player_name: Optional[str] = None) -> List[AnalysedMove]:
        return self._list_moves_of_type(MoveClassification.BLUNDER, player_name=player_name)

    def accuracy(self) -> AccuracySummary:
        return self._accuracy_func(self.moves)


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
