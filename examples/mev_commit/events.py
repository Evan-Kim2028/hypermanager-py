# The goal of this file is to showcase an example by getting mev-commit event logs.
# 1. define an event config
# 2. call the manager and get the logs

import asyncio

from hypermanager.events import EventConfig
from hypermanager.schema import COMMON_TRANSACTION_MAPPING, COMMON_BLOCK_MAPPING
from hypermanager.manager import HyperManager
from hypersync import ColumnMapping, DataType

unopened_commitment_event = EventConfig(
    name="UnopenedCommitmentStored",
    signature="UnopenedCommitmentStored(bytes32 indexed commitmentIndex,address committer,bytes32 commitmentDigest,bytes commitmentSignature,uint64 dispatchTimestamp)",
    contract="0xCAC68D97a56b19204Dd3dbDC103CB24D47A825A3".lower(),
    column_mapping=ColumnMapping(
        decoded_log={"dispatchTimestamp": DataType.UINT64},
        transaction=COMMON_TRANSACTION_MAPPING,
        block=COMMON_BLOCK_MAPPING,
    ),
)


async def get_unopened_commitments():
    manager = HyperManager(url="https://mev-commit.hypersync.xyz")
    unopened_commits_df = await manager.execute_event_query(unopened_commitment_event)
    print(unopened_commits_df)


# Run the async function
if __name__ == "__main__":
    asyncio.run(get_unopened_commitments())
