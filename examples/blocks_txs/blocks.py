import asyncio
import polars as pl

from hypermanager.manager import HyperManager

hypersync_client: str = "https://eth.hypersync.xyz"


async def get_events():
    manager = HyperManager(url=hypersync_client)

    df: pl.DataFrame = await manager.get_blocks(
        from_block=20050000, to_block=20160000, save_data=True
    )

    df.write_parquet("blocks.parquet")

    # print(df.head(5))

    # print(f"schema: {df.schema}")
    # print(df.select("base_fee_per_gas").head(5))


if __name__ == "__main__":
    asyncio.run(get_events())
