from copy import deepcopy

from chess import pgn
from chess import engine as computer

from blunder_wunder.types import MoveClassification
from blunder_wunder.game import Move, Game


def color_from_board(board):
    return 'White' if board.turn else 'Black'


def process_pgn(file: str, engine_path: str):
    with open(file, 'r') as pgn_file:
        game = pgn.read_game(pgn_file)
    analyse_game(game, engine_path, "Black")


def calculate_relative_move_score(prior: int, after: int):
    result = prior - after
    print(result)


def evaluate_for_white(engine, board) -> int:
    return engine.analyse(board, computer.Limit(depth=20))["score"].white()


def classify_move(difference: int):
    # TODO - Make move classification configurable
    if difference == 0:
        return MoveClassification.TOP_ENGINE_MOVE
    elif difference < 100:
        return MoveClassification.GOOD_MOVE
    elif difference >= 100:
        return MoveClassification.INACCURACY
    elif difference >= 200:
        return MoveClassification.MISTAKE
    elif difference >= 500:
        return MoveClassification.BLUNDER


def determine_move_strength(color, human_move, engine_move):
    if color == "Black":
        difference = human_move - engine_move
        return classify_move(difference)
    difference = engine_move - human_move
    return classify_move(difference)


def analyse_game(game, engine_path: str, player_color):
    analysed_game = Game()
    board = game.board()
    engine = computer.SimpleEngine.popen_uci(engine_path)
    for move in game.mainline_moves():
        current_player = color_from_board(board)
        if current_player == player_color:
            # TODO - Refactor this mess
            starting_fen = board.fen()
            copied_board = deepcopy(board)
            board.push(move)
            ending_fen = board.fen()
            post_move = evaluate_for_white(engine, board)
            best_engine_move = engine.play(copied_board, computer.Limit(depth=20))
            copied_board.push(best_engine_move.move)
            post_engine_move = evaluate_for_white(engine, copied_board)
            classification = determine_move_strength(current_player, post_move.score(), post_engine_move.score())
            analysed_game.moves.append(Move(starting_fen, ending_fen, current_player, move, str(best_engine_move.move), classification))
            print(analysed_game.moves[-1])
        else:
            board.push(move)


if __name__ == '__main__':
    process_pgn("/Users/edmundmartin/PycharmProjects/blunder_wunder/test_pgn", "/usr/local/bin/stockfish")