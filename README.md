# Blunder Wunder

Supports automated analysis of Chess games from a PGN file. Providing, a similar output to
what online game analyzers provide. A compatible UCI engine is required to run analysis.

```python 3
from blunder_wunder import GameAnalysis

analyzer = GameAnalysis("/usr/local/bin/stockfish", depth=5)
analyzed_game = analyzer.analyse_game_from_pgn(
        "/Users/edmundmartin/PycharmProjects/blunder_wunder/test_pgn",
        Color.BLACK) 
mistakes = analyzed_game.list_mistakes("WhySoBad909")
print(mistakes)
```
