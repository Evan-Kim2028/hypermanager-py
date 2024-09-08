import asyncio
import polars as pl

from hypermanager.events import EventConfig
from hypermanager.schema import COMMON_TRANSACTION_MAPPING, COMMON_BLOCK_MAPPING
from hypermanager.manager import HyperManager
from hypersync import ColumnMapping, DataType

contract: str = "0x09aea4b2242abC8bb4BB78D537A67a245A7bEC64"
hypersync_client: str = "https://base.hypersync.xyz"

# List of event configurations
event_configs = [
    EventConfig(
        name="V3FundsDeposited",
        signature=(
            "V3FundsDeposited(address inputToken,address outputToken,uint256 inputAmount,"
            "uint256 outputAmount,uint256 indexed destinationChainId,uint32 indexed depositId,"
            "uint32 quoteTimestamp,uint32 fillDeadline,uint32 exclusivityDeadline,"
            "address indexed depositor,address recipient,address exclusiveRelayer,bytes message)"
        ),
        contract=contract,
        column_mapping=ColumnMapping(
            decoded_log={"fillDeadline": DataType.UINT32},
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    ),
    EventConfig(
        name="RequestedSpeedUpV3Deposit",
        signature=(
            "RequestedSpeedUpV3Deposit(uint256 updatedOutputAmount,uint32 indexed depositId,"
            "address indexed depositor,address updatedRecipient,bytes updatedMessage,"
            "bytes depositorSignature)"
        ),
        contract=contract,
        column_mapping=ColumnMapping(
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    ),
    EventConfig(
        name="FilledV3Relay",
        signature=(
            "FilledV3Relay(address inputToken,address outputToken,uint256 inputAmount,"
            "uint256 outputAmount,uint256 repaymentChainId,uint256 indexed originChainId,"
            "uint32 indexed depositId,uint32 fillDeadline,uint32 exclusivityDeadline,"
            "address exclusiveRelayer,address indexed relayer,address depositor,"
            "address recipient,bytes message,V3RelayExecutionEventInfo relayExecutionInfo)"
        ),
        contract=contract,
        column_mapping=ColumnMapping(
            decoded_log={"fillDeadline": DataType.UINT32},
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    ),
    EventConfig(
        name="RequestedV3SlowFill",
        signature=(
            "RequestedV3SlowFill(address inputToken,address outputToken,uint256 inputAmount,"
            "uint256 outputAmount,uint256 indexed originChainId,uint32 indexed depositId,"
            "uint32 fillDeadline,uint32 exclusivityDeadline,address exclusiveRelayer,"
            "address depositor,address recipient,bytes message)"
        ),
        contract=contract,
        column_mapping=ColumnMapping(
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    ),
]


async def get_events():
    manager = HyperManager(url=hypersync_client)

    for event_config in event_configs:
        try:
            df: pl.DataFrame = await manager.execute_event_query(
                event_config, save_data=False, block_range=20_000
            )

            # Check if the DataFrame is empty
            if df.is_empty():
                print(f"No events found for {event_config.name}, continuing...")
                continue

            # Process the non-empty DataFrame
            print(f"Events found for {event_config.name}:")
            print(df)

        except Exception as e:
            print(f"Error querying {event_config.name}: {e}")


if __name__ == "__main__":
    asyncio.run(get_events())
