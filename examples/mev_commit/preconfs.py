import asyncio
import polars as pl
from hypermanager.events import EventConfig
from hypermanager.manager import HyperManager
from hypermanager.protocols.mev_commit import mev_commit_config


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

    opened_commits_config = EventConfig(
        name=mev_commit_config["OpenedCommitmentStored"].name,
        signature=mev_commit_config["OpenedCommitmentStored"].signature,
        column_mapping=mev_commit_config["OpenedCommitmentStored"].column_mapping,
    )

    unopened_commits_config = EventConfig(
        name=mev_commit_config["UnopenedCommitmentStored"].name,
        signature=mev_commit_config["UnopenedCommitmentStored"].signature,
        column_mapping=mev_commit_config["UnopenedCommitmentStored"].column_mapping,
    )

    commits_processed_config = EventConfig(
        name=mev_commit_config["CommitmentProcessed"].name,
        signature=mev_commit_config["CommitmentProcessed"].signature,
        column_mapping=mev_commit_config["CommitmentProcessed"].column_mapping,
    )

    # Query events using the event configuration and return the result as a Polars DataFrame
    commit_stores: pl.DataFrame = await manager.execute_event_query(
        opened_commits_config,
        tx_data=True,
    )

    encrypted_stores: pl.DataFrame = await manager.execute_event_query(
        unopened_commits_config,
        tx_data=True,
    )

    commits_processed: pl.DataFrame = await manager.execute_event_query(
        commits_processed_config,
        tx_data=True,
    )

    # merge dataframes into unified one
    commitments_df = (
        encrypted_stores.join(commit_stores, on="commitmentIndex", how="inner")
        .with_columns(("0x" + pl.col("txnHash")).alias("txnHash"))
        .join(
            commits_processed.select("commitmentIndex", "isSlash"),
            on="commitmentIndex",
            how="inner",
        )
    ).select(
        "block_number",
        "timestamp",
        "blockNumber",
        "txnHash",
        "bid",
        "commiter",
        "bidder",
        "isSlash",
        "decayStartTimeStamp",
        "decayEndTimeStamp",
        "dispatchTimestamp",
        "commitmentHash",
        "commitmentIndex",
        "commitmentDigest",
        "commitmentSignature",
        "revertingTxHashes",
        "bidHash",
        "bidSignature",
        "sharedSecretKey",
    )

    print(commitments_df.head(10))
    print(commitments_df.shape)

    commitments_df.write_parquet("commits_df.parquet")


# Entry point: Run the async function to execute the event queries
if __name__ == "__main__":
    # Use asyncio to run the asynchronous function in an event loop
    asyncio.run(get_events())
