"""Constants for QFC SDK."""

from qfc_sdk.types import NetworkConfig

# Network configurations
NETWORKS: dict[str, NetworkConfig] = {
    "localhost": NetworkConfig(
        name="Localhost",
        chain_id=9000,
        rpc_url="http://127.0.0.1:8545",
        ws_url="ws://127.0.0.1:8546",
    ),
    "testnet": NetworkConfig(
        name="QFC Testnet",
        chain_id=9000,
        rpc_url="https://rpc.testnet.qfc.network",
        ws_url="wss://ws.testnet.qfc.network",
        explorer_url="https://explorer.testnet.qfc.network",
        faucet_url="https://faucet.testnet.qfc.network",
    ),
    "mainnet": NetworkConfig(
        name="QFC Mainnet",
        chain_id=9001,
        rpc_url="https://rpc.qfc.network",
        ws_url="wss://ws.qfc.network",
        explorer_url="https://explorer.qfc.network",
    ),
}

# Contract addresses
CONTRACTS = {
    "STAKING_TESTNET": "0x0000000000000000000000000000000000001000",
    "STAKING_MAINNET": "0x0000000000000000000000000000000000001000",
    "MULTICALL3": "0xcA11bde05977b3631167028862bE2a173976CA11",
}

# Staking constants
MIN_STAKE = 10_000 * 10**18  # 10,000 QFC in wei
MIN_DELEGATION = 100 * 10**18  # 100 QFC in wei
UNSTAKE_DELAY = 7 * 24 * 60 * 60  # 7 days in seconds
MAX_COMMISSION_RATE = 5000  # 50% in basis points

# Gas limits
GAS_LIMITS = {
    "TRANSFER": 21000,
    "ERC20_TRANSFER": 65000,
    "ERC20_APPROVE": 50000,
    "STAKE": 100000,
    "UNSTAKE": 100000,
    "DELEGATE": 120000,
    "UNDELEGATE": 120000,
    "CLAIM_REWARDS": 80000,
    "CONTRACT_DEPLOY": 3000000,
}

# ABIs
STAKING_ABI = [
    "function stake() payable",
    "function unstake(uint256 amount)",
    "function delegate(address validator, uint256 amount)",
    "function undelegate(address validator, uint256 amount)",
    "function claimRewards()",
    "function getStakeInfo(address account) view returns (uint256 staked, uint256 delegated, uint256 pending, uint256 unstaking)",
    "function getDelegation(address delegator, address validator) view returns (uint256 amount, uint256 rewards)",
    "function getValidator(address validator) view returns (address, uint256, uint256, uint256, uint256, bool)",
    "function getValidators() view returns (address[])",
    "function registerValidator(uint256 commission)",
    "function updateCommission(uint256 commission)",
]

ERC20_ABI = [
    "function name() view returns (string)",
    "function symbol() view returns (string)",
    "function decimals() view returns (uint8)",
    "function totalSupply() view returns (uint256)",
    "function balanceOf(address account) view returns (uint256)",
    "function transfer(address to, uint256 amount) returns (bool)",
    "function allowance(address owner, address spender) view returns (uint256)",
    "function approve(address spender, uint256 amount) returns (bool)",
    "function transferFrom(address from, address to, uint256 amount) returns (bool)",
    "event Transfer(address indexed from, address indexed to, uint256 value)",
    "event Approval(address indexed owner, address indexed spender, uint256 value)",
]

ERC721_ABI = [
    "function name() view returns (string)",
    "function symbol() view returns (string)",
    "function tokenURI(uint256 tokenId) view returns (string)",
    "function balanceOf(address owner) view returns (uint256)",
    "function ownerOf(uint256 tokenId) view returns (address)",
    "function approve(address to, uint256 tokenId)",
    "function getApproved(uint256 tokenId) view returns (address)",
    "function setApprovalForAll(address operator, bool approved)",
    "function isApprovedForAll(address owner, address operator) view returns (bool)",
    "function transferFrom(address from, address to, uint256 tokenId)",
    "function safeTransferFrom(address from, address to, uint256 tokenId)",
    "function safeTransferFrom(address from, address to, uint256 tokenId, bytes data)",
    "event Transfer(address indexed from, address indexed to, uint256 indexed tokenId)",
    "event Approval(address indexed owner, address indexed approved, uint256 indexed tokenId)",
]

ERC1155_ABI = [
    "function uri(uint256 id) view returns (string)",
    "function balanceOf(address account, uint256 id) view returns (uint256)",
    "function balanceOfBatch(address[] accounts, uint256[] ids) view returns (uint256[])",
    "function setApprovalForAll(address operator, bool approved)",
    "function isApprovedForAll(address account, address operator) view returns (bool)",
    "function safeTransferFrom(address from, address to, uint256 id, uint256 amount, bytes data)",
    "function safeBatchTransferFrom(address from, address to, uint256[] ids, uint256[] amounts, bytes data)",
    "event TransferSingle(address indexed operator, address indexed from, address indexed to, uint256 id, uint256 value)",
    "event TransferBatch(address indexed operator, address indexed from, address indexed to, uint256[] ids, uint256[] values)",
]

MULTICALL3_ABI = [
    "function aggregate(tuple(address target, bytes callData)[] calls) payable returns (uint256 blockNumber, bytes[] returnData)",
    "function aggregate3(tuple(address target, bool allowFailure, bytes callData)[] calls) payable returns (tuple(bool success, bytes returnData)[] returnData)",
    "function getEthBalance(address addr) view returns (uint256 balance)",
    "function getBlockNumber() view returns (uint256 blockNumber)",
    "function getCurrentBlockTimestamp() view returns (uint256 timestamp)",
]

__all__ = [
    "NETWORKS",
    "CONTRACTS",
    "MIN_STAKE",
    "MIN_DELEGATION",
    "UNSTAKE_DELAY",
    "MAX_COMMISSION_RATE",
    "GAS_LIMITS",
    "STAKING_ABI",
    "ERC20_ABI",
    "ERC721_ABI",
    "ERC1155_ABI",
    "MULTICALL3_ABI",
]
