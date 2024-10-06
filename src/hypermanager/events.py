from typing import Optional
import hypersync
from dataclasses import dataclass
from hypermanager.schema import COMMON_TRANSACTION_MAPPING, COMMON_BLOCK_MAPPING


@dataclass
class EventConfig:
    """
    Represents the configuration for a specific log event.

    This configuration includes the event name, its signature, the optional contract
    address, and an optional column mapping. The column mapping defines how the event's
    transaction and block data should be processed.

    Attributes:
        name (str): The human-readable name of the event.
        signature (str): The unique event signature (usually a hashed method/event name).
        contract (Optional[str]): The contract address associated with the event. If None,
            no contract address is required or used. Defaults to None.
        column_mapping (Optional[hypersync.ColumnMapping]): A mapping of columns for
            transaction and block data. Defaults to a common column mapping if not provided.
    """

    name: str
    signature: str
    contract: Optional[str] = None
    column_mapping: Optional[hypersync.ColumnMapping] = None

    def __post_init__(self):
        """
        Post-initialization method that sets the default column mapping if none is provided.

        This method is called automatically after the dataclass is initialized. If
        the `column_mapping` attribute is `None`, it will be assigned a default column
        mapping consisting of common transaction and block field mappings.
        """
        if self.column_mapping is None:
            self.column_mapping = self.get_default_column_mapping()

        # Ensure contract is lowercase if it is not None
        if self.contract is not None:
            self.contract = self.contract.lower()

    def get_topic(self) -> str:
        """
        Retrieves the topic (hashed signature) of the event for use in event filtering.

        This method converts the event signature into its corresponding topic hash
        using `hypersync.signature_to_topic0`.

        Returns:
            str: The topic (hashed signature) of the event.
        """
        return hypersync.signature_to_topic0(self.signature)

    @staticmethod
    def get_default_column_mapping() -> hypersync.ColumnMapping:
        """
        Returns a default column mapping for the event, which maps common transaction
        and block fields to their corresponding data types.

        The default mapping includes:
            - Transaction fields such as GAS_USED and MAX_PRIORITY_FEE_PER_GAS.
            - Block fields such as TIMESTAMP and BASE_FEE_PER_GAS.

        Returns:
            hypersync.ColumnMapping: A column mapping that defines how transaction and
            block data should be processed for the event.
        """
        return hypersync.ColumnMapping(
            transaction=COMMON_TRANSACTION_MAPPING, block=COMMON_BLOCK_MAPPING
        )
