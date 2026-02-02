# QFC SDK for Python

Python SDK for interacting with the QFC blockchain.

## Installation

```bash
pip install qfc-sdk
```

Or with pip from source:

```bash
pip install -e .
```

## Quick Start

```python
from qfc_sdk import QfcProvider, QfcWallet, parse_qfc, format_qfc

# Connect to testnet
provider = QfcProvider(network="testnet")

# Get balance
balance = provider.get_balance("0x742d35Cc6634C0532925a3b844Bc9e7595f12345")
print(f"Balance: {format_qfc(balance)} QFC")

# Create wallet from private key
wallet = QfcWallet.from_private_key("0x...", provider)
print(f"Address: {wallet.address}")

# Send transaction
tx = wallet.send_transaction({
    "to": "0xRecipient...",
    "value": parse_qfc("10"),
})
receipt = tx.wait()
print(f"TX Hash: {receipt.transaction_hash}")
```

## Features

### Provider

```python
from qfc_sdk import QfcProvider, NETWORKS

# Using network name
provider = QfcProvider(network="testnet")

# Using custom RPC URL
provider = QfcProvider("http://localhost:8545")

# Standard methods
balance = provider.get_balance("0x...")
block = provider.get_block("latest")
tx = provider.get_transaction("0x...")
receipt = provider.get_transaction_receipt("0x...")

# QFC-specific methods
validators = provider.get_validators()
validator = provider.get_validator("0x...")
score = provider.get_contribution_score("0x...")
epoch = provider.get_epoch()
stats = provider.get_network_stats()
```

### Wallet

```python
from qfc_sdk import QfcWallet

# From private key
wallet = QfcWallet.from_private_key("0x...", provider)

# From mnemonic
wallet = QfcWallet.from_mnemonic("word1 word2 ... word12", provider)

# Create random wallet
wallet, mnemonic = QfcWallet.create_random(provider)
print(f"Save this mnemonic: {mnemonic}")

# Send transaction
tx = wallet.send_transaction({
    "to": "0x...",
    "value": parse_qfc("1.5"),
})
receipt = tx.wait()

# Staking
wallet.stake(parse_qfc("1000"))
wallet.delegate("0xValidator...", parse_qfc("500"))
wallet.claim_rewards()
wallet.unstake(parse_qfc("100"))
```

### Staking Client

```python
from qfc_sdk import StakingClient

staking = StakingClient(provider)

# Get staking info
info = staking.get_stake_info("0x...")
print(f"Staked: {format_qfc(info.staked_amount)}")
print(f"Pending rewards: {format_qfc(info.pending_rewards)}")

# Get delegations
delegations = staking.get_delegations("0x...")
for d in delegations:
    print(f"Validator: {d.validator}, Amount: {format_qfc(d.amount)}")

# Get validators
validators = staking.get_validators_list(status="active", page=1, per_page=10)
```

### Token Contracts

```python
from qfc_sdk import get_erc20, get_erc721, get_erc1155

# ERC-20
token = get_erc20("0xTokenAddress...", provider)
print(f"Name: {token.name}")
print(f"Symbol: {token.symbol}")
balance = token.balance_of("0x...")

# With wallet for transfers
token = get_erc20("0xTokenAddress...", wallet)
tx = token.transfer("0xRecipient...", 1000)
tx.wait()

# ERC-721
nft = get_erc721("0xNFTAddress...", provider)
owner = nft.owner_of(1)
uri = nft.token_uri(1)

# ERC-1155
multi = get_erc1155("0xAddress...", provider)
balance = multi.balance_of("0x...", token_id=1)
```

### Multicall

```python
from qfc_sdk import get_multicall3
from qfc_sdk.contracts.multicall import Call

multicall = get_multicall3(provider)

# Get multiple balances in one call
balances = multicall.get_balances([
    "0xAddress1...",
    "0xAddress2...",
    "0xAddress3...",
])
```

### Utilities

```python
from qfc_sdk import (
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

# Unit conversion
wei = parse_qfc("1.5")          # 1500000000000000000
qfc = format_qfc(wei)            # "1.5000"
gas_wei = parse_gwei("10")       # 10000000000

# Validation
is_valid_address("0x...")        # True/False
is_valid_private_key("0x...")    # True/False
is_valid_tx_hash("0x...")        # True/False

# Formatting
shorten_address("0x742d35Cc6634C0532925a3b844Bc9e7595f12345")
# "0x742d...2345"
```

### Constants

```python
from qfc_sdk import NETWORKS, CONTRACTS, MIN_STAKE, MIN_DELEGATION

print(NETWORKS["testnet"].rpc_url)
print(NETWORKS["testnet"].chain_id)
print(f"Min stake: {format_qfc(MIN_STAKE)} QFC")
```

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=qfc_sdk

# Type checking
mypy src/qfc_sdk

# Linting
ruff check src/qfc_sdk

# Formatting
black src/qfc_sdk
```

## Requirements

- Python 3.10+
- web3.py 6.0+
- pydantic 2.0+

## License

MIT
