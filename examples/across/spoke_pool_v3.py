import asyncio
import os
import polars as pl

from enum import Enum
from hypermanager.events import EventConfig
from hypermanager.networks import HyperSyncClients
from hypermanager.schema import COMMON_TRANSACTION_MAPPING, COMMON_BLOCK_MAPPING
from hypermanager.manager import HyperManager
from hypersync import ColumnMapping, DataType


# Enum for SpokePool addresses
class SpokePoolAddresses(Enum):
    ARBITRUM = "0xe35e9842fceaca96570b734083f4a58e8f7c5f2a"
    BASE = "0x09aea4b2242abC8bb4BB78D537A67a245A7bEC64"
    BLAST = "0x2D509190Ed0172ba588407D4c2df918F955Cc6E1"
    ETHEREUM = "0x5c7BCd6E7De5423a257D81B442095A1a6ced35C5"
    LINEA = "0x7E63A5f1a8F0B4d0934B2f2327DAED3F6bb2ee75"
    OPTIMISM = "0x6f26Bf09B1C792e3228e5467807a900A503c0281"
    SCROLL = "0x3bad7ad0728f9917d1bf08af5782dcbd516cdd96"


# Mapping relevant HyperSyncClients to SpokePoolAddresses
relevant_clients = {
    HyperSyncClients.ARBITRUM: SpokePoolAddresses.ARBITRUM,
    HyperSyncClients.BASE: SpokePoolAddresses.BASE,
    HyperSyncClients.BLAST: SpokePoolAddresses.BLAST,
    HyperSyncClients.ETHEREUM_MAINNET: SpokePoolAddresses.ETHEREUM,
    HyperSyncClients.LINEA: SpokePoolAddresses.LINEA,
    HyperSyncClients.OPTIMISM: SpokePoolAddresses.OPTIMISM,
    HyperSyncClients.SCROLL: SpokePoolAddresses.SCROLL,
}

# List of event configurations
base_event_configs = [
    {
        "name": "V3FundsDeposited",
        "signature": (
            "V3FundsDeposited(address inputToken,address outputToken,uint256 inputAmount,"
            "uint256 outputAmount,uint256 indexed destinationChainId,uint32 indexed depositId,"
            "uint32 quoteTimestamp,uint32 fillDeadline,uint32 exclusivityDeadline,"
            "address indexed depositor,address recipient,address exclusiveRelayer,bytes message)"
        ),
        "column_mapping": ColumnMapping(
            decoded_log={
                "inputAmount": DataType.FLOAT64,
                "outputAmount": DataType.FLOAT64,
                "quoteTimestamp": DataType.INT64,
                "fillDeadline": DataType.UINT64,
                "exclusivityDeadline": DataType.INT64,
                "destinationChainId": DataType.UINT64,
                "depositId": DataType.UINT64,
            },
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    },
    {
        "name": "RequestedSpeedUpV3Deposit",
        "signature": (
            "RequestedSpeedUpV3Deposit(uint256 updatedOutputAmount,uint32 indexed depositId,"
            "address indexed depositor,address updatedRecipient,bytes updatedMessage,"
            "bytes depositorSignature)"
        ),
        "column_mapping": ColumnMapping(
            decoded_log={
                "updatedOutputAmount": DataType.INT64,
                "depositId": DataType.UINT64,
            },
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    },
    {
        "name": "FilledV3Relay",
        "signature": (
            "FilledV3Relay(address inputToken,address outputToken,uint256 inputAmount,"
            "uint256 outputAmount,uint256 repaymentChainId,uint256 indexed originChainId,"
            "uint32 indexed depositId,uint32 fillDeadline,uint32 exclusivityDeadline,"
            "address exclusiveRelayer,address indexed relayer,address depositor,"
            "address recipient,bytes message,V3RelayExecutionEventInfo relayExecutionInfo)"
        ),
        "column_mapping": ColumnMapping(
            decoded_log={
                "inputAmount": DataType.FLOAT64,
                "outputAmount": DataType.FLOAT64,
                "quoteTimestamp": DataType.INT64,
                "fillDeadline": DataType.UINT64,
                "exclusivityDeadline": DataType.INT64,
                "originChainId": DataType.UINT64,
                "repaymentChainId": DataType.UINT64,
                "depositId": DataType.UINT64,
            },
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    },
    {
        "name": "RequestedV3SlowFill",
        "signature": (
            "RequestedV3SlowFill(address inputToken,address outputToken,uint256 inputAmount,"
            "uint256 outputAmount,uint256 indexed originChainId,uint32 indexed depositId,"
            "uint32 fillDeadline,uint32 exclusivityDeadline,address exclusiveRelayer,"
            "address depositor,address recipient,bytes message)"
        ),
        "column_mapping": ColumnMapping(
            decoded_log={
                "inputAmount": DataType.FLOAT64,
                "outputAmount": DataType.FLOAT64,
                "quoteTimestamp": DataType.INT32,
                "fillDeadline": DataType.UINT64,
                "originChainId": DataType.UINT64,
            },
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    },
]


async def get_events():
    # Iterate through relevant HyperSync clients and associated SpokePool addresses
    for client, spoke_pool_address in relevant_clients.items():
        print(f"querying events for {client.name}...")
        for base_event_config in base_event_configs:
            try:
                # Create a fresh EventConfig and assign the contract at runtime
                event_config = EventConfig(
                    name=base_event_config["name"],
                    signature=base_event_config["signature"],
                    contract=spoke_pool_address.value,  # Assign at runtime
                    column_mapping=base_event_config["column_mapping"],
                )

                manager = HyperManager(url=client.client)

                # Query the events
                df: pl.DataFrame = await manager.execute_event_query(
                    event_config, save_data=False, tx_data=True, block_range=2_000_000
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
                df.write_parquet(f"{folder_path}/{event_config.name}.parquet")
            except Exception as e:
                print(f"Error querying {event_config.name} on {client.name}: {e}")


if __name__ == "__main__":
    asyncio.run(get_events())
