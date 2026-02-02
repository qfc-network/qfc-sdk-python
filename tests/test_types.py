"""Tests for type definitions."""

import pytest
from qfc_sdk.types import (
    Network,
    NetworkConfig,
    Block,
    Transaction,
    TransactionReceipt,
    Validator,
    StakeInfo,
)


class TestNetworkTypes:
    """Test network types."""

    def test_network_enum(self):
        """Test Network enum values."""
        assert Network.LOCALHOST == "localhost"
        assert Network.TESTNET == "testnet"
        assert Network.MAINNET == "mainnet"

    def test_network_config(self):
        """Test NetworkConfig model."""
        config = NetworkConfig(
            name="Test",
            chain_id=9000,
            rpc_url="http://localhost:8545",
        )
        assert config.name == "Test"
        assert config.chain_id == 9000
        assert config.currency_symbol == "QFC"
        assert config.currency_decimals == 18


class TestBlockTypes:
    """Test block types."""

    def test_block_model(self):
        """Test Block model."""
        block = Block(
            number=100,
            hash="0x" + "a" * 64,
            parent_hash="0x" + "b" * 64,
            timestamp=1234567890,
            producer="0x" + "c" * 40,
            gas_limit=30000000,
            gas_used=21000,
            transaction_count=1,
        )
        assert block.number == 100
        assert block.gas_used == 21000


class TestTransactionTypes:
    """Test transaction types."""

    def test_transaction_model(self):
        """Test Transaction model."""
        tx = Transaction(
            hash="0x" + "a" * 64,
            from_address="0x" + "b" * 40,
            to="0x" + "c" * 40,
            value=1000,
            gas=21000,
            nonce=0,
            data="0x",
        )
        assert tx.hash == "0x" + "a" * 64
        assert tx.value == 1000

    def test_transaction_receipt_success(self):
        """Test TransactionReceipt success property."""
        receipt = TransactionReceipt(
            transaction_hash="0x" + "a" * 64,
            transaction_index=0,
            block_hash="0x" + "b" * 64,
            block_number=100,
            from_address="0x" + "c" * 40,
            gas_used=21000,
            cumulative_gas_used=21000,
            effective_gas_price=1000000000,
            status=1,
        )
        assert receipt.success is True

        failed_receipt = TransactionReceipt(
            transaction_hash="0x" + "a" * 64,
            transaction_index=0,
            block_hash="0x" + "b" * 64,
            block_number=100,
            from_address="0x" + "c" * 40,
            gas_used=21000,
            cumulative_gas_used=21000,
            effective_gas_price=1000000000,
            status=0,
        )
        assert failed_receipt.success is False


class TestValidatorTypes:
    """Test validator types."""

    def test_validator_model(self):
        """Test Validator model."""
        validator = Validator(
            address="0x" + "a" * 40,
            status="active",
            total_stake=10**21,
            self_stake=10**20,
            delegated_stake=9 * 10**20,
            commission_rate=500,
            contribution_score=8500,
            blocks_produced=1000,
            uptime=99.9,
        )
        assert validator.status == "active"
        assert validator.commission_rate == 500

    def test_stake_info_model(self):
        """Test StakeInfo model."""
        info = StakeInfo(
            address="0x" + "a" * 40,
            staked_amount=10**20,
            delegated_amount=5 * 10**19,
            pending_rewards=10**18,
            unstaking_amount=0,
        )
        assert info.staked_amount == 10**20
        assert info.is_validator is False
