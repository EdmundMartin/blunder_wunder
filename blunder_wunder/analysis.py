from copy import deepcopy
from typing import Optional, Callable, List
from dataclasses import dataclass
import io

from chess import pgn
from chess import engine as computer
from chess.pgn import Game

from blunder_wunder.types import MoveClassification, Color
from blunder_wunder.game import AnalysedMove, AnalysedGame


MOVE_CLASSIFIER = Callable[[int], MoveClassification]


@dataclass
class EngineInfo:
    white_score: computer.Score
    suggested_line: List
    pov: computer.PovScore


def color_from_board(board):
    return Color.WHITE if board.turn else Color.BLACK


def evaluate_for_white(engine: computer.SimpleEngine, board, depth: computer.Limit) -> EngineInfo:
    raw = engine.analyse(board, depth)
    return EngineInfo(raw["score"].white(), raw.get("pv", list()), raw["score"])


def classify_move(difference: int) -> MoveClassification:
    if difference == 0:
        return MoveClassification.TOP_ENGINE_MOVE
    elif difference < 25:
        return MoveClassification.EXCELLENT_MOVE
    elif difference < 50:
        return MoveClassification.GOOD_MOVE
    elif difference < 150:
        return MoveClassification.INACCURACY
    elif difference < 250:
        return MoveClassification.MISTAKE
    else:
        return MoveClassification.BLUNDER


def determine_move_strength(color, human_move, engine_move, classifier: MOVE_CLASSIFIER):
    if color == color.BLACK:
        difference = human_move - engine_move
        return classify_move(difference)
    difference = engine_move - human_move
    return classifier(difference)


class GameAnalysis:
    def __init__(self, engine_path: str, depth: int = 20,  time_limit: Optional[int] = None,
                 move_classifier: Optional[MOVE_CLASSIFIER] = None):
        self.engine_path = engine_path
        self.config = None
        self.depth = computer.Limit(depth=depth) if time_limit is None else computer.Limit(time=time_limit)
        self._best_line = None
        self._move_classifier = classify_move if move_classifier is None else move_classifier

    def _is_mate(self, first_eval, second_eval) -> bool:
        return first_eval.is_mate() or second_eval.is_mate()

    def evaluate_mate(self, post_move, post_engine_move):
        if post_move.is_mate() and not post_engine_move.is_mate():
            return MoveClassification.BLUNDER
        return MoveClassification.GOOD_MOVE

    def _analyse_move(self, engine: computer.SimpleEngine, board, move) -> AnalysedMove:
        current_color = color_from_board(board)
        pre_move_fen = board.fen()
        copied_board = deepcopy(board)
        board.push(move)
        post_move_fen = board.fen()
        human_eval: EngineInfo = evaluate_for_white(engine, board, self.depth)
        best_engine_move = engine.play(copied_board, self.depth)
        copied_board.push(best_engine_move.move)
        computer_eval: EngineInfo = evaluate_for_white(engine, copied_board, self.depth)
        if self._is_mate(human_eval.white_score, computer_eval.white_score):
            classification = self.evaluate_mate(human_eval.white_score, computer_eval.white_score)
        else:
            classification = determine_move_strength(current_color, human_eval.white_score.score(), computer_eval.white_score.score(), self._move_classifier)
        analyzed_move = AnalysedMove(
            pre_move_fen,
            post_move_fen,
            current_color,
            str(move),
            str(best_engine_move.move),
            classification,
            human_eval.pov,
            self._best_line
        )
        self._best_line = human_eval.suggested_line
        return analyzed_move

    def analyse_game(self, game: Game, color: Optional[Color] = None):
        analysed_game = AnalysedGame(game.headers)
        board = game.board()
        engine: computer.SimpleEngine = computer.SimpleEngine.popen_uci(
            self.engine_path
        )
        for move in game.mainline_moves():
            current_player = color_from_board(board)
            if color and current_player != color:
                board.push(move)
                continue
            analysed_move = self._analyse_move(engine, board, move)
            analysed_game.moves.append(analysed_move)
            print(analysed_move)
        engine.close()
        return analysed_game

    def analyse_game_from_pgn(self, pgn_file_path: str, color: Optional[Color] = None) -> AnalysedGame:
        with open(pgn_file_path, "r") as pgn_file:
            game = pgn.read_game(pgn_file)
        return self.analyse_game(game, color)

    def analyse_game_from_pgn_str(self, pgn_content: str) -> AnalysedGame:
        return self.analyse_game(pgn.read_game(io.StringIO(pgn_content)))
