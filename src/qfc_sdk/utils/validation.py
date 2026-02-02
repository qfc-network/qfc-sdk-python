"""Validation utilities."""

import re
from eth_utils import is_checksum_address, to_checksum_address


def is_valid_address(address: str) -> bool:
    """Check if a string is a valid Ethereum address.

    Args:
        address: The address to validate

    Returns:
        True if valid, False otherwise

    Examples:
        >>> is_valid_address("0x742d35Cc6634C0532925a3b844Bc9e7595f12345")
        True
        >>> is_valid_address("0xinvalid")
        False
    """
    if not isinstance(address, str):
        return False

    if not address.startswith("0x"):
        return False

    if len(address) != 42:
        return False

    # Check if it's a valid hex string
    try:
        int(address, 16)
    except ValueError:
        return False

    # If it has mixed case, validate checksum
    if address != address.lower() and address != address.upper():
        try:
            return is_checksum_address(address)
        except Exception:
            return False

    return True


def to_checksum(address: str) -> str:
    """Convert an address to checksum format.

    Args:
        address: The address to convert

    Returns:
        Checksummed address

    Raises:
        ValueError: If address is invalid
    """
    if not is_valid_address(address):
        raise ValueError(f"Invalid address: {address}")
    return to_checksum_address(address)


def is_valid_private_key(key: str) -> bool:
    """Check if a string is a valid private key.

    Args:
        key: The private key to validate

    Returns:
        True if valid, False otherwise
    """
    if not isinstance(key, str):
        return False

    # Remove 0x prefix if present
    if key.startswith("0x"):
        key = key[2:]

    # Must be 64 hex characters (32 bytes)
    if len(key) != 64:
        return False

    # Check if it's a valid hex string
    try:
        value = int(key, 16)
        # Private key must be > 0 and < secp256k1 order
        secp256k1_order = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
        return 0 < value < secp256k1_order
    except ValueError:
        return False


def is_valid_tx_hash(tx_hash: str) -> bool:
    """Check if a string is a valid transaction hash.

    Args:
        tx_hash: The transaction hash to validate

    Returns:
        True if valid, False otherwise
    """
    if not isinstance(tx_hash, str):
        return False

    if not tx_hash.startswith("0x"):
        return False

    if len(tx_hash) != 66:
        return False

    try:
        int(tx_hash, 16)
        return True
    except ValueError:
        return False


def is_valid_mnemonic(mnemonic: str) -> bool:
    """Check if a mnemonic phrase is valid.

    Args:
        mnemonic: The mnemonic phrase to validate

    Returns:
        True if valid, False otherwise
    """
    if not isinstance(mnemonic, str):
        return False

    words = mnemonic.strip().split()

    # Must be 12, 15, 18, 21, or 24 words
    if len(words) not in (12, 15, 18, 21, 24):
        return False

    # Check all words are lowercase alphabetic
    for word in words:
        if not word.isalpha() or not word.islower():
            return False

    return True


def is_valid_block_tag(tag: str | int) -> bool:
    """Check if a block tag is valid.

    Args:
        tag: Block number or tag ("latest", "pending", "earliest")

    Returns:
        True if valid, False otherwise
    """
    if isinstance(tag, int):
        return tag >= 0

    if isinstance(tag, str):
        return tag in ("latest", "pending", "earliest", "safe", "finalized")

    return False
