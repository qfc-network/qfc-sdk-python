"""ERC-1155 multi-token helper."""

from web3 import Web3
from web3.contract import Contract

from qfc_sdk.provider import QfcProvider
from qfc_sdk.wallet import QfcWallet
from qfc_sdk.wallet.wallet import TransactionResponse
from qfc_sdk.constants import ERC1155_ABI


class ERC1155Token:
    """ERC-1155 multi-token wrapper.

    Examples:
        >>> token = get_erc1155("0xAddress...", provider)
        >>> balance = token.balance_of("0x...", 1)
    """

    def __init__(
        self,
        address: str,
        provider: QfcProvider,
        wallet: QfcWallet | None = None,
    ):
        """Initialize the ERC-1155 token.

        Args:
            address: Contract address
            provider: QFC provider
            wallet: Optional wallet for write operations
        """
        self.address = Web3.to_checksum_address(address)
        self._provider = provider
        self._wallet = wallet
        self._contract: Contract = provider.web3.eth.contract(
            address=self.address,
            abi=ERC1155_ABI,
        )

    def uri(self, token_id: int) -> str:
        """Get the URI for a token ID.

        Args:
            token_id: Token ID

        Returns:
            URI string
        """
        return self._contract.functions.uri(token_id).call()

    def balance_of(self, account: str, token_id: int) -> int:
        """Get the balance of a specific token.

        Args:
            account: Account address
            token_id: Token ID

        Returns:
            Balance
        """
        return self._contract.functions.balanceOf(
            Web3.to_checksum_address(account),
            token_id,
        ).call()

    def balance_of_batch(
        self,
        accounts: list[str],
        token_ids: list[int],
    ) -> list[int]:
        """Get balances for multiple account/token pairs.

        Args:
            accounts: List of account addresses
            token_ids: List of token IDs

        Returns:
            List of balances
        """
        return self._contract.functions.balanceOfBatch(
            [Web3.to_checksum_address(a) for a in accounts],
            token_ids,
        ).call()

    def is_approved_for_all(self, account: str, operator: str) -> bool:
        """Check if an operator is approved.

        Args:
            account: Account address
            operator: Operator address

        Returns:
            True if approved
        """
        return self._contract.functions.isApprovedForAll(
            Web3.to_checksum_address(account),
            Web3.to_checksum_address(operator),
        ).call()

    def set_approval_for_all(self, operator: str, approved: bool) -> TransactionResponse:
        """Set approval for an operator.

        Args:
            operator: Operator address
            approved: Whether to approve

        Returns:
            TransactionResponse
        """
        if self._wallet is None:
            raise ValueError("Wallet required for write operations")

        tx = self._contract.functions.setApprovalForAll(
            Web3.to_checksum_address(operator),
            approved,
        ).build_transaction({
            "from": self._wallet.address,
            "gas": 60000,
            "nonce": self._wallet.get_nonce(),
            "chainId": self._provider.chain_id,
            "gasPrice": self._provider.get_gas_price(),
        })

        signed_tx = self._wallet.sign_transaction(tx)
        tx_hash = self._provider.send_raw_transaction(signed_tx)
        return TransactionResponse(tx_hash, self._provider)

    def safe_transfer_from(
        self,
        from_addr: str,
        to: str,
        token_id: int,
        amount: int,
        data: bytes = b"",
    ) -> TransactionResponse:
        """Transfer tokens.

        Args:
            from_addr: Source address
            to: Destination address
            token_id: Token ID
            amount: Amount to transfer
            data: Additional data

        Returns:
            TransactionResponse
        """
        if self._wallet is None:
            raise ValueError("Wallet required for write operations")

        tx = self._contract.functions.safeTransferFrom(
            Web3.to_checksum_address(from_addr),
            Web3.to_checksum_address(to),
            token_id,
            amount,
            data,
        ).build_transaction({
            "from": self._wallet.address,
            "gas": 100000,
            "nonce": self._wallet.get_nonce(),
            "chainId": self._provider.chain_id,
            "gasPrice": self._provider.get_gas_price(),
        })

        signed_tx = self._wallet.sign_transaction(tx)
        tx_hash = self._provider.send_raw_transaction(signed_tx)
        return TransactionResponse(tx_hash, self._provider)

    def safe_batch_transfer_from(
        self,
        from_addr: str,
        to: str,
        token_ids: list[int],
        amounts: list[int],
        data: bytes = b"",
    ) -> TransactionResponse:
        """Batch transfer tokens.

        Args:
            from_addr: Source address
            to: Destination address
            token_ids: List of token IDs
            amounts: List of amounts
            data: Additional data

        Returns:
            TransactionResponse
        """
        if self._wallet is None:
            raise ValueError("Wallet required for write operations")

        tx = self._contract.functions.safeBatchTransferFrom(
            Web3.to_checksum_address(from_addr),
            Web3.to_checksum_address(to),
            token_ids,
            amounts,
            data,
        ).build_transaction({
            "from": self._wallet.address,
            "gas": 150000,
            "nonce": self._wallet.get_nonce(),
            "chainId": self._provider.chain_id,
            "gasPrice": self._provider.get_gas_price(),
        })

        signed_tx = self._wallet.sign_transaction(tx)
        tx_hash = self._provider.send_raw_transaction(signed_tx)
        return TransactionResponse(tx_hash, self._provider)


def get_erc1155(
    address: str,
    provider_or_wallet: QfcProvider | QfcWallet,
) -> ERC1155Token:
    """Get an ERC-1155 token instance.

    Args:
        address: Contract address
        provider_or_wallet: Provider or wallet

    Returns:
        ERC1155Token instance
    """
    if isinstance(provider_or_wallet, QfcWallet):
        return ERC1155Token(address, provider_or_wallet.provider, provider_or_wallet)
    return ERC1155Token(address, provider_or_wallet)
