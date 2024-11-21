from hypermanager.events import EventConfig
from hypersync import ColumnMapping, DataType
from hypermanager.schema import COMMON_TRANSACTION_MAPPING, COMMON_BLOCK_MAPPING


mev_commit_config = {
    # mev_commit logs config as of v0.6.0
    "NewL1Block": EventConfig(
        name="NewL1Block",
        signature="NewL1Block(uint256 indexed blockNumber,address indexed winner,uint256 indexed window)",
        column_mapping=ColumnMapping(
            decoded_log={
                "blockNumber": DataType.INT64,
                "window": DataType.INT64,
            },
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    ),
    "CommitmentProcessed": EventConfig(
        name="CommitmentProcessed",
        signature="CommitmentProcessed(bytes32 indexed commitmentIndex, bool isSlash)",
        column_mapping=ColumnMapping(
            transaction=COMMON_TRANSACTION_MAPPING, block=COMMON_BLOCK_MAPPING
        ),
    ),
    "BidderRegistered": EventConfig(
        name="BidderRegistered",
        signature="BidderRegistered(address indexed bidder, uint256 indexed depositedAmount, uint256 indexed windowNumber)",
        column_mapping=ColumnMapping(
            decoded_log={
                "depositedAmount": DataType.FLOAT64,
                "windowNumber": DataType.FLOAT64,
            },
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    ),
    "BidderWithdrawal": EventConfig(
        name="BidderWithdrawal",
        signature="BidderWithdrawal(address indexed bidder, uint256 indexed window, uint256 indexed amount)",
        column_mapping=ColumnMapping(
            decoded_log={
                "amount": DataType.INT64,
                "window": DataType.INT64,
            },
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    ),
    "OpenedCommitmentStored": EventConfig(
        name="OpenedCommitmentStored",
        signature=(
            "OpenedCommitmentStored(bytes32 indexed commitmentIndex, address bidder, address commiter, "
            "uint256 bid, uint64 blockNumber, bytes32 bidHash, uint64 decayStartTimeStamp, "
            "uint64 decayEndTimeStamp, string txnHash, string revertingTxHashes, bytes32 commitmentHash, "
            "bytes bidSignature, bytes commitmentSignature, uint64 dispatchTimestamp, bytes sharedSecretKey)"
        ),
        # v0.6.0? Wasn't able to confirm
        contract='0xCAC68D97a56b19204Dd3dbDC103CB24D47A825A3',
        column_mapping=ColumnMapping(
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
    ),
    "FundsRetrieved": EventConfig(
        name="FundsRetrieved",
        signature="FundsRetrieved(bytes32 indexed commitmentDigest,address indexed bidder,uint256 indexed window,uint256 amount)",
        column_mapping=ColumnMapping(
            decoded_log={
                "window": DataType.UINT64,
                "amount": DataType.UINT64,
            },
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    ),
    "FundsRewarded": EventConfig(
        name="FundsRewarded",
        signature="FundsRewarded(bytes32 indexed commitmentDigest, address indexed bidder, address indexed provider, uint256 window, uint256 amount)",
        column_mapping=ColumnMapping(
            decoded_log={
                "window": DataType.UINT64,
                "amount": DataType.UINT64,
            },
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    ),
    "FundsSlashed": EventConfig(
        name="FundsSlashed",
        signature="FundsSlashed(address indexed provider, uint256 amount)",
        column_mapping=ColumnMapping(
            decoded_log={"amount": DataType.UINT64},
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    ),
    "FundsDeposited": EventConfig(
        name="FundsDeposited",
        signature="FundsDeposited(address indexed provider, uint256 amount)",
        column_mapping=ColumnMapping(
            decoded_log={"amount": DataType.UINT64},
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    ),
    "Withdraw": EventConfig(
        name="Withdraw",
        signature="Withdraw(address indexed provider, uint256 amount)",
        column_mapping=ColumnMapping(
            decoded_log={"amount": DataType.UINT64},
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    ),
    "ProviderRegistered": EventConfig(
        name="ProviderRegistered",
        signature="ProviderRegistered(address indexed provider, uint256 stakedAmount, bytes blsPublicKey)",
        column_mapping=ColumnMapping(
            decoded_log={"stakedAmount": DataType.UINT64},
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    ),
    "UnopenedCommitmentStored": EventConfig(
        name="UnopenedCommitmentStored",
        signature="UnopenedCommitmentStored(bytes32 indexed commitmentIndex,address committer,bytes32 commitmentDigest,bytes commitmentSignature,uint64 dispatchTimestamp)",
        column_mapping=ColumnMapping(
            decoded_log={"dispatchTimestamp": DataType.UINT64},
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    ),
    # Events added from v0.7.0
    "OpenedCommitmentStoredv2": EventConfig(
        name="OpenedCommitmentStoredv2",
        signature=(
            "OpenedCommitmentStored(bytes32 indexed commitmentIndex, address bidder, address committer, "
            "uint256 bidAmt, uint64 blockNumber, bytes32 bidHash, uint64 decayStartTimeStamp, "
            "uint64 decayEndTimeStamp, string txnHash, string revertingTxHashes, bytes32 commitmentHash, "
            "bytes bidSignature, bytes commitmentSignature, uint64 dispatchTimestamp, bytes sharedSecretKey)"
        ),
        # Specify the contract address because v0.6 and v0.7 have same signatures but different contract addresses.
        contract='0x9433bCD9e89F923ce587f7FA7E39e120E93eb84D',
        column_mapping=ColumnMapping(
            decoded_log={
                "bidAmt": DataType.UINT64,
                "blockNumber": DataType.UINT64,
                "decayStartTimeStamp": DataType.UINT64,
                "decayEndTimeStamp": DataType.UINT64,
                "dispatchTimestamp": DataType.UINT64,
            },
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    ),

    # OracleContractUpdated with indexed newOracleContract
    "OracleContractUpdatedv2": EventConfig(
        name="OracleContractUpdatedv2",
        signature="OracleContractUpdated(address indexed newOracleContract)",
        column_mapping=ColumnMapping(
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    ),

    # New event from iBidderRegistry.sol and iProviderRegistry.sol
    "TransferToBidderFailed": EventConfig(
        name="TransferToBidderFailed",
        signature="TransferToBidderFailed(address indexed bidder, uint256 amount)",
        column_mapping=ColumnMapping(
            decoded_log={
                "amount": DataType.UINT64,
            },
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    ),

    # New event from iProviderRegistry.sol
    "BidderWithdrawSlashedAmount": EventConfig(
        name="BidderWithdrawSlashedAmount",
        signature="BidderWithdrawSlashedAmount(address indexed bidder, uint256 amount)",
        column_mapping=ColumnMapping(
            decoded_log={
                "amount": DataType.UINT64,
            },
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    ),

    # New event from blockTracker.sol
    "BuilderAddressAdded": EventConfig(
        name="BuilderAddressAdded",
        signature="BuilderAddressAdded(string indexed builderName, address indexed builderAddress)",
        column_mapping=ColumnMapping(
            # No non-indexed fields
            decoded_log={},
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    )
}

# validator config for mev_commit v0.6.0
mev_commit_validator_config = {
    "Staked_old": EventConfig(
        name="Staked_old",
        signature="Staked(address indexed txOriginator, bytes valBLSPubKey, uint256 amount)",
        column_mapping=ColumnMapping(
            decoded_log={"amount": DataType.UINT64},
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    ),
    "Staked": EventConfig(
        name="Staked",
        signature="Staked(address indexed msgSender, address indexed withdrawalAddress, bytes valBLSPubKey, uint256 amount)",
        # version v.7.0 https://holesky.etherscan.io/address/0x87d5f694fad0b6c8aabca96277de09451e277bcf
        # contract="0x87D5F694fAD0b6C8aaBCa96277DE09451E277Bcf",
        column_mapping=ColumnMapping(
            decoded_log={"amount": DataType.FLOAT64},
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    ),
    "StakeAdded": EventConfig(
        name="StakeAdded",
        signature="StakeAdded(address indexed msgSender, address indexed withdrawalAddress, bytes valBLSPubKey, uint256 amount, uint256 newBalance)",
        column_mapping=ColumnMapping(
            decoded_log={
                "amount": DataType.UINT64,
                "newBalance": DataType.UINT64,
            },
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    ),
    "Unstaked": EventConfig(
        name="Unstaked",
        signature="Unstaked(address indexed msgSender, address indexed withdrawalAddress, bytes valBLSPubKey, uint256 amount)",
        column_mapping=ColumnMapping(
            decoded_log={"amount": DataType.UINT64},
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    ),
    "StakeWithdrawn": EventConfig(
        name="StakeWithdrawn",
        signature="StakeWithdrawn(address indexed msgSender, address indexed withdrawalAddress, bytes valBLSPubKey, uint256 amount)",
        column_mapping=ColumnMapping(
            decoded_log={"amount": DataType.UINT64},
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    ),
    "Slashed": EventConfig(
        name="Slashed",
        signature="Slashed(address indexed msgSender, address indexed slashReceiver, address indexed withdrawalAddress, bytes valBLSPubKey, uint256 amount)",
        column_mapping=ColumnMapping(
            decoded_log={"amount": DataType.UINT64},
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    ),
    "MinStakeSet": EventConfig(
        name="MinStakeSet",
        signature="MinStakeSet(address indexed msgSender, uint256 newMinStake)",
        column_mapping=ColumnMapping(
            decoded_log={"newMinStake": DataType.UINT64},
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    ),
    "SlashAmountSet": EventConfig(
        name="SlashAmountSet",
        signature="SlashAmountSet(address indexed msgSender, uint256 newSlashAmount)",
        column_mapping=ColumnMapping(
            decoded_log={"newSlashAmount": DataType.UINT64},
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    ),
    "SlashOracleSet": EventConfig(
        name="SlashOracleSet",
        signature="SlashOracleSet(address indexed msgSender, address newSlashOracle)",
        column_mapping=ColumnMapping(
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    ),
    "SlashReceiverSet": EventConfig(
        name="SlashReceiverSet",
        signature="SlashReceiverSet(address indexed msgSender, address newSlashReceiver)",
        column_mapping=ColumnMapping(
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    ),
    "UnstakePeriodBlocksSet": EventConfig(
        name="UnstakePeriodBlocksSet",
        signature="UnstakePeriodBlocksSet(address indexed msgSender, uint256 newUnstakePeriodBlocks)",
        column_mapping=ColumnMapping(
            decoded_log={"newUnstakePeriodBlocks": DataType.UINT64},
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    ),
    "VanillaRegistrySet": EventConfig(
        name="VanillaRegistrySet",
        signature="VanillaRegistrySet(address oldContract, address newContract)",
        column_mapping=ColumnMapping(
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    ),
    "MevCommitAVSSet": EventConfig(
        name="MevCommitAVSSet",
        signature="VanillaRegistrySet(address oldContract, address newContract)",
        column_mapping=ColumnMapping(
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    ),
    "OperatorRegistered": EventConfig(
        name="OperatorRegistered",
        signature="OperatorRegistered(address indexed operator)",
        column_mapping=ColumnMapping(
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    ),
    "OperatorDeregistrationRequested": EventConfig(
        name="OperatorDeregistrationRequested",
        signature="OperatorDeregistrationRequested(address indexed operator)",
        column_mapping=ColumnMapping(
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    ),
    "OperatorDeregistered": EventConfig(
        name="OperatorDeregistered",
        signature="OperatorDeregistered(address indexed operator)",
        column_mapping=ColumnMapping(
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    ),
    "ValidatorRegistered": EventConfig(
        name="ValidatorRegistered",
        signature="ValidatorRegistered(bytes validatorPubKey, address indexed podOwner)",
        column_mapping=ColumnMapping(
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    ),
    "ValidatorDeregistrationRequested": EventConfig(
        name="ValidatorDeregistrationRequested",
        signature="ValidatorDeregistrationRequested(bytes validatorPubKey, address indexed podOwner)",
        column_mapping=ColumnMapping(
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    ),
    "ValidatorDeregistered": EventConfig(
        name="ValidatorDeregistered",
        signature="ValidatorDeregistered(bytes validatorPubKey, address indexed podOwner)",
        column_mapping=ColumnMapping(
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    ),
    "LSTRestakerRegistered": EventConfig(
        name="LSTRestakerRegistered",
        signature="LSTRestakerRegistered(bytes chosenValidator, uint256 numChosen, address indexed lstRestaker)",
        column_mapping=ColumnMapping(
            decoded_log={"numChosen": DataType.UINT64},
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    ),
    "LSTRestakerDeregistrationRequested": EventConfig(
        name="LSTRestakerDeregistrationRequested",
        signature="LSTRestakerDeregistrationRequested(bytes chosenValidator, uint256 numChosen, address indexed lstRestaker)",
        column_mapping=ColumnMapping(
            decoded_log={"numChosen": DataType.UINT64},
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    ),
    "LSTRestakerDeregistered": EventConfig(
        name="LSTRestakerDeregistered",
        signature="LSTRestakerDeregistered(bytes chosenValidator, uint256 numChosen, address indexed lstRestaker)",
        column_mapping=ColumnMapping(
            decoded_log={"numChosen": DataType.UINT64},
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    ),
    "ValidatorFrozen": EventConfig(
        name="ValidatorFrozen",
        signature="ValidatorFrozen(bytes validatorPubKey, address indexed podOwner)",
        column_mapping=ColumnMapping(
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    ),
    "ValidatorUnfrozen": EventConfig(
        name="ValidatorUnfrozen",
        signature="ValidatorUnfrozen(bytes validatorPubKey, address indexed podOwner)",
        column_mapping=ColumnMapping(
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    ),
    "AVSDirectorySet": EventConfig(
        name="AVSDirectorySet",
        signature="AVSDirectorySet(address indexed avsDirectory)",
        column_mapping=ColumnMapping(
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    ),
    "StrategyManagerSet": EventConfig(
        name="StrategyManagerSet",
        signature="StrategyManagerSet(address indexed strategyManager)",
        column_mapping=ColumnMapping(
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    ),
    "DelegationManagerSet": EventConfig(
        name="DelegationManagerSet",
        signature="DelegationManagerSet(address indexed delegationManager)",
        column_mapping=ColumnMapping(
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    ),
    "EigenPodManagerSet": EventConfig(
        name="EigenPodManagerSet",
        signature="EigenPodManagerSet(address indexed eigenPodManager)",
        column_mapping=ColumnMapping(
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    ),
    "RestakeableStrategiesSet": EventConfig(
        name="RestakeableStrategiesSet",
        signature="RestakeableStrategiesSet(address[] indexed restakeableStrategies)",
        column_mapping=ColumnMapping(
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    ),
    "FreezeOracleSet": EventConfig(
        name="FreezeOracleSet",
        signature="FreezeOracleSet(address indexed freezeOracle)",
        column_mapping=ColumnMapping(
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    ),
    "UnfreezeFeeSet": EventConfig(
        name="UnfreezeFeeSet",
        signature="UnfreezeFeeSet(uint256 unfreezeFee)",
        column_mapping=ColumnMapping(
            decoded_log={"unfreezeFee": DataType.UINT64},
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    ),
    "UnfreezeReceiverSet": EventConfig(
        name="UnfreezeReceiverSet",
        signature="UnfreezeReceiverSet(address indexed unfreezeReceiver)",
        column_mapping=ColumnMapping(
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    ),
    "UnfreezePeriodBlocksSet": EventConfig(
        name="UnfreezePeriodBlocksSet",
        signature="UnfreezePeriodBlocksSet(uint256 unfreezePeriodBlocks)",
        column_mapping=ColumnMapping(
            decoded_log={"unfreezePeriodBlocks": DataType.UINT64},
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    ),
    "OperatorDeregPeriodBlocksSet": EventConfig(
        name="OperatorDeregPeriodBlocksSet",
        signature="OperatorDeregPeriodBlocksSet(uint256 operatorDeregPeriodBlocks)",
        column_mapping=ColumnMapping(
            decoded_log={"operatorDeregPeriodBlocks": DataType.UINT64},
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    ),
    "ValidatorDeregPeriodBlocksSet": EventConfig(
        name="ValidatorDeregPeriodBlocksSet",
        signature="ValidatorDeregPeriodBlocksSet(uint256 validatorDeregPeriodBlocks)",
        column_mapping=ColumnMapping(
            decoded_log={"validatorDeregPeriodBlocks": DataType.UINT64},
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    ),
    "LSTRestakerDeregPeriodBlocksSet": EventConfig(
        name="LSTRestakerDeregPeriodBlocksSet",
        signature="LSTRestakerDeregPeriodBlocksSet(uint256 lstRestakerDeregPeriodBlocks)",
        column_mapping=ColumnMapping(
            decoded_log={"lstRestakerDeregPeriodBlocks": DataType.UINT64},
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    ),
}
