from uuid import uuid4


def pgn_title_from_metadata(metadata) -> str:
    return f'{metadata["White"]}_{metadata["Black"]}_{metadata["Date"]}_{str(uuid4())}.pgn'
