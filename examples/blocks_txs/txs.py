import asyncio
import polars as pl

from hypermanager.manager import HyperManager

hypersync_client: str = "https://eth.hypersync.xyz"


async def get_events():
    manager = HyperManager(url=hypersync_client)

    df: pl.DataFrame = await manager.get_txs(block_range=100)

    print(df.head(5))

    print(f"schema: {df.schema}")
    print(df.select("base_fee_per_gas").head(5))


if __name__ == "__main__":
    asyncio.run(get_events())
