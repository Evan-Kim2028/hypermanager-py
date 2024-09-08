# Example File: Retrieve MEV-Commit Event Logs
# This file demonstrates how to define an event configuration and query logs
# from the MEV-Commit system using the HyperManager and Hypersync libraries.
#
# Steps:
# 1. Define the event configuration (name, signature, contract, column mapping).
# 2. Use the HyperManager to query event logs from the blockchain.
# 3. Showcase different ways to query:
#    - All historical events.
#    - Events from a specific block onward.
#    - Events within a recent block range.

import asyncio
import polars as pl

from hypermanager.events import EventConfig
from hypermanager.schema import COMMON_TRANSACTION_MAPPING, COMMON_BLOCK_MAPPING
from hypermanager.manager import HyperManager
from hypersync import ColumnMapping, DataType

# Define the configuration for the "UnopenedCommitmentStored" event.
# This includes its signature, the contract address, and how the event data should be processed.
unopened_commitment_event = EventConfig(
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


# Asynchronous function to retrieve logs for the UnopenedCommitmentStored event
async def get_unopened_commitments():
    """
    Fetch event logs for the UnopenedCommitmentStored event from the MEV-Commit system.
    Demonstrates three different queries:
    1. All historical events.
    2. Events from a specific block onward.
    3. Events within the most recent block range.

    The results are returned as Polars DataFrames and their shapes are printed.
    """
    # Initialize the HyperManager with the MEV-Commit endpoint URL
    manager = HyperManager(url="https://mev-commit.hypersync.xyz")

    # 1. Retrieve all historical events for the "UnopenedCommitmentStored" event
    unopened_commits_historical_df: pl.DataFrame = await manager.execute_event_query(
        unopened_commitment_event
    )

    # 2. Retrieve events starting from a specific block (e.g., block 5,000,000)
    unopened_commits_from_df: pl.DataFrame = await manager.execute_event_query(
        unopened_commitment_event, from_block=5_000_000
    )

    # 3. Retrieve events from the most recent 10,000 blocks
    unopened_commits_range_df: pl.DataFrame = await manager.execute_event_query(
        unopened_commitment_event, block_range=10_000
    )

    # Print the number of rows and columns (shape) of each DataFrame result
    print("Historical DataFrame shape:", unopened_commits_historical_df.shape)
    print("From Block 5,000,000 DataFrame shape:", unopened_commits_from_df.shape)
    print("Recent 10,000 Block Range DataFrame shape:", unopened_commits_range_df.shape)


# Entry point: Run the async function to execute the event queries
if __name__ == "__main__":
    # Use asyncio to run the asynchronous function in an event loop
    asyncio.run(get_unopened_commitments())
