from hypersync import TransactionField, DataType, BlockField

# Common transaction column mappings reused across events
COMMON_TRANSACTION_MAPPING = {
    TransactionField.GAS_USED: DataType.FLOAT64,
    TransactionField.MAX_PRIORITY_FEE_PER_GAS: DataType.FLOAT64,
    TransactionField.MAX_FEE_PER_GAS: DataType.FLOAT64,
    TransactionField.EFFECTIVE_GAS_PRICE: DataType.FLOAT64,
    TransactionField.NONCE: DataType.UINT64,
    TransactionField.CHAIN_ID: DataType.UINT64,
    TransactionField.CUMULATIVE_GAS_USED: DataType.UINT64,
    TransactionField.VALUE: DataType.FLOAT64,
    TransactionField.GAS: DataType.UINT64,
    TransactionField.GAS_PRICE: DataType.FLOAT64,
}

COMMON_BLOCK_MAPPING = {
    BlockField.TIMESTAMP: DataType.UINT64,
    BlockField.BASE_FEE_PER_GAS: DataType.FLOAT64,
    BlockField.GAS_USED: DataType.UINT64,
    BlockField.NONCE: DataType.UINT64,
    BlockField.DIFFICULTY: DataType.UINT64,
    BlockField.SIZE: DataType.UINT64,
    BlockField.GAS_LIMIT: DataType.UINT64,
    BlockField.BLOB_GAS_USED: DataType.UINT64,
    BlockField.EXCESS_BLOB_GAS: DataType.UINT64,
}
