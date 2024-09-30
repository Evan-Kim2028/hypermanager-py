import asyncio
import os
import polars as pl
from hypermanager.events import EventConfig
from hypermanager.manager import HyperManager
from hypermanager.protocols.across import (
    client_config,
    base_event_configs,
)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Queries all events for the Across protocol, which is a solver-intent bridge.
# This example shows how to interact programatically with the hypermanager protocols schemas to easily access and query events.
# If an event is not found, then it is skipped. All events are saved into a data folder in parquet files.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


async def get_events():
    # Iterate through relevant HyperSync clients and associated SpokePool addresses
    for client, spoke_pool_address in client_config.items():
        print(f"Querying events for {client.name}...")
        for base_event_config in base_event_configs:
            try:
                # Create a fresh EventConfig and assign the contract at runtime
                event_config = EventConfig(
                    name=base_event_config["name"],
                    signature=base_event_config["signature"],
                    contract=spoke_pool_address.value,  # Assign contract address dynamically
                    column_mapping=base_event_config["column_mapping"],
                )

                manager = HyperManager(url=client.client)

                # Query the events
                df: pl.DataFrame = await manager.execute_event_query(
                    event_config, save_data=False, tx_data=True, block_range=500
                )

                # Check if the DataFrame is empty
                if df.is_empty():
                    print(
                        f"No events found for {event_config.name} on {client.name}, continuing..."
                    )
                    continue

                # Process the non-empty DataFrame
                print(f"Events found for {event_config.name} on {client.name}:")
                print(df.shape)

                # Create the folder if it doesn't exist
                folder_path = f"data/across/{client.name}"
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)

                # Save the file with the new naming convention
                df.write_parquet(
                    f"{folder_path}/{event_config.name}_{client.name}.parquet"
                )
            except Exception as e:
                print(f"Error querying {event_config.name} on {client.name}: {e}")


if __name__ == "__main__":
    asyncio.run(get_events())
