# Blunder Wunder

Supports automated analysis of Chess games from a PGN file. Providing, a similar output to
what online game analyzers provide. A compatible UCI engine is required to run analysis.

```python
from blunder_wunder import GameAnalysis

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

## Example Output PGN
Blunder Wunder can output analysed games to PGN, for further analysis in your favorite Chess software. An example
of such output can be found below:
```
[Event "Live Chess"]
[Site "Chess.com"]
[Date "2021.06.22"]
[Round "-"]
[White "SxyUncleFlxy"]
[Black "WhySoBad909"]
[Result "0-1"]
[Accuracy "White Accuracy Score: 79.0625%, Black Accuracy Score: 90.625%"]
[Annotator "https://github.com/EdmundMartin/blunder_wunder"]
[BlackElo "825"]
[CurrentPosition "3r1rk1/pb2qppp/1p2pn2/1B6/n4B2/P1P2N2/5PPP/1R3RK1 w - -"]
[ECO "A40"]
[ECOUrl "https://www.chess.com/openings/Queens-Pawn-Opening-Horwitz-Defense-2.Bf4"]
[EndDate "2021.06.22"]
[EndTime "22:10:58"]
[Link "https://www.chess.com/game/live/18138694879"]
[StartTime "22:08:25"]
[Termination "WhySoBad909 won by resignation"]
[TimeControl "120+1"]
[Timezone "UTC"]
[UTCDate "2021.06.22"]
[UTCTime "22:08:25"]
[WhiteElo "788"]

1. d4 { [%eval 0.11] } 1... e6 { [%eval 0.46] } 
2. Bf4 { [%eval 0.02] } 2... b6 { b7b6 was a inaccuracy, suggested engine move was c7c5 [%eval 0.69] } 
3. Nf3 { [%eval 0.23] } 3... Bb7 { [%eval 0.18] } 4. e3 { [%eval 0.21] } 
4... Nf6 { [%eval 0.14] } 5. c4 { [%eval 0.18] } 5... c5 { [%eval 0.35] } 6. Nc3 { [%eval 0.15] } 6... cxd4 { [%eval 0.50] } 
7. exd4 { [%eval -0.03] } 7... Bb4 { [%eval 0.32] } 8. a3 { [%eval -0.40] } 8... Bxc3+ { [%eval 0.00] } 9. bxc3 { [%eval -0.18] } 
9... O-O { [%eval 0.19] } 10. Bd3 { [%eval -0.23] } 10... d6 { [%eval -0.16] } 11. O-O { [%eval 0.06] } 
11... Qe7 { [%eval 0.48] } 12. Rb1 { [%eval 0.11] } 12... Nbd7 { [%eval 0.62] } 13. c5 { c4c5 was a mistake, suggested engine move was f1e1 [%eval -2.04] } 
13... dxc5 { [%eval -1.62] } 14. dxc5 { [%eval -1.36] } 14... Nxc5 { [%eval -0.80] } 15. Bb5 { d3b5 was a blunder, suggested engine move was f4d6 [%eval -3.79] } 
15... Rad8 { [%eval -4.27] } 16. Qa4 { d1a4 was a blunder, suggested engine move was d1e2 [%eval -9.70] } 16... Nxa4 { [%eval -9.24] } 0-1
```