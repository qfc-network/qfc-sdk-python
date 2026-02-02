"""ERC-20 token helper."""

from web3 import Web3
from web3.contract import Contract

from qfc_sdk.provider import QfcProvider
from qfc_sdk.wallet import QfcWallet
from qfc_sdk.wallet.wallet import TransactionResponse
from qfc_sdk.constants import ERC20_ABI, GAS_LIMITS


class ERC20Token:
    """ERC-20 token wrapper.

    Examples:
        >>> token = get_erc20("0xTokenAddress...", provider)
        >>> print(f"Name: {token.name}")
        >>> balance = token.balance_of("0x...")
    """

    def __init__(
        self,
        address: str,
        provider: QfcProvider,
        wallet: QfcWallet | None = None,
    ):
        """Initialize the ERC-20 token.

        Args:
            address: Token contract address
            provider: QFC provider
            wallet: Optional wallet for write operations
        """
        self.address = Web3.to_checksum_address(address)
        self._provider = provider
        self._wallet = wallet
        self._contract: Contract = provider.web3.eth.contract(
            address=self.address,
            abi=ERC20_ABI,
        )

        # Cache token info
        self._name: str | None = None
        self._symbol: str | None = None
        self._decimals: int | None = None

    @property
    def name(self) -> str:
        """Get the token name."""
        if self._name is None:
            self._name = self._contract.functions.name().call()
        return self._name

    @property
    def symbol(self) -> str:
        """Get the token symbol."""
        if self._symbol is None:
            self._symbol = self._contract.functions.symbol().call()
        return self._symbol

    @property
    def decimals(self) -> int:
        """Get the token decimals."""
        if self._decimals is None:
            self._decimals = self._contract.functions.decimals().call()
        return self._decimals

    def total_supply(self) -> int:
        """Get the total supply.

        Returns:
            Total supply in smallest units
        """
        return self._contract.functions.totalSupply().call()

    def balance_of(self, address: str) -> int:
        """Get the balance of an address.

        Args:
            address: Account address

        Returns:
            Balance in smallest units
        """
        return self._contract.functions.balanceOf(
            Web3.to_checksum_address(address)
        ).call()

    def allowance(self, owner: str, spender: str) -> int:
        """Get the allowance for a spender.

        Args:
            owner: Token owner address
            spender: Spender address

        Returns:
            Allowance in smallest units
        """
        return self._contract.functions.allowance(
            Web3.to_checksum_address(owner),
            Web3.to_checksum_address(spender),
        ).call()

    def transfer(self, to: str, amount: int) -> TransactionResponse:
        """Transfer tokens to an address.

        Args:
            to: Recipient address
            amount: Amount in smallest units

        Returns:
            TransactionResponse
        """
        if self._wallet is None:
            raise ValueError("Wallet required for write operations")

        tx = self._contract.functions.transfer(
            Web3.to_checksum_address(to),
            amount,
        ).build_transaction({
            "from": self._wallet.address,
            "gas": GAS_LIMITS["ERC20_TRANSFER"],
            "nonce": self._wallet.get_nonce(),
            "chainId": self._provider.chain_id,
            "gasPrice": self._provider.get_gas_price(),
        })

        signed_tx = self._wallet.sign_transaction(tx)
        tx_hash = self._provider.send_raw_transaction(signed_tx)
        return TransactionResponse(tx_hash, self._provider)

    def approve(self, spender: str, amount: int) -> TransactionResponse:
        """Approve a spender to use tokens.

        Args:
            spender: Spender address
            amount: Amount to approve

        Returns:
            TransactionResponse
        """
        if self._wallet is None:
            raise ValueError("Wallet required for write operations")

        tx = self._contract.functions.approve(
            Web3.to_checksum_address(spender),
            amount,
        ).build_transaction({
            "from": self._wallet.address,
            "gas": GAS_LIMITS["ERC20_APPROVE"],
            "nonce": self._wallet.get_nonce(),
            "chainId": self._provider.chain_id,
            "gasPrice": self._provider.get_gas_price(),
        })

        signed_tx = self._wallet.sign_transaction(tx)
        tx_hash = self._provider.send_raw_transaction(signed_tx)
        return TransactionResponse(tx_hash, self._provider)

    def transfer_from(self, from_addr: str, to: str, amount: int) -> TransactionResponse:
        """Transfer tokens from one address to another.

        Args:
            from_addr: Source address
            to: Destination address
            amount: Amount to transfer

        Returns:
            TransactionResponse
        """
        if self._wallet is None:
            raise ValueError("Wallet required for write operations")

        tx = self._contract.functions.transferFrom(
            Web3.to_checksum_address(from_addr),
            Web3.to_checksum_address(to),
            amount,
        ).build_transaction({
            "from": self._wallet.address,
            "gas": GAS_LIMITS["ERC20_TRANSFER"],
            "nonce": self._wallet.get_nonce(),
            "chainId": self._provider.chain_id,
            "gasPrice": self._provider.get_gas_price(),
        })

        signed_tx = self._wallet.sign_transaction(tx)
        tx_hash = self._provider.send_raw_transaction(signed_tx)
        return TransactionResponse(tx_hash, self._provider)


def get_erc20(
    address: str,
    provider_or_wallet: QfcProvider | QfcWallet,
) -> ERC20Token:
    """Get an ERC-20 token instance.

    Args:
        address: Token contract address
        provider_or_wallet: Provider or wallet

    Returns:
        ERC20Token instance
    """
    if isinstance(provider_or_wallet, QfcWallet):
        return ERC20Token(address, provider_or_wallet.provider, provider_or_wallet)
    return ERC20Token(address, provider_or_wallet)
