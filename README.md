# Blunder Wunder

Supports automated analysis of Chess games from a PGN file. Providing, a similar output to
what online game analyzers provide. A compatible UCI engine is required to run analysis.

```python
from blunder_wunder import GameAnalysis
from 

analyzer = GameAnalysis("/usr/local/bin/stockfish", depth=20)
analyzed_game = analyzer.analyse_game_from_pgn(
        "/Users/edmundmartin/PycharmProjects/blunder_wunder/test_pgn") 
mistakes = analyzed_game.list_mistakes("WhySoBad909")
print(mistakes)
```

## Chess.com Integration
```python
from blunder_wunder.chess_com import ChessComClient

analyzed_games = ChessComClient("/usr/local/bin/stockfish", 20).analyse_games_for_player("PlayerName", 2021, 6)
for game in analyzed_games:
    game.write_to_pgn_name_from_metadata()
```
Blunder Wunder integrates with the Chess.com API allowing for automated analysis of all games from a particular month. 
These can even then be examined from other Python programs, or can be dumped PGNs which contain notes in regards to 
inaccuracies, mistakes and the suggested computer move.

If you play too much Chess (like me), analysing all games from a particular month at a significant depth will take a 
considerable amount of time. As such it is possible to simply download the PGNs for a particular month for later analysis.
```python
from blunder_wunder.chess_com import ChessComClient

ChessComClient.save_pgns_for_player("PlayerName", 2021, 6, "output_folder_path")
```

Analysing existing PGNs can be done in a manner similar to the snippet below:
```python
import glob
import os
from blunder_wunder import GameAnalysis
from blunder_wunder.utils import pgn_title_from_metadata


files = glob.glob("/Users/username/chess/test_pgns/*.pgn")
print(f"Analysing {len(files)} games")
analysis_engine = GameAnalysis("/usr/local/bin/stockfish", 20)
for idx, file in enumerate(files):
    print(idx, file)
    analysed_game = analysis_engine.analyse_game_from_pgn(file)
    analysed_game.write_to_pgn(os.path.join("/Users/username/chess/june_pgns", pgn_title_from_metadata(analysed_game.metadata)))
```