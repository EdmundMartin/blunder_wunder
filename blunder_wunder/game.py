from dataclasses import dataclass
from typing import List, Optional

from chess.pgn import Game
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
    suggested_line: List[chess.Move]


class AnalysedGame:

    def __init__(self, game_metadata):
        self.metadata = game_metadata
        self.moves: List[AnalysedMove] = []

    def _color_from_player_name(self, player_name: str) -> Color:
        if self.metadata["White"] == player_name:
            return Color.WHITE
        return Color.BLACK

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
        for move in self.moves:
            node = node.add_main_variation(chess.Move.from_uci(move.played_move))
            if move.classification >= MoveClassification.INACCURACY:
                node.comment = f"{move.played_move} was a {move.classification.to_friendly_string().lower()}, suggested engine move was {move.engine_move}"
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
