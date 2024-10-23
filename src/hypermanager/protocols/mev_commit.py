from hypermanager.events import EventConfig
from hypersync import ColumnMapping, DataType
from hypermanager.schema import COMMON_TRANSACTION_MAPPING, COMMON_BLOCK_MAPPING


# Base event configurations as a dictionary with event names as keys
mev_commit_config = {
    "NewL1Block": EventConfig(
        name="NewL1Block",
        signature="NewL1Block(uint256 indexed blockNumber,address indexed winner,uint256 indexed window)",
        column_mapping=ColumnMapping(
            transaction=COMMON_TRANSACTION_MAPPING, block=COMMON_BLOCK_MAPPING
        ),
        decoded_log={
            "blockNumber": DataType.INT64,
            "window": DataType.INT64,
        },
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
        signature="BidderRegistered(address indexed bidder, uint256 depositedAmount, uint256 windowNumber)",
        column_mapping=ColumnMapping(
            decoded_log={
                "depositedAmount": DataType.INT64,
                "windowNumber": DataType.INT64,
            },
            transaction=COMMON_TRANSACTION_MAPPING,
            block=COMMON_BLOCK_MAPPING,
        ),
    ),
    "BidderWithdrawal": EventConfig(
        name="BidderWithdrawal",
        signature="BidderWithdrawal(address indexed bidder, uint256 window, uint256 amount)",
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
        signature="FundsRetrieved(bytes32 indexed commitmentDigest,address indexed bidder,uint256 window,uint256 amount)",
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
        column_mapping=ColumnMapping(
            decoded_log={"amount": DataType.UINT64},
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
}
