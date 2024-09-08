import asyncio
import polars as pl

from hypermanager.events import EventConfig
from hypermanager.schema import COMMON_TRANSACTION_MAPPING, COMMON_BLOCK_MAPPING
from hypermanager.manager import HyperManager
from hypersync import ColumnMapping, DataType


event_config = EventConfig(
    name="UnopenedCommitmentStored",
    signature=(
        "UnopenedCommitmentStored(bytes32 indexed commitmentIndex,"
        "address committer,bytes32 commitmentDigest,bytes commitmentSignature,"
        "uint64 dispatchTimestamp)"
    ),
    contract="0xCAC68D97a56b19204Dd3dbDC103CB24D47A825A3",
    column_mapping=ColumnMapping(
        decoded_log={"dispatchTimestamp": DataType.UINT64},
        transaction=COMMON_TRANSACTION_MAPPING,
        block=COMMON_BLOCK_MAPPING,
    ),
)


async def get_events():
    """
    Fetch event logs for the UnopenedCommitmentStored event from the MEV-Commit system.
    Demonstrates three different queries:
    1. All historical events.
    2. Events from a specific block onward.
    3. Events within the most recent block range.

    The results are returned as Polars DataFrames and their shapes are printed.
    """
    manager = HyperManager(url="https://mev-commit.hypersync.xyz")

    # 1. Retrieve all historical events for the "UnopenedCommitmentStored" event
    unopened_commits_historical_df: pl.DataFrame = await manager.execute_event_query(
        event_config
    )

    # 2. Retrieve events starting from a specific block (e.g., block 5,000,000)
    unopened_commits_from_df: pl.DataFrame = await manager.execute_event_query(
        event_config, from_block=5_000_000
    )

    # 3. Retrieve events from the most recent 10,000 blocks
    unopened_commits_range_df: pl.DataFrame = await manager.execute_event_query(
        event_config, block_range=10_000
    )

    # Print the number of rows and columns (shape) of each DataFrame result
    print("Historical DataFrame shape:", unopened_commits_historical_df.shape)
    print("From Block 5,000,000 DataFrame shape:", unopened_commits_from_df.shape)
    print("Recent 10,000 Block Range DataFrame shape:", unopened_commits_range_df.shape)


# Entry point: Run the async function to execute the event queries
if __name__ == "__main__":
    # Use asyncio to run the asynchronous function in an event loop
    asyncio.run(get_events())
