# QFC SDK Python

Python SDK for interacting with the QFC blockchain.

## Project Structure

```
qfc-sdk-python/
├── src/qfc_sdk/
│   ├── __init__.py          # Main exports
│   ├── provider/            # RPC provider
│   │   ├── provider.py      # QfcProvider (wraps web3.py)
│   │   └── websocket.py     # WebSocket subscriptions
│   ├── wallet/              # Wallet management
│   │   └── wallet.py        # QfcWallet with staking
│   ├── staking/             # Staking client
│   │   └── client.py        # High-level staking API
│   ├── contracts/           # Contract helpers
│   │   ├── erc20.py         # ERC-20 wrapper
│   │   ├── erc721.py        # ERC-721 wrapper
│   │   ├── erc1155.py       # ERC-1155 wrapper
│   │   └── multicall.py     # Multicall3 batching
│   ├── types/               # Type definitions
│   │   ├── network.py       # Network types
│   │   ├── block.py         # Block types
│   │   ├── transaction.py   # Transaction types
│   │   ├── validator.py     # Validator/staking types
│   │   └── account.py       # Account types
│   ├── utils/               # Utilities
│   │   ├── units.py         # Unit conversion
│   │   ├── validation.py    # Address validation
│   │   └── format.py        # Display formatting
│   └── constants/           # Constants
│       └── __init__.py      # Networks, ABIs, limits
├── tests/
│   ├── test_utils.py
│   └── test_types.py
├── pyproject.toml           # Project configuration
└── README.md
```

## Common Commands

```bash
# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Run tests with coverage
pytest --cov=qfc_sdk --cov-report=html

# Type checking
mypy src/qfc_sdk

# Linting
ruff check src/qfc_sdk

# Format code
black src/qfc_sdk
```

## Key Dependencies

- **web3.py** - Ethereum interaction
- **eth-account** - Account management
- **pydantic** - Data validation

## Design Notes

- Wraps web3.py instead of reimplementing
- Uses pydantic for all data models
- Synchronous API (async planned for future)
- Type hints throughout (strict mypy)

## Testing

Tests use pytest with pytest-asyncio for any async code:

```bash
# Run specific test file
pytest tests/test_utils.py -v

# Run tests matching pattern
pytest -k "test_parse" -v
```

## Publishing

```bash
# Build
python -m build

# Publish to PyPI
twine upload dist/*
```
