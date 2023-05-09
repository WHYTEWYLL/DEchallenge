import argparse
import os
from datetime import date
from typing import List

import awswrangler as wr
import pandas as pd
from dotenv import load_dotenv
from web3 import Web3

from src.abi import contract_abi

load_dotenv()

w3 = Web3(
    Web3.HTTPProvider(
        f"https://eth-mainnet.g.alchemy.com/v2/{os.getenv('privateKeyToAccount')}"
    )
)

contract_address = "0xbaac2b4491727d78d2b78815144570b9f2fe8899"

checksum_address = w3.to_checksum_address(contract_address)
contract = w3.eth.contract(
    address=Web3.to_checksum_address(contract_address), abi=contract_abi
)


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


def fetch_transfer_logs(
    from_block: int, to_block: int, max_block_range: int = 2000
) -> List[dict]:
    """
    Load transfer logs to S3.
    """

    if to_block - from_block > max_block_range:
        subranges = create_subranges(from_block, to_block, max_block_range)
    else:
        subranges = [(from_block, to_block)]

    flattened_dicts = []
    for subrange_from, subrange_to in subranges:
        event_filter = contract.events.Transfer.get_logs(
            fromBlock=hex(subrange_from), toBlock=hex((subrange_to))
        )
        flattened_dicts += [flatten_attr_dicts(event) for event in event_filter]

    return flattened_dicts


def load_transfer_logs_to_s3(flattened_dicts: list, from_block: int, to_block: int):
    today = date.today()

    # Convert your flattened_dicts to JSON
    df = pd.DataFrame(flattened_dicts)

    # Upload the JSON data to S3
    wr.s3.to_csv(
        df,
        f"s3://my-transfer-logs/{contract_address}/{today}_{from_block}_{to_block}.csv",
        index=False,
        line_terminator="\n",
    )


def on_demand_transtactions(from_block: int, to_block: int):
    """
    Load transfer logs to S3.
    """
    coa = fetch_transfer_logs(from_block=from_block, to_block=to_block)
    print(len(coa))
    load_transfer_logs_to_s3(coa, from_block=from_block, to_block=to_block)
    print("Done!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--adhoc", type=bool, default=False)
    parser.add_argument("--from_block", type=int, default=13140651)
    parser.add_argument("--to_block", type=int, default=13150651)

    index_config = parser.parse_args()

    ## if adhoc was pass as aflagg plus a from value and a to value:
    # run ad_hoc function

    if index_config.adhoc:
        on_demand_transtactions(index_config.from_block, index_config.to_block)
    # else run listner
