"""Tests for utility functions."""

import pytest
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


class TestUnits:
    """Test unit conversion functions."""

    def test_parse_qfc_string(self):
        """Test parsing QFC from string."""
        assert parse_qfc("1") == 10**18
        assert parse_qfc("1.5") == 15 * 10**17
        assert parse_qfc("0.001") == 10**15

    def test_parse_qfc_int(self):
        """Test parsing QFC from int."""
        assert parse_qfc(1) == 10**18
        assert parse_qfc(10) == 10 * 10**18

    def test_parse_qfc_invalid(self):
        """Test parsing invalid QFC."""
        with pytest.raises(ValueError):
            parse_qfc("invalid")

    def test_format_qfc(self):
        """Test formatting wei to QFC."""
        assert format_qfc(10**18) == "1.0000"
        assert format_qfc(15 * 10**17) == "1.5000"
        assert format_qfc(10**18, 2) == "1.00"

    def test_parse_gwei(self):
        """Test parsing gwei."""
        assert parse_gwei("10") == 10 * 10**9
        assert parse_gwei(1) == 10**9

    def test_format_gwei(self):
        """Test formatting gwei."""
        assert format_gwei(10 * 10**9) == "10.0"


class TestValidation:
    """Test validation functions."""

    def test_is_valid_address_valid(self):
        """Test valid addresses."""
        assert is_valid_address("0x742d35Cc6634C0532925a3b844Bc9e7595f12345")
        assert is_valid_address("0x" + "a" * 40)
        assert is_valid_address("0x" + "A" * 40)

    def test_is_valid_address_invalid(self):
        """Test invalid addresses."""
        assert not is_valid_address("0xinvalid")
        assert not is_valid_address("not-an-address")
        assert not is_valid_address("0x123")  # too short
        assert not is_valid_address("")
        assert not is_valid_address(None)  # type: ignore

    def test_is_valid_private_key_valid(self):
        """Test valid private keys."""
        assert is_valid_private_key("0x" + "a" * 64)
        assert is_valid_private_key("a" * 64)

    def test_is_valid_private_key_invalid(self):
        """Test invalid private keys."""
        assert not is_valid_private_key("0x" + "a" * 63)  # too short
        assert not is_valid_private_key("invalid")
        assert not is_valid_private_key("")

    def test_is_valid_tx_hash_valid(self):
        """Test valid transaction hashes."""
        assert is_valid_tx_hash("0x" + "a" * 64)

    def test_is_valid_tx_hash_invalid(self):
        """Test invalid transaction hashes."""
        assert not is_valid_tx_hash("0x" + "a" * 63)
        assert not is_valid_tx_hash("invalid")


class TestFormatting:
    """Test formatting functions."""

    def test_shorten_address(self):
        """Test address shortening."""
        addr = "0x742d35Cc6634C0532925a3b844Bc9e7595f12345"
        assert shorten_address(addr) == "0x742d...2345"
        assert shorten_address(addr, 6, 6) == "0x742d35...f12345"

    def test_shorten_hash(self):
        """Test hash shortening."""
        hash_ = "0x" + "a" * 64
        assert shorten_hash(hash_) == "0xaaaa...aaaa"

    def test_shorten_short_string(self):
        """Test shortening already short strings."""
        assert shorten_address("0x1234") == "0x1234"
