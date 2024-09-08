from hypersync import TransactionField, DataType, BlockField

COMMON_TRANSACTION_MAPPING = {
    TransactionField.GAS_USED: DataType.FLOAT64,
    TransactionField.MAX_PRIORITY_FEE_PER_GAS: DataType.FLOAT64,
    TransactionField.MAX_FEE_PER_GAS: DataType.FLOAT64,
    TransactionField.GAS_USED: DataType.FLOAT64,
    TransactionField.EFFECTIVE_GAS_PRICE: DataType.FLOAT64,
    TransactionField.NONCE: DataType.UINT64,
}

COMMON_BLOCK_MAPPING = {
    BlockField.TIMESTAMP: DataType.UINT64,
    BlockField.BASE_FEE_PER_GAS: DataType.FLOAT64,
    BlockField.GAS_USED: DataType.UINT64,
}
