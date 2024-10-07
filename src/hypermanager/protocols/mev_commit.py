from hypersync import ColumnMapping, DataType
from hypermanager.schema import COMMON_TRANSACTION_MAPPING, COMMON_BLOCK_MAPPING


# Event configurations with event names as keys, including signatures, contracts, and optional column mappings
base_event_configs = {
    "NewL1Block": {
        "signature": "NewL1Block(uint256 indexed blockNumber,address indexed winner,uint256 indexed window)",
        "column_mapping": ColumnMapping(
            transaction=COMMON_TRANSACTION_MAPPING, block=COMMON_BLOCK_MAPPING
        ),
    },
    "CommitmentProcessed": {
        "signature": "CommitmentProcessed(bytes32 indexed commitmentIndex, bool isSlash)",
        "column_mapping": ColumnMapping(
            transaction=COMMON_TRANSACTION_MAPPING, block=COMMON_BLOCK_MAPPING
        ),
    },
    "BidderRegistered": {
        "signature": "BidderRegistered(address indexed bidder, uint256 depositedAmount, uint256 windowNumber)",
        "column_mapping": ColumnMapping(
            decoded_log={
                "depositedAmount": DataType.INT64,
                "windowNumber": DataType.INT64,
            },
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    },
    "BidderWithdrawal": {
        "signature": "BidderWithdrawal(address indexed bidder, uint256 window, uint256 amount)",
        "column_mapping": ColumnMapping(
            decoded_log={
                "amount": DataType.INT64,
                "window": DataType.INT64,
            },
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    },
    "OpenedCommitmentStored": {
        "signature": "OpenedCommitmentStored(bytes32 indexed commitmentIndex, address bidder, address commiter, uint256 bid, uint64 blockNumber, bytes32 bidHash, uint64 decayStartTimeStamp, uint64 decayEndTimeStamp, string txnHash, string revertingTxHashes, bytes32 commitmentHash, bytes bidSignature, bytes commitmentSignature, uint64 dispatchTimestamp, bytes sharedSecretKey)",
        "column_mapping": ColumnMapping(
            decoded_log={
                "bid": DataType.UINT64,
                "blockNumber": DataType.UINT64,
                "decayStartTimeStamp": DataType.UINT64,
                "decayEndTimeStamp": DataType.UINT64,
                "dispatchTimestamp": DataType.UINT64,
            },
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    },
    "FundsRetrieved": {
        "signature": "FundsRetrieved(bytes32 indexed commitmentDigest,address indexed bidder,uint256 window,uint256 amount)",
        "column_mapping": ColumnMapping(
            decoded_log={
                "window": DataType.UINT64,
                "amount": DataType.UINT64,
            },
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    },
    "FundsRewarded": {
        "signature": "FundsRewarded(bytes32 indexed commitmentDigest, address indexed bidder, address indexed provider, uint256 window, uint256 amount)",
        "column_mapping": ColumnMapping(
            decoded_log={
                "window": DataType.UINT64,
                "amount": DataType.UINT64,
            },
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    },
    "FundsSlashed": {
        "signature": "FundsSlashed(address indexed provider, uint256 amount)",
        "column_mapping": ColumnMapping(
            decoded_log={"amount": DataType.UINT64},
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    },
    "FundsDeposited": {
        "signature": "FundsDeposited(address indexed provider, uint256 amount)",
        "column_mapping": ColumnMapping(
            decoded_log={"amount": DataType.UINT64},
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    },
    "Withdraw": {
        "signature": "Withdraw(address indexed provider, uint256 amount)",
        "column_mapping": ColumnMapping(
            decoded_log={"amount": DataType.UINT64},
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    },
    "ProviderRegistered": {
        "signature": "ProviderRegistered(address indexed provider, uint256 stakedAmount, bytes blsPublicKey)",
        "column_mapping": ColumnMapping(
            decoded_log={"stakedAmount": DataType.UINT64},
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    },
    "UnopenedCommitmentStored": {
        "signature": "UnopenedCommitmentStored(bytes32 indexed commitmentIndex,address committer,bytes32 commitmentDigest,bytes commitmentSignature,uint64 dispatchTimestamp)",
        "column_mapping": ColumnMapping(
            decoded_log={"dispatchTimestamp": DataType.UINT64},
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    },
    # old validator staking
    # validator set stuff
    "Staked_old": {
        "signature": "Staked(address indexed txOriginator, bytes valBLSPubKey, uint256 amount)",
        "column_mapping": ColumnMapping(
            decoded_log={"amount": DataType.UINT64},
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    },
    # validator set stuff
    "Staked": {
        "signature": "Staked(address indexed msgSender, address indexed withdrawalAddress, bytes valBLSPubKey, uint256 amount)",
        "column_mapping": ColumnMapping(
            decoded_log={"amount": DataType.UINT64},
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    },
    "StakeAdded": {
        "signature": "StakeAdded(address indexed msgSender, address indexed withdrawalAddress, bytes valBLSPubKey, uint256 amount, uint256 newBalance)",
        "column_mapping": ColumnMapping(
            decoded_log={
                "amount": DataType.UINT64,
                "newBalance": DataType.UINT64,
            },
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    },
    "Unstaked": {
        "signature": "Unstaked(address indexed msgSender, address indexed withdrawalAddress, bytes valBLSPubKey, uint256 amount)",
        "column_mapping": ColumnMapping(
            decoded_log={"amount": DataType.UINT64},
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    },
    "StakeWithdrawn": {
        "signature": "StakeWithdrawn(address indexed msgSender, address indexed withdrawalAddress, bytes valBLSPubKey, uint256 amount)",
        "column_mapping": ColumnMapping(
            decoded_log={"amount": DataType.UINT64},
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    },
    "Slashed": {
        "signature": "Slashed(address indexed msgSender, address indexed slashReceiver, address indexed withdrawalAddress, bytes valBLSPubKey, uint256 amount)",
        "column_mapping": ColumnMapping(
            decoded_log={"amount": DataType.UINT64},
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    },
    "MinStakeSet": {
        "signature": "MinStakeSet(address indexed msgSender, uint256 newMinStake)",
        "column_mapping": ColumnMapping(
            decoded_log={"newMinStake": DataType.UINT64},
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    },
    "SlashAmountSet": {
        "signature": "SlashAmountSet(address indexed msgSender, uint256 newSlashAmount)",
        "column_mapping": ColumnMapping(
            decoded_log={"newSlashAmount": DataType.UINT64},
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    },
    "SlashOracleSet": {
        "signature": "SlashOracleSet(address indexed msgSender, address newSlashOracle)",
        "column_mapping": ColumnMapping(
            transaction=COMMON_TRANSACTION_MAPPING, block=COMMON_BLOCK_MAPPING
        ),
    },
    "SlashReceiverSet": {
        "signature": "SlashReceiverSet(address indexed msgSender, address newSlashReceiver)",
        "column_mapping": ColumnMapping(
            transaction=COMMON_TRANSACTION_MAPPING, block=COMMON_BLOCK_MAPPING
        ),
    },
    "UnstakePeriodBlocksSet": {
        "signature": "UnstakePeriodBlocksSet(address indexed msgSender, uint256 newUnstakePeriodBlocks)",
        "column_mapping": ColumnMapping(
            decoded_log={"newUnstakePeriodBlocks": DataType.UINT64},
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    },
    "VanillaRegistrySet": {
        "signature": "VanillaRegistrySet(address oldContract, address newContract)",
        "column_mapping": ColumnMapping(
            transaction=COMMON_TRANSACTION_MAPPING, block=COMMON_BLOCK_MAPPING
        ),
    },
    "MevCommitAVSSet": {
        "signature": "VanillaRegistrySet(address oldContract, address newContract)",
        "column_mapping": ColumnMapping(
            transaction=COMMON_TRANSACTION_MAPPING, block=COMMON_BLOCK_MAPPING
        ),
    },
    "OperatorRegistered": {
        "signature": "OperatorRegistered(address indexed operator)",
        "column_mapping": ColumnMapping(
            transaction=COMMON_TRANSACTION_MAPPING, block=COMMON_BLOCK_MAPPING
        ),
    },
    "OperatorDeregistrationRequested": {
        "signature": "OperatorDeregistrationRequested(address indexed operator)",
        "column_mapping": ColumnMapping(
            transaction=COMMON_TRANSACTION_MAPPING, block=COMMON_BLOCK_MAPPING
        ),
    },
    "OperatorDeregistered": {
        "signature": "OperatorDeregistered(address indexed operator)",
        "column_mapping": ColumnMapping(
            transaction=COMMON_TRANSACTION_MAPPING, block=COMMON_BLOCK_MAPPING
        ),
    },
    "ValidatorRegistered": {
        "signature": "ValidatorRegistered(bytes validatorPubKey, address indexed podOwner)",
        "column_mapping": ColumnMapping(
            transaction=COMMON_TRANSACTION_MAPPING, block=COMMON_BLOCK_MAPPING
        ),
    },
    "ValidatorDeregistrationRequested": {
        "signature": "ValidatorDeregistrationRequested(bytes validatorPubKey, address indexed podOwner)",
        "column_mapping": ColumnMapping(
            transaction=COMMON_TRANSACTION_MAPPING, block=COMMON_BLOCK_MAPPING
        ),
    },
    "ValidatorDeregistered": {
        "signature": "ValidatorDeregistered(bytes validatorPubKey, address indexed podOwner)",
        "column_mapping": ColumnMapping(
            transaction=COMMON_TRANSACTION_MAPPING, block=COMMON_BLOCK_MAPPING
        ),
    },
    "LSTRestakerRegistered": {
        "signature": "LSTRestakerRegistered(bytes chosenValidator, uint256 numChosen, address indexed lstRestaker)",
        "column_mapping": ColumnMapping(
            decoded_log={"numChosen": DataType.UINT64},
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    },
    "LSTRestakerDeregistrationRequested": {
        "signature": "LSTRestakerDeregistrationRequested(bytes chosenValidator, uint256 numChosen, address indexed lstRestaker)",
        "column_mapping": ColumnMapping(
            decoded_log={"numChosen": DataType.UINT64},
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    },
    "LSTRestakerDeregistered": {
        "signature": "LSTRestakerDeregistered(bytes chosenValidator, uint256 numChosen, address indexed lstRestaker)",
        "column_mapping": ColumnMapping(
            decoded_log={"numChosen": DataType.UINT64},
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    },
    "ValidatorFrozen": {
        "signature": "ValidatorFrozen(bytes validatorPubKey, address indexed podOwner)",
        "column_mapping": ColumnMapping(
            transaction=COMMON_TRANSACTION_MAPPING, block=COMMON_BLOCK_MAPPING
        ),
    },
    "ValidatorUnfrozen": {
        "signature": "ValidatorUnfrozen(bytes validatorPubKey, address indexed podOwner)",
        "column_mapping": ColumnMapping(
            transaction=COMMON_TRANSACTION_MAPPING, block=COMMON_BLOCK_MAPPING
        ),
    },
    "AVSDirectorySet": {
        "signature": "AVSDirectorySet(address indexed avsDirectory)",
        "column_mapping": ColumnMapping(
            transaction=COMMON_TRANSACTION_MAPPING, block=COMMON_BLOCK_MAPPING
        ),
    },
    "StrategyManagerSet": {
        "signature": "StrategyManagerSet(address indexed strategyManager)",
        "column_mapping": ColumnMapping(
            transaction=COMMON_TRANSACTION_MAPPING, block=COMMON_BLOCK_MAPPING
        ),
    },
    "DelegationManagerSet": {
        "signature": "DelegationManagerSet(address indexed delegationManager)",
        "column_mapping": ColumnMapping(
            transaction=COMMON_TRANSACTION_MAPPING, block=COMMON_BLOCK_MAPPING
        ),
    },
    "EigenPodManagerSet": {
        "signature": "EigenPodManagerSet(address indexed eigenPodManager)",
        "column_mapping": ColumnMapping(
            transaction=COMMON_TRANSACTION_MAPPING, block=COMMON_BLOCK_MAPPING
        ),
    },
    "RestakeableStrategiesSet": {
        "signature": "RestakeableStrategiesSet(address[] indexed restakeableStrategies)",
        "column_mapping": ColumnMapping(
            transaction=COMMON_TRANSACTION_MAPPING, block=COMMON_BLOCK_MAPPING
        ),
    },
    "FreezeOracleSet": {
        "signature": "FreezeOracleSet(address indexed freezeOracle)",
        "column_mapping": ColumnMapping(
            transaction=COMMON_TRANSACTION_MAPPING, block=COMMON_BLOCK_MAPPING
        ),
    },
    "UnfreezeFeeSet": {
        "signature": "UnfreezeFeeSet(uint256 unfreezeFee)",
        "column_mapping": ColumnMapping(
            decoded_log={"unfreezeFee": DataType.UINT64},
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    },
    "UnfreezeReceiverSet": {
        "signature": "UnfreezeReceiverSet(address indexed unfreezeReceiver)",
        "column_mapping": ColumnMapping(
            transaction=COMMON_TRANSACTION_MAPPING, block=COMMON_BLOCK_MAPPING
        ),
    },
    "UnfreezePeriodBlocksSet": {
        "signature": "UnfreezePeriodBlocksSet(uint256 unfreezePeriodBlocks)",
        "column_mapping": ColumnMapping(
            decoded_log={"unfreezePeriodBlocks": DataType.UINT64},
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    },
    "OperatorDeregPeriodBlocksSet": {
        "signature": "OperatorDeregPeriodBlocksSet(uint256 operatorDeregPeriodBlocks)",
        "column_mapping": ColumnMapping(
            decoded_log={"operatorDeregPeriodBlocks": DataType.UINT64},
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    },
    "ValidatorDeregPeriodBlocksSet": {
        "signature": "ValidatorDeregPeriodBlocksSet(uint256 validatorDeregPeriodBlocks)",
        "column_mapping": ColumnMapping(
            decoded_log={"validatorDeregPeriodBlocks": DataType.UINT64},
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    },
    "LSTRestakerDeregPeriodBlocksSet": {
        "signature": "LSTRestakerDeregPeriodBlocksSet(uint256 lstRestakerDeregPeriodBlocks)",
        "column_mapping": ColumnMapping(
            decoded_log={"lstRestakerDeregPeriodBlocks": DataType.UINT64},
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    },
}
