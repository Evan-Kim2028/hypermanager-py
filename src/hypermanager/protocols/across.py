from enum import Enum
from hypersync import ColumnMapping, DataType
from hypermanager.events import EventConfig
from hypermanager.networks import HyperSyncClients
from hypermanager.schema import COMMON_TRANSACTION_MAPPING, COMMON_BLOCK_MAPPING


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
client_config = {
    HyperSyncClients.ARBITRUM: SpokePoolAddresses.ARBITRUM,
    HyperSyncClients.BASE: SpokePoolAddresses.BASE,
    HyperSyncClients.BLAST: SpokePoolAddresses.BLAST,
    HyperSyncClients.ETHEREUM_MAINNET: SpokePoolAddresses.ETHEREUM,
    HyperSyncClients.LINEA: SpokePoolAddresses.LINEA,
    HyperSyncClients.OPTIMISM: SpokePoolAddresses.OPTIMISM,
    HyperSyncClients.SCROLL: SpokePoolAddresses.SCROLL,
}

# Base event configurations as a dictionary with event names as keys
across_config = {
    "V3FundsDeposited": EventConfig(
        name="V3FundsDeposited",
        signature=(
            "V3FundsDeposited(address inputToken,address outputToken,uint256 inputAmount,"
            "uint256 outputAmount,uint256 indexed destinationChainId,uint32 indexed depositId,"
            "uint32 quoteTimestamp,uint32 fillDeadline,uint32 exclusivityDeadline,"
            "address indexed depositor,address recipient,address exclusiveRelayer,bytes message)"
        ),
        column_mapping=ColumnMapping(
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
            decoded_log={
                "inputAmount": DataType.FLOAT64,
                "outputAmount": DataType.FLOAT64,
                "quoteTimestamp": DataType.INT64,
                "fillDeadline": DataType.UINT64,
                "exclusivityDeadline": DataType.INT64,
                "destinationChainId": DataType.UINT64,
                "depositId": DataType.UINT64,
            },
        ),
    ),
    "RequestedSpeedUpV3Deposit": EventConfig(
        name="RequestedSpeedUpV3Deposit",
        signature=(
            "RequestedSpeedUpV3Deposit(uint256 updatedOutputAmount,uint32 indexed depositId,"
            "address indexed depositor,address updatedRecipient,bytes updatedMessage,"
            "bytes depositorSignature)"
        ),
        column_mapping=ColumnMapping(
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
            decoded_log={
                "updatedOutputAmount": DataType.INT64,
                "depositId": DataType.UINT64,
            },
        ),
    ),
    "FilledV3Relay": EventConfig(
        name="FilledV3Relay",
        signature=(
            "FilledV3Relay(address inputToken,address outputToken,uint256 inputAmount,"
            "uint256 outputAmount,uint256 repaymentChainId,uint256 indexed originChainId,"
            "uint32 indexed depositId,uint32 fillDeadline,uint32 exclusivityDeadline,"
            "address exclusiveRelayer,address indexed relayer,address depositor,"
            "address recipient,bytes message,V3RelayExecutionEventInfo relayExecutionInfo)"
        ),
        column_mapping=ColumnMapping(
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
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
        ),
    ),
    "RequestedV3SlowFill": EventConfig(
        name="RequestedV3SlowFill",
        signature=(
            "RequestedV3SlowFill(address inputToken,address outputToken,uint256 inputAmount,"
            "uint256 outputAmount,uint256 indexed originChainId,uint32 indexed depositId,"
            "uint32 fillDeadline,uint32 exclusivityDeadline,address exclusiveRelayer,"
            "address depositor,address recipient,bytes message)"
        ),
        column_mapping=ColumnMapping(
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
            decoded_log={
                "inputAmount": DataType.FLOAT64,
                "outputAmount": DataType.FLOAT64,
                "quoteTimestamp": DataType.INT32,
                "fillDeadline": DataType.UINT64,
                "originChainId": DataType.UINT64,
            },
        ),
    ),
}
