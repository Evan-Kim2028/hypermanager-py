import asyncio
import os
import polars as pl
from hypermanager.events import EventConfig
from hypermanager.manager import HyperManager
from hypermanager.protocols.uniswap_v3 import uniswap_config


async def get_events():
    """
    Queries events from multiple blockchain clients for the Across Protocol.

    The function iterates through each client configured in the `client_config` dictionary,
    which contains HyperSync client instances and their corresponding SpokePool contract addresses.
    For each client, the function loops through the event configurations (e.g., event signatures and column mappings)
    and attempts to retrieve logs using the `HyperManager` interface.

    Each set of events, if found, is stored as a Parquet file in a `data/` directory,
    grouped by client name and event type.

    Note:
        The function skips events if they are not found or if errors occur during querying.
    """

    manager = HyperManager(url="https://base.hypersync.xyz")

    try:
        # Query events using the event configuration and return the result as a Polars DataFrame
        swaps_df: pl.DataFrame = await manager.execute_event_query(
            uniswap_config["Swap"],  # loads the swap event config
            tx_data=True,  # auto joins transaction and block data to the event
            block_range=10_000,  # query the most recent 10,000 blocks from the chain
        )
        print(f'queried {swaps_df.shape[0]} rows from {uniswap_config["Swap"].name}')
        print(swaps_df.columns)
        print(swaps_df.head(5))

        pools_df: pl.DataFrame = await manager.execute_event_query(
            uniswap_config["PoolCreated"],
            tx_data=True,
            block_range=10_000,
        )
        print(
            f'queried {pools_df.shape[0]} rows from {uniswap_config["PoolCreated"].name}'
        )
        print(pools_df.columns)
        print(pools_df.head(5))
    # Handle any exceptions that occur during the query process
    except Exception as e:
        print(f"Error querying {uniswap_config["Swap"].name}: {e}")


if __name__ == "__main__":
    # Execute the async get_events function using asyncio
    asyncio.run(get_events())
