"""QFC Wallet implementation."""

from typing import Any
from eth_account import Account
from eth_account.signers.local import LocalAccount
from eth_account.hdaccount import generate_mnemonic
from web3 import Web3
from web3.types import TxParams

from qfc_sdk.provider import QfcProvider
from qfc_sdk.types import TransactionReceipt, TransactionRequest
from qfc_sdk.constants import CONTRACTS, STAKING_ABI, GAS_LIMITS


class QfcWallet:
    """Wallet for signing transactions and interacting with QFC blockchain.

    Examples:
        >>> wallet = QfcWallet.from_private_key("0x...", provider)
        >>> tx = await wallet.send_transaction(to="0x...", value=parse_qfc("10"))
        >>> receipt = await tx.wait()
    """

    def __init__(self, account: LocalAccount, provider: QfcProvider):
        """Initialize the wallet.

        Args:
            account: eth-account LocalAccount instance
            provider: QFC provider for blockchain interaction
        """
        self._account = account
        self._provider = provider
        self._staking_contract = self._provider.web3.eth.contract(
            address=Web3.to_checksum_address(CONTRACTS["STAKING_TESTNET"]),
            abi=STAKING_ABI,
        )

    @property
    def address(self) -> str:
        """Get the wallet address."""
        return self._account.address

    @property
    def private_key(self) -> str:
        """Get the private key (hex string with 0x prefix)."""
        return self._account.key.hex()

    @property
    def provider(self) -> QfcProvider:
        """Get the provider."""
        return self._provider

    @classmethod
    def from_private_key(cls, private_key: str, provider: QfcProvider) -> "QfcWallet":
        """Create a wallet from a private key.

        Args:
            private_key: Private key (hex string, with or without 0x prefix)
            provider: QFC provider

        Returns:
            QfcWallet instance
        """
        account = Account.from_key(private_key)
        return cls(account, provider)

    @classmethod
    def from_mnemonic(
        cls,
        mnemonic: str,
        provider: QfcProvider,
        path: str = "m/44'/60'/0'/0/0",
    ) -> "QfcWallet":
        """Create a wallet from a mnemonic phrase.

        Args:
            mnemonic: 12 or 24 word mnemonic
            provider: QFC provider
            path: Derivation path (default: Ethereum standard)

        Returns:
            QfcWallet instance
        """
        Account.enable_unaudited_hdwallet_features()
        account = Account.from_mnemonic(mnemonic, account_path=path)
        return cls(account, provider)

    @classmethod
    def create_random(cls, provider: QfcProvider) -> tuple["QfcWallet", str]:
        """Create a new random wallet.

        Args:
            provider: QFC provider

        Returns:
            Tuple of (wallet, mnemonic)
        """
        Account.enable_unaudited_hdwallet_features()
        mnemonic = generate_mnemonic(num_words=12, lang="english")
        wallet = cls.from_mnemonic(mnemonic, provider)
        return wallet, mnemonic

    def get_balance(self) -> int:
        """Get the wallet's balance.

        Returns:
            Balance in wei
        """
        return self._provider.get_balance(self.address)

    def get_nonce(self) -> int:
        """Get the current nonce.

        Returns:
            Transaction count (nonce)
        """
        return self._provider.get_transaction_count(self.address)

    def sign_transaction(self, tx: TxParams) -> bytes:
        """Sign a transaction.

        Args:
            tx: Transaction parameters

        Returns:
            Signed transaction bytes
        """
        # Fill in defaults
        if "nonce" not in tx:
            tx["nonce"] = self.get_nonce()
        if "chainId" not in tx:
            tx["chainId"] = self._provider.chain_id
        if "gas" not in tx:
            tx["gas"] = self._provider.estimate_gas(tx)
        if "gasPrice" not in tx and "maxFeePerGas" not in tx:
            tx["gasPrice"] = self._provider.get_gas_price()

        signed = self._account.sign_transaction(tx)
        return signed.rawTransaction

    def send_transaction(self, tx: TransactionRequest | dict[str, Any]) -> "TransactionResponse":
        """Send a transaction.

        Args:
            tx: Transaction parameters

        Returns:
            TransactionResponse for tracking
        """
        if isinstance(tx, TransactionRequest):
            tx_params: TxParams = {
                "from": self.address,
                "to": tx.to,
                "value": tx.value,
                "data": tx.data,
            }
            if tx.gas:
                tx_params["gas"] = tx.gas
            if tx.gas_price:
                tx_params["gasPrice"] = tx.gas_price
            if tx.nonce:
                tx_params["nonce"] = tx.nonce
        else:
            tx_params = {"from": self.address, **tx}

        signed_tx = self.sign_transaction(tx_params)
        tx_hash = self._provider.send_raw_transaction(signed_tx)
        return TransactionResponse(tx_hash, self._provider)

    def sign_message(self, message: str | bytes) -> str:
        """Sign a message.

        Args:
            message: Message to sign (string or bytes)

        Returns:
            Signature hex string
        """
        if isinstance(message, str):
            message = message.encode()

        signed = self._account.sign_message(
            {"raw": message}
        )
        return signed.signature.hex()

    # Staking methods

    def stake(self, amount: int) -> "TransactionResponse":
        """Stake QFC tokens.

        Args:
            amount: Amount to stake in wei

        Returns:
            TransactionResponse
        """
        tx = self._staking_contract.functions.stake().build_transaction({
            "from": self.address,
            "value": amount,
            "gas": GAS_LIMITS["STAKE"],
            "nonce": self.get_nonce(),
            "chainId": self._provider.chain_id,
            "gasPrice": self._provider.get_gas_price(),
        })

        signed_tx = self.sign_transaction(tx)
        tx_hash = self._provider.send_raw_transaction(signed_tx)
        return TransactionResponse(tx_hash, self._provider)

    def unstake(self, amount: int) -> "TransactionResponse":
        """Unstake QFC tokens.

        Args:
            amount: Amount to unstake in wei

        Returns:
            TransactionResponse
        """
        tx = self._staking_contract.functions.unstake(amount).build_transaction({
            "from": self.address,
            "gas": GAS_LIMITS["UNSTAKE"],
            "nonce": self.get_nonce(),
            "chainId": self._provider.chain_id,
            "gasPrice": self._provider.get_gas_price(),
        })

        signed_tx = self.sign_transaction(tx)
        tx_hash = self._provider.send_raw_transaction(signed_tx)
        return TransactionResponse(tx_hash, self._provider)

    def delegate(self, validator: str, amount: int) -> "TransactionResponse":
        """Delegate tokens to a validator.

        Args:
            validator: Validator address
            amount: Amount to delegate in wei

        Returns:
            TransactionResponse
        """
        tx = self._staking_contract.functions.delegate(
            Web3.to_checksum_address(validator),
            amount,
        ).build_transaction({
            "from": self.address,
            "gas": GAS_LIMITS["DELEGATE"],
            "nonce": self.get_nonce(),
            "chainId": self._provider.chain_id,
            "gasPrice": self._provider.get_gas_price(),
        })

        signed_tx = self.sign_transaction(tx)
        tx_hash = self._provider.send_raw_transaction(signed_tx)
        return TransactionResponse(tx_hash, self._provider)

    def undelegate(self, validator: str, amount: int) -> "TransactionResponse":
        """Undelegate tokens from a validator.

        Args:
            validator: Validator address
            amount: Amount to undelegate in wei

        Returns:
            TransactionResponse
        """
        tx = self._staking_contract.functions.undelegate(
            Web3.to_checksum_address(validator),
            amount,
        ).build_transaction({
            "from": self.address,
            "gas": GAS_LIMITS["UNDELEGATE"],
            "nonce": self.get_nonce(),
            "chainId": self._provider.chain_id,
            "gasPrice": self._provider.get_gas_price(),
        })

        signed_tx = self.sign_transaction(tx)
        tx_hash = self._provider.send_raw_transaction(signed_tx)
        return TransactionResponse(tx_hash, self._provider)

    def claim_rewards(self) -> "TransactionResponse":
        """Claim staking rewards.

        Returns:
            TransactionResponse
        """
        tx = self._staking_contract.functions.claimRewards().build_transaction({
            "from": self.address,
            "gas": GAS_LIMITS["CLAIM_REWARDS"],
            "nonce": self.get_nonce(),
            "chainId": self._provider.chain_id,
            "gasPrice": self._provider.get_gas_price(),
        })

        signed_tx = self.sign_transaction(tx)
        tx_hash = self._provider.send_raw_transaction(signed_tx)
        return TransactionResponse(tx_hash, self._provider)


class TransactionResponse:
    """Response from sending a transaction."""

    def __init__(self, tx_hash: str, provider: QfcProvider):
        """Initialize the response.

        Args:
            tx_hash: Transaction hash
            provider: QFC provider
        """
        self.hash = tx_hash
        self._provider = provider

    def wait(self, timeout: int = 120) -> TransactionReceipt:
        """Wait for the transaction to be mined.

        Args:
            timeout: Timeout in seconds

        Returns:
            Transaction receipt
        """
        return self._provider.wait_for_transaction(self.hash, timeout)

    def __repr__(self) -> str:
        """String representation."""
        return f"TransactionResponse(hash={self.hash})"
