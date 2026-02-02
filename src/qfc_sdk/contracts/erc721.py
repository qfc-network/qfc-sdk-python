"""ERC-721 NFT helper."""

from web3 import Web3
from web3.contract import Contract

from qfc_sdk.provider import QfcProvider
from qfc_sdk.wallet import QfcWallet
from qfc_sdk.wallet.wallet import TransactionResponse
from qfc_sdk.constants import ERC721_ABI


class ERC721Token:
    """ERC-721 NFT wrapper.

    Examples:
        >>> nft = get_erc721("0xNFTAddress...", provider)
        >>> owner = nft.owner_of(1)
        >>> uri = nft.token_uri(1)
    """

    def __init__(
        self,
        address: str,
        provider: QfcProvider,
        wallet: QfcWallet | None = None,
    ):
        """Initialize the ERC-721 token.

        Args:
            address: NFT contract address
            provider: QFC provider
            wallet: Optional wallet for write operations
        """
        self.address = Web3.to_checksum_address(address)
        self._provider = provider
        self._wallet = wallet
        self._contract: Contract = provider.web3.eth.contract(
            address=self.address,
            abi=ERC721_ABI,
        )

        self._name: str | None = None
        self._symbol: str | None = None

    @property
    def name(self) -> str:
        """Get the collection name."""
        if self._name is None:
            self._name = self._contract.functions.name().call()
        return self._name

    @property
    def symbol(self) -> str:
        """Get the collection symbol."""
        if self._symbol is None:
            self._symbol = self._contract.functions.symbol().call()
        return self._symbol

    def balance_of(self, address: str) -> int:
        """Get the number of NFTs owned by an address.

        Args:
            address: Owner address

        Returns:
            Number of NFTs
        """
        return self._contract.functions.balanceOf(
            Web3.to_checksum_address(address)
        ).call()

    def owner_of(self, token_id: int) -> str:
        """Get the owner of a token.

        Args:
            token_id: Token ID

        Returns:
            Owner address
        """
        return self._contract.functions.ownerOf(token_id).call()

    def token_uri(self, token_id: int) -> str:
        """Get the token URI.

        Args:
            token_id: Token ID

        Returns:
            Token URI string
        """
        return self._contract.functions.tokenURI(token_id).call()

    def get_approved(self, token_id: int) -> str:
        """Get the approved address for a token.

        Args:
            token_id: Token ID

        Returns:
            Approved address
        """
        return self._contract.functions.getApproved(token_id).call()

    def is_approved_for_all(self, owner: str, operator: str) -> bool:
        """Check if an operator is approved for all tokens.

        Args:
            owner: Owner address
            operator: Operator address

        Returns:
            True if approved
        """
        return self._contract.functions.isApprovedForAll(
            Web3.to_checksum_address(owner),
            Web3.to_checksum_address(operator),
        ).call()

    def approve(self, to: str, token_id: int) -> TransactionResponse:
        """Approve an address to transfer a token.

        Args:
            to: Address to approve
            token_id: Token ID

        Returns:
            TransactionResponse
        """
        if self._wallet is None:
            raise ValueError("Wallet required for write operations")

        tx = self._contract.functions.approve(
            Web3.to_checksum_address(to),
            token_id,
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

    def set_approval_for_all(self, operator: str, approved: bool) -> TransactionResponse:
        """Set approval for all tokens.

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

    def transfer_from(self, from_addr: str, to: str, token_id: int) -> TransactionResponse:
        """Transfer a token.

        Args:
            from_addr: Current owner
            to: New owner
            token_id: Token ID

        Returns:
            TransactionResponse
        """
        if self._wallet is None:
            raise ValueError("Wallet required for write operations")

        tx = self._contract.functions.transferFrom(
            Web3.to_checksum_address(from_addr),
            Web3.to_checksum_address(to),
            token_id,
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

    def safe_transfer_from(
        self,
        from_addr: str,
        to: str,
        token_id: int,
        data: bytes = b"",
    ) -> TransactionResponse:
        """Safely transfer a token.

        Args:
            from_addr: Current owner
            to: New owner
            token_id: Token ID
            data: Additional data

        Returns:
            TransactionResponse
        """
        if self._wallet is None:
            raise ValueError("Wallet required for write operations")

        if data:
            tx = self._contract.functions.safeTransferFrom(
                Web3.to_checksum_address(from_addr),
                Web3.to_checksum_address(to),
                token_id,
                data,
            ).build_transaction({
                "from": self._wallet.address,
                "gas": 120000,
                "nonce": self._wallet.get_nonce(),
                "chainId": self._provider.chain_id,
                "gasPrice": self._provider.get_gas_price(),
            })
        else:
            tx = self._contract.functions.safeTransferFrom(
                Web3.to_checksum_address(from_addr),
                Web3.to_checksum_address(to),
                token_id,
            ).build_transaction({
                "from": self._wallet.address,
                "gas": 120000,
                "nonce": self._wallet.get_nonce(),
                "chainId": self._provider.chain_id,
                "gasPrice": self._provider.get_gas_price(),
            })

        signed_tx = self._wallet.sign_transaction(tx)
        tx_hash = self._provider.send_raw_transaction(signed_tx)
        return TransactionResponse(tx_hash, self._provider)


def get_erc721(
    address: str,
    provider_or_wallet: QfcProvider | QfcWallet,
) -> ERC721Token:
    """Get an ERC-721 token instance.

    Args:
        address: NFT contract address
        provider_or_wallet: Provider or wallet

    Returns:
        ERC721Token instance
    """
    if isinstance(provider_or_wallet, QfcWallet):
        return ERC721Token(address, provider_or_wallet.provider, provider_or_wallet)
    return ERC721Token(address, provider_or_wallet)
