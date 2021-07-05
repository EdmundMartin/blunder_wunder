from typing import List
import io
import os

import chess.pgn

import requests

from blunder_wunder.analysis import GameAnalysis
from blunder_wunder.game import AnalysedGame
from blunder_wunder.utils import pgn_title_from_metadata


def _pad_int(unpadded_int: int) -> str:
    if unpadded_int < 10:
        return f"0{unpadded_int}"
    return str(int)


class ChessComClient:

    GAME_URL = "https://api.chess.com/pub/player/{}/games/{}/{}"

    def __init__(self, engine_path: str, depth: int = 20):
        self.analyzer = GameAnalysis(engine_path, depth)

    @staticmethod
    def save_pgns_for_player(player_name: str, year: int, month: int, output_folder: str):
        url = ChessComClient.GAME_URL.format(player_name, year, _pad_int(month))
        response = requests.get(url).json()
        for game in response["games"]:
            new_pgn = chess.pgn.read_game(io.StringIO(game['pgn']))
            with open(os.path.join(output_folder, pgn_title_from_metadata(new_pgn.headers)), 'w') as output:
                output.write(str(new_pgn))

    def analyse_games_for_player(self, player_name: str, year: int, month: int) -> List[AnalysedGame]:
        url = self.GAME_URL.format(player_name, year, _pad_int(month))
        response = requests.get(url).json()
        analyzed_games: List[AnalysedGame] = []
        for game in response["games"]:
            analyzed_games.append(self.analyzer.analyse_game_from_pgn_str(game['pgn']))
        return analyzed_games
