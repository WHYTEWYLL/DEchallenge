from typing import List


def create_subranges(
    from_block: int, to_block: int, max_block_range: int = 2000
) -> List[tuple]:
    """
    Create subranges of blocks given the start and end blocks.
    """
    subranges = []
    while to_block >= from_block:
        end_block = from_block + max_block_range - 1
        if end_block > to_block:
            end_block = to_block
        subranges.append((from_block, end_block))
        from_block = end_block + 1
    return subranges


def flatten_attr_dicts(rawDict: dict) -> List[dict]:
    """
    Flatten attribute dictionaries.
    """
    return {
        "from": rawDict["args"]["from"],
        "to": rawDict["args"]["to"],
        "value": rawDict["args"]["value"],
        "event": rawDict["event"],
        "logIndex": rawDict["event"],
        "transactionIndex": rawDict["transactionIndex"],
        "transactionHash": rawDict["transactionHash"],
        "address": rawDict["address"],
        "blockHash": rawDict["blockHash"],
        "blockNumber": rawDict["blockNumber"],
    }
