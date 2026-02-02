"""QFC JSON-RPC Provider."""

from typing import Any
from web3 import Web3
from web3.types import BlockIdentifier, TxParams

from qfc_sdk.types import Block, Transaction, TransactionReceipt, Validator, ContributionScore
from qfc_sdk.constants import NETWORKS


class QfcProvider:
    """JSON-RPC provider for QFC blockchain.

    Wraps web3.py with QFC-specific methods.

    Examples:
        >>> provider = QfcProvider("https://rpc.testnet.qfc.network")
        >>> balance = await provider.get_balance("0x...")
        >>> validators = await provider.get_validators()
    """

    def __init__(self, rpc_url: str | None = None, network: str = "testnet"):
        """Initialize the provider.

        Args:
            rpc_url: RPC endpoint URL (optional if network is specified)
            network: Network name ("localhost", "testnet", "mainnet")
        """
        if rpc_url is None:
            if network not in NETWORKS:
                raise ValueError(f"Unknown network: {network}")
            rpc_url = NETWORKS[network].rpc_url

        self.rpc_url = rpc_url
        self._web3 = Web3(Web3.HTTPProvider(rpc_url))
        self._network = network

    @property
    def web3(self) -> Web3:
        """Get the underlying web3 instance."""
        return self._web3

    @property
    def chain_id(self) -> int:
        """Get the chain ID."""
        return self._web3.eth.chain_id

    # Standard Ethereum methods

    def get_balance(self, address: str, block: BlockIdentifier = "latest") -> int:
        """Get the balance of an address.

        Args:
            address: The address to query
            block: Block identifier (number, hash, or tag)

        Returns:
            Balance in wei
        """
        return self._web3.eth.get_balance(address, block)

    def get_transaction_count(self, address: str, block: BlockIdentifier = "latest") -> int:
        """Get the transaction count (nonce) of an address.

        Args:
            address: The address to query
            block: Block identifier

        Returns:
            Transaction count
        """
        return self._web3.eth.get_transaction_count(address, block)

    def get_code(self, address: str, block: BlockIdentifier = "latest") -> bytes:
        """Get the code at an address.

        Args:
            address: The contract address
            block: Block identifier

        Returns:
            Contract bytecode
        """
        return self._web3.eth.get_code(address, block)

    def get_block_number(self) -> int:
        """Get the current block number.

        Returns:
            Current block number
        """
        return self._web3.eth.block_number

    def get_block(self, block: BlockIdentifier = "latest", full_transactions: bool = False) -> Block:
        """Get a block by number or hash.

        Args:
            block: Block number, hash, or tag
            full_transactions: Include full transaction objects

        Returns:
            Block information
        """
        block_data = self._web3.eth.get_block(block, full_transactions)
        return Block(
            number=block_data["number"],
            hash=block_data["hash"].hex(),
            parent_hash=block_data["parentHash"].hex(),
            timestamp=block_data["timestamp"],
            producer=block_data["miner"],
            gas_limit=block_data["gasLimit"],
            gas_used=block_data["gasUsed"],
            base_fee_per_gas=block_data.get("baseFeePerGas"),
            transaction_count=len(block_data["transactions"]),
            transactions=[
                tx.hex() if isinstance(tx, bytes) else tx["hash"].hex()
                for tx in block_data["transactions"]
            ] if not full_transactions else None,
        )

    def get_transaction(self, tx_hash: str) -> Transaction:
        """Get a transaction by hash.

        Args:
            tx_hash: Transaction hash

        Returns:
            Transaction information
        """
        tx = self._web3.eth.get_transaction(tx_hash)
        return Transaction(
            hash=tx["hash"].hex(),
            block_number=tx.get("blockNumber"),
            block_hash=tx.get("blockHash").hex() if tx.get("blockHash") else None,
            from_address=tx["from"],
            to=tx.get("to"),
            value=tx["value"],
            gas=tx["gas"],
            gas_price=tx.get("gasPrice"),
            max_fee_per_gas=tx.get("maxFeePerGas"),
            max_priority_fee_per_gas=tx.get("maxPriorityFeePerGas"),
            nonce=tx["nonce"],
            data=tx["input"].hex() if isinstance(tx["input"], bytes) else tx["input"],
            transaction_index=tx.get("transactionIndex"),
        )

    def get_transaction_receipt(self, tx_hash: str) -> TransactionReceipt | None:
        """Get a transaction receipt.

        Args:
            tx_hash: Transaction hash

        Returns:
            Transaction receipt or None if not found
        """
        receipt = self._web3.eth.get_transaction_receipt(tx_hash)
        if receipt is None:
            return None

        return TransactionReceipt(
            transaction_hash=receipt["transactionHash"].hex(),
            transaction_index=receipt["transactionIndex"],
            block_hash=receipt["blockHash"].hex(),
            block_number=receipt["blockNumber"],
            from_address=receipt["from"],
            to=receipt.get("to"),
            gas_used=receipt["gasUsed"],
            cumulative_gas_used=receipt["cumulativeGasUsed"],
            effective_gas_price=receipt.get("effectiveGasPrice", 0),
            status=receipt["status"],
            contract_address=receipt.get("contractAddress"),
            logs=[],  # Simplified for now
        )

    def send_raw_transaction(self, signed_tx: bytes | str) -> str:
        """Send a signed transaction.

        Args:
            signed_tx: Signed transaction data

        Returns:
            Transaction hash
        """
        tx_hash = self._web3.eth.send_raw_transaction(signed_tx)
        return tx_hash.hex()

    def call(self, tx: TxParams, block: BlockIdentifier = "latest") -> bytes:
        """Execute a call without creating a transaction.

        Args:
            tx: Transaction parameters
            block: Block identifier

        Returns:
            Call result
        """
        return self._web3.eth.call(tx, block)

    def estimate_gas(self, tx: TxParams) -> int:
        """Estimate gas for a transaction.

        Args:
            tx: Transaction parameters

        Returns:
            Estimated gas
        """
        return self._web3.eth.estimate_gas(tx)

    def get_gas_price(self) -> int:
        """Get the current gas price.

        Returns:
            Gas price in wei
        """
        return self._web3.eth.gas_price

    def get_fee_data(self) -> dict[str, int | None]:
        """Get current fee data (EIP-1559).

        Returns:
            Dictionary with gas price information
        """
        try:
            block = self._web3.eth.get_block("latest")
            base_fee = block.get("baseFeePerGas")
            max_priority_fee = self._web3.eth.max_priority_fee
            max_fee = (base_fee * 2 + max_priority_fee) if base_fee else None

            return {
                "gas_price": self._web3.eth.gas_price,
                "base_fee": base_fee,
                "max_priority_fee": max_priority_fee,
                "max_fee": max_fee,
            }
        except Exception:
            return {
                "gas_price": self._web3.eth.gas_price,
                "base_fee": None,
                "max_priority_fee": None,
                "max_fee": None,
            }

    def wait_for_transaction(self, tx_hash: str, timeout: int = 120) -> TransactionReceipt:
        """Wait for a transaction to be mined.

        Args:
            tx_hash: Transaction hash
            timeout: Timeout in seconds

        Returns:
            Transaction receipt
        """
        receipt = self._web3.eth.wait_for_transaction_receipt(tx_hash, timeout)
        return TransactionReceipt(
            transaction_hash=receipt["transactionHash"].hex(),
            transaction_index=receipt["transactionIndex"],
            block_hash=receipt["blockHash"].hex(),
            block_number=receipt["blockNumber"],
            from_address=receipt["from"],
            to=receipt.get("to"),
            gas_used=receipt["gasUsed"],
            cumulative_gas_used=receipt["cumulativeGasUsed"],
            effective_gas_price=receipt.get("effectiveGasPrice", 0),
            status=receipt["status"],
            contract_address=receipt.get("contractAddress"),
            logs=[],
        )

    # QFC-specific methods

    def get_validators(self) -> list[Validator]:
        """Get the list of active validators.

        Returns:
            List of validators
        """
        result = self._rpc_call("qfc_getValidators", [])
        return [
            Validator(
                address=v["address"],
                status=v["status"],
                total_stake=int(v["totalStake"], 16),
                self_stake=int(v["selfStake"], 16),
                delegated_stake=int(v["delegatedStake"], 16),
                commission_rate=v["commissionRate"],
                contribution_score=v["contributionScore"],
                blocks_produced=v["blocksProduced"],
                uptime=v["uptime"],
                jailed=v.get("jailed", False),
            )
            for v in result
        ]

    def get_validator(self, address: str) -> Validator | None:
        """Get a specific validator's information.

        Args:
            address: Validator address

        Returns:
            Validator information or None
        """
        result = self._rpc_call("qfc_getValidator", [address])
        if result is None:
            return None

        return Validator(
            address=result["address"],
            status=result["status"],
            total_stake=int(result["totalStake"], 16),
            self_stake=int(result["selfStake"], 16),
            delegated_stake=int(result["delegatedStake"], 16),
            commission_rate=result["commissionRate"],
            contribution_score=result["contributionScore"],
            blocks_produced=result["blocksProduced"],
            uptime=result["uptime"],
            jailed=result.get("jailed", False),
        )

    def get_contribution_score(self, address: str) -> ContributionScore:
        """Get the contribution score for an address.

        Args:
            address: Account address

        Returns:
            Contribution score breakdown
        """
        result = self._rpc_call("qfc_getContributionScore", [address])
        return ContributionScore(
            total=result["total"],
            staking=result["staking"],
            computation=result["computation"],
            uptime=result["uptime"],
            validation=result["validation"],
            network=result["network"],
            storage=result["storage"],
            reputation=result["reputation"],
        )

    def get_epoch(self) -> dict[str, Any]:
        """Get current epoch information.

        Returns:
            Epoch information
        """
        return self._rpc_call("qfc_getEpoch", [])

    def get_network_stats(self) -> dict[str, Any]:
        """Get network statistics.

        Returns:
            Network statistics including TPS, block time, etc.
        """
        return self._rpc_call("qfc_getNetworkStats", [])

    def _rpc_call(self, method: str, params: list[Any]) -> Any:
        """Make a raw JSON-RPC call.

        Args:
            method: RPC method name
            params: Method parameters

        Returns:
            RPC result
        """
        return self._web3.provider.make_request(method, params)["result"]
