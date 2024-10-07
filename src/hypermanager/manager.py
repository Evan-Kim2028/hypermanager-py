import polars as pl
from typing import List, Optional
from functools import lru_cache
import hypersync

from dataclasses import dataclass, field
from hypermanager.decorators import timer
from hypermanager.helpers import address_to_topic
from hypermanager.schema import COMMON_TRANSACTION_MAPPING, COMMON_BLOCK_MAPPING
from hypermanager.events import EventConfig


@dataclass
class HyperManager:
    url: str
    client: hypersync.HypersyncClient = field(init=False)

    def __post_init__(self):
        self.client = hypersync.HypersyncClient(hypersync.ClientConfig(url=self.url))

    def __hash__(self):
        return hash(self.url)  # Make the object hashable based on URL

    async def _get_height(self) -> int:
        """
        Get the current block height from the blockchain.

        Returns:
            int: The current block height.
        """
        return await self.client.get_height()

    def _create_query(
        self,
        from_block: int,
        to_block: int,
        logs: List[hypersync.LogSelection],
        transactions: Optional[List[hypersync.TransactionSelection]] = None,
        blocks: Optional[List[hypersync.BlockSelection]] = None,
    ) -> hypersync.Query:
        """
        Create a Hypersync query object for querying blockchain data.

        Args:
            from_block (int): The starting block number for the query.
            to_block (int): The ending block number for the query.
            logs (List[hypersync.LogSelection]): A list of log selections to filter the query.
            transactions (Optional[List[hypersync.TransactionSelection]]): Optional transaction selections for the query.

        Returns:
            hypersync.Query: The constructed query object.
        """
        return hypersync.Query(
            from_block=from_block,
            to_block=to_block,
            logs=logs,
            transactions=transactions or [],
            blocks=blocks or [],
            field_selection=hypersync.FieldSelection(
                log=[e.value for e in hypersync.LogField],
                transaction=[e.value for e in hypersync.TransactionField],
                block=[e.value for e in hypersync.BlockField],
            ),
        )

    async def _collect_data(
        self,
        query: hypersync.Query,
        config: hypersync.StreamConfig,
        save_data: bool,
        tx_data: bool = False,
    ) -> Optional[pl.DataFrame]:
        """
        Collect logs data using the Hypersync client and return it as a Polars DataFrame or save it as a parquet file in a "data" folder.

        Args:
            query (hypersync.Query): The query object to execute.
            config (hypersync.StreamConfig): The configuration for the data stream.
            save_data (bool): Whether to save the data as a parquet file.
            tx_data (bool): Whether to include transaction data in the result.

        Returns:
            Optional[pl.DataFrame]: The collected data as a Polars DataFrame, or None if no data is returned.
        """
        if save_data:
            return await self.client.collect_parquet("data", query, config)
        else:
            data = await self.client.collect_arrow(query, config)
            decoded_logs_df = pl.from_arrow(data.data.decoded_logs)
            logs_df = pl.from_arrow(data.data.logs)
            transactions_df = pl.from_arrow(data.data.transactions)
            blocks_df = pl.from_arrow(data.data.blocks)

            # Check for empty data and handle the case gracefully
            if (
                decoded_logs_df.is_empty()
                and logs_df.is_empty()
                and transactions_df.is_empty()
                and blocks_df.is_empty()
            ):
                raise ValueError("All queries returned empty results.")

            txs_blocks_df = transactions_df.join(
                blocks_df.select(
                    "number",
                    "extra_data",
                    "timestamp",
                    "base_fee_per_gas",
                    "gas_used",
                    "parent_beacon_block_root",
                ).rename({"number": "block_number"}),
                on="block_number",
                how="left",
                suffix="_block",
            )

        if decoded_logs_df.is_empty() or logs_df.is_empty():
            # If both decoded_logs_df and logs_df are empty
            if txs_blocks_df.is_empty():
                return None  # All three DataFrames are empty
            else:
                # Return txs_blocks_df if it's not empty
                return txs_blocks_df.select(
                    "hash",
                    "block_number",
                    "extra_data",
                    "to",
                    "from",
                    "nonce",
                    "type",
                    "block_hash",
                    "timestamp",
                    "base_fee_per_gas",
                    "gas_used_block",
                    "parent_beacon_block_root",
                    "max_priority_fee_per_gas",
                    "max_fee_per_gas",
                    "effective_gas_price",
                    "gas_used",
                    "blob_versioned_hashes",
                )

        if tx_data:
            result_df = (
                decoded_logs_df.hstack(logs_df.select("transaction_hash"))
                .rename({"transaction_hash": "hash"})
                .join(
                    txs_blocks_df.select(
                        "hash",
                        "block_number",
                        "extra_data",
                        "to",
                        "from",
                        "nonce",
                        "type",
                        "block_hash",
                        "timestamp",
                        "base_fee_per_gas",
                        "gas_used_block",
                        "max_priority_fee_per_gas",
                        "max_fee_per_gas",
                        "effective_gas_price",
                        "gas_used",
                        "chain_id",
                    ),
                    on="hash",
                    how="left",
                )
            )
            return result_df
        else:
            return decoded_logs_df

    async def _get_block_range(
        self,
        from_block: Optional[int] = None,
        to_block: Optional[int] = None,
        block_range: Optional[int] = None,
    ) -> dict[str, int]:
        """
        Determine the block range to be used in a query.

        Args:
            from_block (Optional[int]): The starting block number, optional.
            to_block (Optional[int]): The ending block number, optional.
            block_range (Optional[int]): The range of blocks, optional.

        Returns:
            dict[str, int]: A dictionary containing 'from_block' and 'to_block'.
        """
        if to_block is None:
            to_block = await self._get_height()  # Await only once

        from_block = from_block or (to_block - block_range if block_range else 0)

        return {"from_block": from_block, "to_block": to_block}

    def _create_event_query(
        self,
        event_config: EventConfig,
        from_block: int,
        to_block: int,
        address: Optional[str] = None,
    ) -> hypersync.Query:
        """
        Create a query for a specific event based on the event signature.

        If the `contract` in the `EventConfig` class is None, then the query will use wildcard indexing to find the
        event logs. See docs here - https://docs.envio.dev/docs/HyperIndex/wildcard-indexing


        Args:
            event_signature (str): The event signature to query.
            from_block (int): The starting block number for the query.
            to_block (int): The ending block number for the query.
            address (Optional[str]): Optional address to filter the event logs.

        Returns:
            hypersync.Query: The constructed query object.

        Raises:
            ValueError: If the event signature is not supported.
        """

        topic0 = event_config.get_topic()
        topics = [[topic0]]
        if address:
            topics.append([address_to_topic(address.lower())])

        # handle the case where contract is not provided
        if event_config.contract is None:
            return self._create_query(
                from_block=from_block,
                to_block=to_block,
                logs=[hypersync.LogSelection(topics=topics)],
            )

        return self._create_query(
            from_block=from_block,
            to_block=to_block,
            logs=[
                hypersync.LogSelection(address=[event_config.contract], topics=topics)
            ],
        )

    @timer
    async def execute_event_query(
        self,
        event_config: EventConfig,
        from_block: Optional[int] = None,
        to_block: Optional[int] = None,
        block_range: Optional[int] = None,
        save_data: bool = False,
        print_time: bool = True,
        address: Optional[str] = None,
        tx_data: bool = True,
    ) -> Optional[pl.DataFrame]:
        """
        Execute a query for a specific event by its signature and collect the data.

        If the `contract` in the `EventConfig` class is None, then the query will use wildcard indexing to find the
        event logs. See docs here - https://docs.envio.dev/docs/HyperIndex/wildcard-indexing


        Args:
            event_name (str): The name of the event to query.
            from_block (Optional[int]): The starting block number for the query. Defaults to None, which will use the latest block.
            to_block (Optional[int]): The ending block number for the query. Defaults to None, which will use the latest block.
            block_range (Optional[int]): Specifies a block range to query if from_block and to_block are not provided. Optional.
            save_data (bool): Whether to save the data as a parquet file. Defaults to False.
            print_time (bool): Whether to print the execution time of the query. Defaults to True.
            address (Optional[str]): The contract address to filter the event logs. Defaults to None.
            tx_data (bool): Whether to include transaction data. Defaults to True.

        Returns:
            Optional[pl.DataFrame]: The collected data as a Polars DataFrame, or None if no data is returned.

        Raises:
            ValueError: If no data is returned for the specified event name or if the query range is invalid.
        """
        # Determine the block range for the query
        block_range_dict = await self._get_block_range(
            from_block, to_block, block_range
        )

        # Create the query object for the specified event
        query = self._create_event_query(
            event_config,
            block_range_dict["from_block"],
            block_range_dict["to_block"],
            address,
        )

        # Retrieve the column mapping for the event, if available
        column_mapping = event_config.column_mapping

        # Configure the stream settings for the data collection
        config = hypersync.StreamConfig(
            hex_output=hypersync.HexOutput.PREFIXED,
            event_signature=event_config.signature,
            column_mapping=column_mapping,
        )

        # Collect the data based on the query and configuration
        result = await self._collect_data(query, config, save_data, tx_data=tx_data)

        # Handle the case where no data is returned
        if result is None:
            raise ValueError(f"No data returned for event name: {event_config.name} from blocks {
                             block_range_dict['from_block']} to {block_range_dict['to_block']}")

        return result

    @timer
    async def get_txs(
        self,
        from_block: Optional[int] = None,
        to_block: Optional[int] = None,
        block_range: Optional[int] = None,
        save_data: bool = False,
        print_time: bool = True,
        blocks_only=False,
    ) -> Optional[pl.DataFrame]:
        """
        Query for blocks and transactions within a specified block range and optionally save results.

        Args:
            from_block (Optional[int]): The starting block number, optional.
            to_block (Optional[int]): The ending block number, optional.
            block_range (Optional[int]): The range of blocks to query, optional.
            save_data (bool): Whether to save the data as a parquet file.
            print_time (bool): Whether to print the execution time of the query.

        Returns:
            Optional[pl.DataFrame]: The collected blocks and transactions data as a Polars DataFrame, or None if no data is returned.
        """
        block_range_dict = await self._get_block_range(
            from_block, to_block, block_range
        )

        query = self._create_query(
            from_block=block_range_dict["from_block"],
            to_block=block_range_dict["to_block"],
            logs=[],
            blocks=[hypersync.BlockSelection()],
            transactions=[hypersync.TransactionSelection()],
        )

        config = hypersync.StreamConfig(
            hex_output=hypersync.HexOutput.PREFIXED,
            column_mapping=hypersync.ColumnMapping(
                transaction=COMMON_TRANSACTION_MAPPING, block=COMMON_BLOCK_MAPPING
            ),
        )
        return await self._collect_data(query, config, save_data)

    @timer
    async def search_txs(
        self, txs: str | list[str], save_data: bool = False, print_time: bool = True
    ) -> Optional[pl.DataFrame]:
        """
        Query for specific transactions or a list of transactions

        Args:
            save_data (bool): Whether to save the data as a parquet file.
            print_time (bool): Whether to print the execution time of the query.

        Returns:
            Optional[pl.DataFrame]: The collected blocks and transactions data as a Polars DataFrame, or None if no data is returned.
        """
        # Ensure txs is a list
        if isinstance(txs, str):
            txs = [txs]  # Convert single string to a list

        block_range_dict = await self._get_block_range(from_block=None)

        query = self._create_query(
            from_block=0,
            to_block=block_range_dict["to_block"],
            logs=[],
            transactions=[hypersync.TransactionSelection(hash=txs)],
        )

        config = hypersync.StreamConfig(
            hex_output=hypersync.HexOutput.PREFIXED,
            column_mapping=hypersync.ColumnMapping(
                transaction=COMMON_TRANSACTION_MAPPING, block=COMMON_BLOCK_MAPPING
            ),
        )
        return await self._collect_data(query, config, save_data)

    @timer
    async def get_blocks(
        self,
        from_block: Optional[int] = None,
        to_block: Optional[int] = None,
        block_range: Optional[int] = None,
        save_data: bool = False,
        print_time: bool = True,
    ) -> Optional[pl.DataFrame]:
        """
        Query for blocks within a specified block range and optionally save results.

        Args:
            from_block (Optional[int]): The starting block number, optional.
            to_block (Optional[int]): The ending block number, optional.
            block_range (Optional[int]): The range of blocks to query, optional.
            save_data (bool): Whether to save the data as a parquet file.
            print_time (bool): Whether to print the execution time of the query.

        Returns:
            Optional[pl.DataFrame]: The collected block data as a Polars DataFrame, or None if no data is returned.
        """
        # Get the block range to query
        block_range_dict = await self._get_block_range(
            from_block, to_block, block_range
        )

        # Create a query for blocks only
        query = self._create_query(
            from_block=block_range_dict["from_block"],
            to_block=block_range_dict["to_block"],
            logs=[],
            transactions=[],
            blocks=[hypersync.BlockSelection()],
        )

        # Configure the stream settings for blocks
        config = hypersync.StreamConfig(
            hex_output=hypersync.HexOutput.PREFIXED,
            column_mapping=hypersync.ColumnMapping(block=COMMON_BLOCK_MAPPING),
        )

        # Collect block data
        data = await self.client.collect_arrow(query, config)
        blocks_df = pl.from_arrow(data.data.blocks)

        # Save data as parquet file if required
        if save_data and not blocks_df.is_empty():
            blocks_df.write_parquet("blocks_data.parquet")

        return blocks_df if not blocks_df.is_empty() else None
