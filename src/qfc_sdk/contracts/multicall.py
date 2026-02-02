"""Multicall3 helper for batching calls."""

from typing import Any, NamedTuple
from web3 import Web3
from web3.contract import Contract

from qfc_sdk.provider import QfcProvider
from qfc_sdk.constants import CONTRACTS, MULTICALL3_ABI


class Call(NamedTuple):
    """A single call for multicall."""

    target: str
    allow_failure: bool
    call_data: bytes


class CallResult(NamedTuple):
    """Result of a multicall."""

    success: bool
    return_data: bytes


class Multicall3:
    """Multicall3 wrapper for batching RPC calls.

    Examples:
        >>> multicall = get_multicall3(provider)
        >>> results = multicall.aggregate3([
        ...     Call(token_address, False, encode_balance_of(addr1)),
        ...     Call(token_address, False, encode_balance_of(addr2)),
        ... ])
    """

    def __init__(self, provider: QfcProvider, address: str | None = None):
        """Initialize Multicall3.

        Args:
            provider: QFC provider
            address: Override contract address
        """
        self._provider = provider
        self.address = Web3.to_checksum_address(
            address or CONTRACTS["MULTICALL3"]
        )
        self._contract: Contract = provider.web3.eth.contract(
            address=self.address,
            abi=MULTICALL3_ABI,
        )

    def aggregate(
        self,
        calls: list[tuple[str, bytes]],
    ) -> tuple[int, list[bytes]]:
        """Execute multiple calls and return results.

        Args:
            calls: List of (target, callData) tuples

        Returns:
            Tuple of (block_number, return_data_list)
        """
        formatted_calls = [
            (Web3.to_checksum_address(target), call_data)
            for target, call_data in calls
        ]

        result = self._contract.functions.aggregate(formatted_calls).call()
        return result[0], result[1]

    def aggregate3(self, calls: list[Call]) -> list[CallResult]:
        """Execute multiple calls with failure handling.

        Args:
            calls: List of Call namedtuples

        Returns:
            List of CallResult namedtuples
        """
        formatted_calls = [
            (Web3.to_checksum_address(call.target), call.allow_failure, call.call_data)
            for call in calls
        ]

        results = self._contract.functions.aggregate3(formatted_calls).call()
        return [
            CallResult(success=r[0], return_data=r[1])
            for r in results
        ]

    def try_aggregate(
        self,
        require_success: bool,
        calls: list[tuple[str, bytes]],
    ) -> list[CallResult]:
        """Execute calls with optional success requirement.

        Args:
            require_success: Whether all calls must succeed
            calls: List of (target, callData) tuples

        Returns:
            List of CallResult namedtuples
        """
        # Use aggregate3 with allow_failure based on require_success
        call_list = [
            Call(
                target=target,
                allow_failure=not require_success,
                call_data=call_data,
            )
            for target, call_data in calls
        ]
        return self.aggregate3(call_list)

    def get_eth_balance(self, address: str) -> int:
        """Get ETH balance via multicall.

        Args:
            address: Address to check

        Returns:
            Balance in wei
        """
        return self._contract.functions.getEthBalance(
            Web3.to_checksum_address(address)
        ).call()

    def get_block_number(self) -> int:
        """Get current block number.

        Returns:
            Block number
        """
        return self._contract.functions.getBlockNumber().call()

    def get_current_block_timestamp(self) -> int:
        """Get current block timestamp.

        Returns:
            Timestamp in seconds
        """
        return self._contract.functions.getCurrentBlockTimestamp().call()

    def get_balances(self, addresses: list[str]) -> list[int]:
        """Get ETH balances for multiple addresses.

        Args:
            addresses: List of addresses

        Returns:
            List of balances in wei
        """
        calls = [
            Call(
                target=self.address,
                allow_failure=False,
                call_data=self._contract.encodeABI(
                    fn_name="getEthBalance",
                    args=[Web3.to_checksum_address(addr)],
                ),
            )
            for addr in addresses
        ]

        results = self.aggregate3(calls)
        return [
            int.from_bytes(r.return_data, "big")
            for r in results
            if r.success
        ]


def get_multicall3(
    provider: QfcProvider,
    address: str | None = None,
) -> Multicall3:
    """Get a Multicall3 instance.

    Args:
        provider: QFC provider
        address: Optional override address

    Returns:
        Multicall3 instance
    """
    return Multicall3(provider, address)
