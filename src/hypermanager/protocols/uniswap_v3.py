from hypermanager.events import EventConfig
from hypersync import ColumnMapping, DataType
from hypermanager.schema import COMMON_TRANSACTION_MAPPING, COMMON_BLOCK_MAPPING


# Base event configurations as a dictionary with event names as keys
uniswap_config = {
    "Swap": EventConfig(
        name="Swap",
        signature="Swap(address indexed sender, address indexed recipient, int256 amount0, int256 amount1, uint160 sqrtPriceX96, uint128 liquidity, int24 tick)",
        column_mapping=ColumnMapping(
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
            decoded_log={
                "amount0": DataType.FLOAT64,
                "amount1": DataType.FLOAT64,
                "liquidity": DataType.FLOAT64,
                "tick": DataType.FLOAT64,
                "sqrtPriceX96": DataType.FLOAT64,
            },
        ),
    ),
}
