import asyncio
import polars as pl

from hypermanager.manager import HyperManager

hypersync_client: str = "https://eth.hypersync.xyz"


async def get_events():
    manager: HyperManager = HyperManager(url=hypersync_client)

    # await manager.get_txs(from_block=20129500, to_block=20160000, save_data=True)
    df: pl.DataFrame = await manager.get_txs(from_block=20133000, to_block=20150000)
    print(df.schema)
    df.select("block_number", "extra_data").unique().write_parquet(
        "tx_extra_data.parquet"
    )


if __name__ == "__main__":
    asyncio.run(get_events())
