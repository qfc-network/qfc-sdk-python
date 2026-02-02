"""QFC SDK - Python SDK for QFC Blockchain."""

from qfc_sdk.provider import QfcProvider
from qfc_sdk.wallet import QfcWallet
from qfc_sdk.staking import StakingClient
from qfc_sdk.contracts import get_erc20, get_erc721, get_erc1155, get_multicall3
from qfc_sdk.utils import (
    parse_qfc,
    format_qfc,
    parse_gwei,
    format_gwei,
    is_valid_address,
    is_valid_private_key,
    is_valid_tx_hash,
    shorten_address,
    shorten_hash,
)
from qfc_sdk.types import (
    Network,
    NetworkConfig,
    Block,
    Transaction,
    TransactionReceipt,
    Validator,
    StakeInfo,
    Delegation,
)
from qfc_sdk.constants import NETWORKS, CONTRACTS, MIN_STAKE, MIN_DELEGATION, UNSTAKE_DELAY

__version__ = "0.1.0"

__all__ = [
    # Provider
    "QfcProvider",
    # Wallet
    "QfcWallet",
    # Staking
    "StakingClient",
    # Contracts
    "get_erc20",
    "get_erc721",
    "get_erc1155",
    "get_multicall3",
    # Utils
    "parse_qfc",
    "format_qfc",
    "parse_gwei",
    "format_gwei",
    "is_valid_address",
    "is_valid_private_key",
    "is_valid_tx_hash",
    "shorten_address",
    "shorten_hash",
    # Types
    "Network",
    "NetworkConfig",
    "Block",
    "Transaction",
    "TransactionReceipt",
    "Validator",
    "StakeInfo",
    "Delegation",
    # Constants
    "NETWORKS",
    "CONTRACTS",
    "MIN_STAKE",
    "MIN_DELEGATION",
    "UNSTAKE_DELAY",
]
