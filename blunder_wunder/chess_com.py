from typing import List

import requests

from blunder_wunder.analysis import GameAnalysis
from blunder_wunder.game import AnalysedGame


def _pad_int(unpadded_int: int) -> str:
    if unpadded_int < 10:
        return f"0{unpadded_int}"
    return str(int)


class ChessComClient:

    GAME_URL = "https://api.chess.com/pub/player/{}/games/{}/{}"

    def __init__(self, engine_path: str, depth: int = 20):
        self.analyzer = GameAnalysis(engine_path, depth)

    def analyse_games_for_player(self, player_name: str, year: int, month: int) -> List[AnalysedGame]:
        url = self.GAME_URL.format(player_name, year, _pad_int(month))
        response = requests.get(url).json()
        analyzed_games: List[AnalysedGame] = []
        for game in response["games"]:
            analyzed_games.append(self.analyzer.analyse_game_from_pgn_str(game['pgn']))
        return analyzed_games


if __name__ == '__main__':
    analyzed_games = ChessComClient("/usr/local/bin/stockfish", 20).analyse_games_for_player("WhySoBad909", 2021, 6)
    for game in analyzed_games:
        game.write_to_pgn_name_from_metadata()
