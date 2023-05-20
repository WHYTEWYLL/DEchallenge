from __config__ import ALCHEMY_TOKEN, BASE_URL, CONTRACT_ADDRESS

import argparse
import asyncio
import json
import time
from typing import List

import awswrangler as wr
import pandas as pd
from web3 import Web3
from websockets import connect

from src.abi import contract_abi

from utils import create_subranges, flatten_attr_dicts

w3 = Web3(Web3.HTTPProvider(f"https://{BASE_URL}{ALCHEMY_TOKEN}"))

checksum_address = w3.to_checksum_address(CONTRACT_ADDRESS)

contract = w3.eth.contract(
    address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=contract_abi
)


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
            fromBlock=hex(subrange_from), toBlock=hex(subrange_to)
        )
        flattened_dicts += [flatten_attr_dicts(event) for event in event_filter]

    return flattened_dicts


def load_transfer_logs_to_s3(
    flattened_dicts: list, from_block: int = 0, to_block: int = 0
):
    now = int(time.time())
    # Convert your flattened_dicts to JSON
    df = pd.DataFrame(flattened_dicts)

    if from_block == to_block:
        file_name = f"{CONTRACT_ADDRESS}/part-{now}"
    file_name = f"{CONTRACT_ADDRESS}/part-{now}_{from_block}_{to_block}"
    # Upload the JSON data to S3
    wr.s3.to_csv(
        df,
        f"s3://my-transfer-logs/{file_name}.csv",
        index=False,
        line_terminator="\n",
    )


def on_demand_transtactions(from_block: int, to_block: int):
    """
    Load transfer logs to S3.
    """
    coa = fetch_transfer_logs(from_block=from_block, to_block=to_block)

    print(f"Uploading to S3... {(len(coa))} ")
    load_transfer_logs_to_s3(coa, from_block=from_block, to_block=to_block)
    print("Done!")


########################

### Have in consideration that:

# Returns logs that are included in new imported blocks and match the given filter criteria.
# In case of a chain reorganization previous sent logs that are on the old chain will be resent with the removed property set to true.
# Logs from transactions that ended up in the new chain are emitted. Therefore a subscription can emit logs for the same transaction multiple times.


async def listener_get_event():
    alc_websocket = f"wss://{BASE_URL}{ALCHEMY_TOKEN}"

    async with connect(alc_websocket) as ws:
        topic = Web3.keccak(text="Transfer(address,address,uint256)").hex()
        event = json.dumps(
            {
                "id": 1,
                "jsonrpc": "2.0",
                "method": "eth_subscribe",
                "params": [
                    "logs",
                    {
                        "address": "0xbaac2b4491727d78d2b78815144570b9f2fe8899",
                        "topics": [topic],
                    },
                ],
            }
        )

        await ws.send(event)
        subscription_response = await ws.recv()
        print("subscription response:", subscription_response)
        # you are now subscribed to the event
        flattened_dicts = []
        while True:
            try:
                message = await asyncio.wait_for(ws.recv(), timeout=60)
                if message:
                    flattened_dicts += [flatten_attr_dicts(event) for event in message]
                    load_transfer_logs_to_s3(flattened_dicts)
                pass
            except:
                print("Nothing new")
                pass


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
    else:
        loop = asyncio.get_event_loop()
        while True:
            loop.run_until_complete(listener_get_event())
