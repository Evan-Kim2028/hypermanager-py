import asyncio
import polars as pl

from hypermanager.events import EventConfig
from hypermanager.networks import HyperSyncClients
from hypermanager.schema import COMMON_TRANSACTION_MAPPING, COMMON_BLOCK_MAPPING
from hypermanager.manager import HyperManager
from hypersync import ColumnMapping, DataType

# contracts listed on optimism - https://optimistic.etherscan.io/accounts/label/stargate
# 10/24/24 Unsure what this is - https://github.com/stargate-protocol/stargate-v2/blob/main/packages/stg-evm-v2/src/StargateBase.sol # credits received/sent events.
contract: str = "0xe8CDF27AcD73a434D661C84887215F7598e7d0d3".lower()
hypersync_client: str = HyperSyncClients.OPTIMISM.client

events = EventConfig(
    name="Deposited",
    # 10/24/24 - it's a deposit into a liquidity pool. There are three main liqudity pools on optimism: ETH (native), USDC, and USDT. The events look
    # like they are the same for each pool so wildcard indexing would not neccesarily work here.
    # USDC - https://optimistic.etherscan.io/address/0xce8cca271ebc0533920c83d39f417ed6a0abb7d0
    # USDT - https://optimistic.etherscan.io/address/0x19cfce47ed54a88614648dc3f19a5980097007dd
    # ETH - https://optimistic.etherscan.io/address/0xe8cdf27acd73a434d661c84887215f7598e7d0d3
    # https://optimistic.etherscan.io/accounts/label/stargate
    signature="Deposited(address indexed payer, address indexed receiver, uint256 amountLD)",
    column_mapping=ColumnMapping(
        transaction=COMMON_TRANSACTION_MAPPING,
        block=COMMON_BLOCK_MAPPING,
        decoded_log={
            "amountLD": DataType.FLOAT64,
        },
    ),
)


async def get_events():
    try:
        manager = HyperManager(url=hypersync_client)
        df: pl.DataFrame = await manager.execute_event_query(
            events, tx_data=True, block_range=25_000
        )

        # Check if the DataFrame is empty
        if df.is_empty():
            print(f"No events found for {events.name}, continuing...")

        # Process the non-empty DataFrame
        print(f"Events found for {events.name}:")
        print(df)

        df.write_parquet("deposits.parquet")

    except Exception as e:
        print(f"Error querying {events.name}: {e}")


if __name__ == "__main__":
    asyncio.run(get_events())
