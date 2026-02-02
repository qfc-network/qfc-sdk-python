"""WebSocket Provider for QFC SDK."""

from typing import Any, Callable
from web3 import Web3

from qfc_sdk.constants import NETWORKS


class QfcWebSocketProvider:
    """WebSocket provider for real-time updates.

    Examples:
        >>> async with QfcWebSocketProvider("wss://ws.testnet.qfc.network") as provider:
        ...     async for block in provider.subscribe_blocks():
        ...         print(f"New block: {block['number']}")
    """

    def __init__(self, ws_url: str | None = None, network: str = "testnet"):
        """Initialize the WebSocket provider.

        Args:
            ws_url: WebSocket endpoint URL
            network: Network name
        """
        if ws_url is None:
            if network not in NETWORKS:
                raise ValueError(f"Unknown network: {network}")
            ws_url = NETWORKS[network].ws_url
            if ws_url is None:
                raise ValueError(f"Network {network} does not have a WebSocket endpoint")

        self.ws_url = ws_url
        self._web3: Web3 | None = None
        self._subscriptions: dict[str, Callable[[Any], None]] = {}

    async def connect(self) -> None:
        """Connect to the WebSocket endpoint."""
        self._web3 = Web3(Web3.WebsocketProvider(self.ws_url))

    async def disconnect(self) -> None:
        """Disconnect from the WebSocket endpoint."""
        if self._web3 and self._web3.provider:
            # Clean up subscriptions
            self._subscriptions.clear()
            self._web3 = None

    async def __aenter__(self) -> "QfcWebSocketProvider":
        """Async context manager entry."""
        await self.connect()
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Async context manager exit."""
        await self.disconnect()

    def subscribe_new_heads(self, callback: Callable[[dict[str, Any]], None]) -> str:
        """Subscribe to new block headers.

        Args:
            callback: Function to call with each new block header

        Returns:
            Subscription ID
        """
        if self._web3 is None:
            raise RuntimeError("Not connected. Call connect() first.")

        subscription_id = self._web3.eth.subscribe("newHeads")
        self._subscriptions[subscription_id] = callback
        return subscription_id

    def subscribe_pending_transactions(self, callback: Callable[[str], None]) -> str:
        """Subscribe to pending transactions.

        Args:
            callback: Function to call with each pending transaction hash

        Returns:
            Subscription ID
        """
        if self._web3 is None:
            raise RuntimeError("Not connected. Call connect() first.")

        subscription_id = self._web3.eth.subscribe("pendingTransactions")
        self._subscriptions[subscription_id] = callback
        return subscription_id

    def subscribe_logs(
        self,
        callback: Callable[[dict[str, Any]], None],
        address: str | list[str] | None = None,
        topics: list[str | list[str] | None] | None = None,
    ) -> str:
        """Subscribe to contract logs.

        Args:
            callback: Function to call with each log
            address: Contract address(es) to filter
            topics: Topic filters

        Returns:
            Subscription ID
        """
        if self._web3 is None:
            raise RuntimeError("Not connected. Call connect() first.")

        filter_params: dict[str, Any] = {}
        if address:
            filter_params["address"] = address
        if topics:
            filter_params["topics"] = topics

        subscription_id = self._web3.eth.subscribe("logs", filter_params)
        self._subscriptions[subscription_id] = callback
        return subscription_id

    def unsubscribe(self, subscription_id: str) -> bool:
        """Unsubscribe from a subscription.

        Args:
            subscription_id: The subscription to cancel

        Returns:
            True if successful
        """
        if self._web3 is None:
            raise RuntimeError("Not connected.")

        if subscription_id in self._subscriptions:
            del self._subscriptions[subscription_id]

        return self._web3.eth.unsubscribe(subscription_id)
