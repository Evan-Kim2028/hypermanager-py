from enum import Enum


class HyperSyncClients(Enum):
    ARBITRUM = ("https://arbitrum.hypersync.xyz", 42161, "gold")
    ARBITRUM_NOVA = ("https://arbitrum-nova.hypersync.xyz", 42170, "gold")
    ARBITRUM_SEPOLIA = ("https://arbitrum-sepolia.hypersync.xyz", 421614, "gold")
    AURORA = ("https://aurora.hypersync.xyz", 1313161554, "bronze")
    AVALANCHE = ("https://avalanche.hypersync.xyz", 43114, "gold")
    BASE = ("https://base.hypersync.xyz", 8453, "gold")
    BASE_SEPOLIA = ("https://base-sepolia.hypersync.xyz", 84532, "gold")
    BERACHAIN_BARTIO = ("https://berachain-bartio.hypersync.xyz", 80084, "bronze")
    BLAST = ("https://blast.hypersync.xyz", 81457, "gold")
    BLAST_SEPOLIA = ("https://blast-sepolia.hypersync.xyz", 168587773, "gold")
    BOBA = ("https://boba.hypersync.xyz", 288, "bronze")
    BSC = ("https://bsc.hypersync.xyz", 56, "gold")
    BSC_TESTNET = ("https://bsc-testnet.hypersync.xyz", 97, "gold")
    C1_MILKOMEDA = ("https://c1-milkomeda.hypersync.xyz", 2001, "bronze")
    CELO = ("https://celo.hypersync.xyz", 42220, "bronze")
    CHILIZ = ("https://chiliz.hypersync.xyz", 8888, "bronze")
    CITREA_DEVNET = ("https://citrea-devnet.hypersync.xyz", 62298, "bronze")
    CRAB = ("https://crab.hypersync.xyz", 44, "bronze")
    CYBER = ("https://cyber.hypersync.xyz", 7560, "bronze")
    DARWINIA = ("https://darwinia.hypersync.xyz", 46, "bronze")
    ETHEREUM_MAINNET = ("https://eth.hypersync.xyz", 1, "gold")
    FANTOM = ("https://fantom.hypersync.xyz", 250, "bronze")
    FHENIX_TESTNET = ("https://fhenix-testnet.hypersync.xyz", 42069, "bronze")
    FLARE = ("https://flare.hypersync.xyz", 14, "bronze")
    FUJI = ("https://fuji.hypersync.xyz", 43113, "gold")
    GALADRIAL_DEVNET = ("https://galadrial-devnet.hypersync.xyz", 696969, "bronze")
    GNOSIS = ("https://gnosis.hypersync.xyz", 100, "bronze")
    GNOSIS_CHIADO = ("https://gnosis-chiado.hypersync.xyz", 10200, "bronze")
    GOERLI = ("https://goerli.hypersync.xyz", 5, "bronze")
    HARMONY_SHARD_0 = ("https://harmony-shard-0.hypersync.xyz", 1666600000, "bronze")
    HOLESKY = ("https://holesky.hypersync.xyz", 17000, "gold")
    INCO_GENTRY_TESTNET = ("https://inco-gentry-testnet.hypersync.xyz", 9090, "bronze")
    KAKAROT_SEPOLIA = ("https://kakarot-sepolia.hypersync.xyz", 1802203764, "bronze")
    KROMA = ("https://kroma.hypersync.xyz", 255, "bronze")
    LINEA = ("https://linea.hypersync.xyz", 59144, "gold")
    LUKSO = ("https://lukso.hypersync.xyz", 42, "bronze")
    MANTA = ("https://manta.hypersync.xyz", 169, "bronze")
    MANTLE = ("https://mantle.hypersync.xyz", 5000, "gold")
    METIS = ("https://metis.hypersync.xyz", 1088, "bronze")
    MEV_COMMIT = ("https://mev-commit.hypersync.xyz", 17864, "bronze")
    MODE = ("https://mode.hypersync.xyz", 1, "bronze")
    MOONBEAM = ("https://moonbeam.hypersync.xyz", 1284, "gold")
    MORPH_TESTNET = ("https://morph-testnet.hypersync.xyz", 2810, "bronze")
    NEON_EVM = ("https://neon-evm.hypersync.xyz", 245022934, "bronze")
    OPTIMISM = ("https://optimism.hypersync.xyz", 10, "gold")
    OPTIMISM_SEPOLIA = ("https://optimism-sepolia.hypersync.xyz", 11155420, "gold")
    POLYGON = ("https://polygon.hypersync.xyz", 137, "gold")
    POLYGON_AMOY = ("https://polygon-amoy.hypersync.xyz", 80002, "bronze")
    POLYGON_ZKEVM = ("https://polygon-zkevm.hypersync.xyz", 1101, "gold")
    RSK = ("https://rsk.hypersync.xyz", 30, "bronze")
    SAAKURU = ("https://saakuru.hypersync.xyz", 7225878, "bronze")
    SCROLL = ("https://scroll.hypersync.xyz", 534352, "gold")
    SEPOLIA = ("https://sepolia.hypersync.xyz", 11155111, "gold")
    SHIMMER_EVM = ("https://shimmer-evm.hypersync.xyz", 148, "bronze")
    SOPHON_TESTNET = ("https://sophon-testnet.hypersync.xyz", 531050104, "bronze")
    TAIKO_JOLNR = ("https://taiko-jolnr.hypersync.xyz", 1088, "bronze")
    X_LAYER = ("https://x-layer.hypersync.xyz", 196, "bronze")
    X_LAYER_TESTNET = ("https://x-layer-testnet.hypersync.xyz", 195, "bronze")
    ZETA = ("https://zeta.hypersync.xyz", 7000, "bronze")
    ZIRCUIT = ("https://zircuit.hypersync.xyz", 48900, "bronze")
    ZKSYNC = ("https://zksync.hypersync.xyz", 324, "gold")
    ZORA = ("https://zora.hypersync.xyz", 7777777, "bronze")

    def __init__(self, url, network_id, tier):
        self._url = url
        self._network_id = network_id
        self._tier = tier

    @property
    def client(self):
        return self._url

    @property
    def network_id(self):
        return self._network_id

    @property
    def tier(self):
        return self._tier
