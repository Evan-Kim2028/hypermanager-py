"""
Example of Multi-chain Event Query for Across Protocol

This script demonstrates how to query events from the Across Protocol using the HyperManager framework.
Across is a bridge protocol that allows users to transfer assets between different chains. This example
shows how to programmatically interact with HyperManager protocols, schemas, and event configurations to
efficiently query events from different blockchain clients.

The events queried in this example are dynamically pulled from different chains, and the results are saved
as Parquet files to the 'data' folder. If no events are found for a particular configuration or chain, the
script skips that event.

How to run:
Run the script via:
    python examples/across/spoke_pool_v3.py

"""

import asyncio
import os
import polars as pl
from hypermanager.events import EventConfig
from hypermanager.manager import HyperManager
from hypermanager.protocols.across import (
    client_config,
    across_config,
)


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

    # Iterate through the different HyperSync clients and their associated SpokePool addresses
    for client, spoke_pool_address in client_config.items():
        print(f"Querying events for {client.name}...")
        print(f"SpokePool Address: {spoke_pool_address.value}")

        # **Modified Loop**: Iterate over the values of the across_config dictionary
        for base_event_config in across_config.values():
            try:
                # Initialize the HyperManager with the hypersync URL
                manager = HyperManager(url=client.client)

                # Query events using the event configuration and return the result as a Polars DataFrame
                df: pl.DataFrame = await manager.execute_event_query(
                    base_event_config,
                    # save_data=True,
                    tx_data=True,
                    block_range=10_000,  # query the most recent 10,000 blocks from each chain
                )

                # Check if any events were found
                if df.is_empty():
                    print(
                        f"No events found for {base_event_config.name} on {client.name}, continuing..."
                    )
                    continue  # Move to the next event if none found

                # Process the DataFrame if events are found
                print(f"Events found for {base_event_config.name} on {client.name}:")
                print(df.shape)  # Print the number of rows and columns

            # Handle any exceptions that occur during the query process
            except Exception as e:
                print(f"Error querying {base_event_config.name} on {
                      client.name}: {e}")


if __name__ == "__main__":
    # Execute the async get_events function using asyncio
    asyncio.run(get_events())
