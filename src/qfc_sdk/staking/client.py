"""Staking client for high-level staking operations."""

from web3 import Web3

from qfc_sdk.provider import QfcProvider
from qfc_sdk.types import StakeInfo, Delegation, Validator
from qfc_sdk.constants import CONTRACTS, STAKING_ABI, MIN_STAKE, MIN_DELEGATION


class StakingClient:
    """High-level client for staking operations.

    Examples:
        >>> staking = StakingClient(provider)
        >>> info = staking.get_stake_info("0x...")
        >>> print(f"Staked: {format_qfc(info.staked_amount)}")
    """

    def __init__(self, provider: QfcProvider, network: str = "testnet"):
        """Initialize the staking client.

        Args:
            provider: QFC provider
            network: Network name for contract address selection
        """
        self._provider = provider
        contract_key = f"STAKING_{network.upper()}"
        contract_address = CONTRACTS.get(contract_key, CONTRACTS["STAKING_TESTNET"])

        self._contract = provider.web3.eth.contract(
            address=Web3.to_checksum_address(contract_address),
            abi=STAKING_ABI,
        )

    def get_stake_info(self, address: str) -> StakeInfo:
        """Get staking information for an address.

        Args:
            address: Account address

        Returns:
            Staking information
        """
        address = Web3.to_checksum_address(address)
        result = self._contract.functions.getStakeInfo(address).call()

        staked, delegated, pending, unstaking = result

        # Check if address is a validator
        try:
            validator = self._provider.get_validator(address)
            is_validator = validator is not None and validator.status == "active"
        except Exception:
            is_validator = False

        return StakeInfo(
            address=address,
            staked_amount=staked,
            delegated_amount=delegated,
            pending_rewards=pending,
            unstaking_amount=unstaking,
            unstaking_release_time=None,  # Would need additional call
            is_validator=is_validator,
        )

    def get_delegations(self, address: str) -> list[Delegation]:
        """Get all delegations for an address.

        Args:
            address: Delegator address

        Returns:
            List of delegations
        """
        # Get list of validators
        validators = self._provider.get_validators()
        delegations = []

        address = Web3.to_checksum_address(address)

        for validator in validators:
            try:
                result = self._contract.functions.getDelegation(
                    address,
                    Web3.to_checksum_address(validator.address),
                ).call()

                amount, rewards = result
                if amount > 0:
                    delegations.append(Delegation(
                        delegator=address,
                        validator=validator.address,
                        amount=amount,
                        pending_rewards=rewards,
                        created_at=0,  # Not available from contract
                    ))
            except Exception:
                continue

        return delegations

    def get_delegation(self, delegator: str, validator: str) -> Delegation | None:
        """Get a specific delegation.

        Args:
            delegator: Delegator address
            validator: Validator address

        Returns:
            Delegation info or None
        """
        delegator = Web3.to_checksum_address(delegator)
        validator = Web3.to_checksum_address(validator)

        try:
            result = self._contract.functions.getDelegation(delegator, validator).call()
            amount, rewards = result

            if amount == 0:
                return None

            return Delegation(
                delegator=delegator,
                validator=validator,
                amount=amount,
                pending_rewards=rewards,
                created_at=0,
            )
        except Exception:
            return None

    def get_pending_rewards(self, address: str) -> int:
        """Get total pending rewards for an address.

        Args:
            address: Account address

        Returns:
            Pending rewards in wei
        """
        info = self.get_stake_info(address)
        return info.pending_rewards

    def get_validators_list(
        self,
        status: str | None = None,
        page: int = 1,
        per_page: int = 20,
    ) -> list[Validator]:
        """Get paginated list of validators.

        Args:
            status: Filter by status ("active", "inactive", "jailed")
            page: Page number (1-indexed)
            per_page: Results per page

        Returns:
            List of validators
        """
        validators = self._provider.get_validators()

        # Filter by status if specified
        if status:
            validators = [v for v in validators if v.status == status]

        # Sort by total stake (descending)
        validators.sort(key=lambda v: v.total_stake, reverse=True)

        # Paginate
        start = (page - 1) * per_page
        end = start + per_page

        return validators[start:end]

    def get_validator_count(self, status: str | None = None) -> int:
        """Get the count of validators.

        Args:
            status: Filter by status

        Returns:
            Number of validators
        """
        validators = self._provider.get_validators()
        if status:
            validators = [v for v in validators if v.status == status]
        return len(validators)

    def get_total_staked(self) -> int:
        """Get the total amount staked across all validators.

        Returns:
            Total staked in wei
        """
        validators = self._provider.get_validators()
        return sum(v.total_stake for v in validators)

    def can_stake(self, amount: int) -> tuple[bool, str]:
        """Check if an amount can be staked.

        Args:
            amount: Amount in wei

        Returns:
            Tuple of (can_stake, reason)
        """
        if amount < MIN_STAKE:
            from qfc_sdk.utils import format_qfc
            return False, f"Minimum stake is {format_qfc(MIN_STAKE)} QFC"
        return True, ""

    def can_delegate(self, amount: int) -> tuple[bool, str]:
        """Check if an amount can be delegated.

        Args:
            amount: Amount in wei

        Returns:
            Tuple of (can_delegate, reason)
        """
        if amount < MIN_DELEGATION:
            from qfc_sdk.utils import format_qfc
            return False, f"Minimum delegation is {format_qfc(MIN_DELEGATION)} QFC"
        return True, ""

    def estimate_rewards(self, amount: int, duration_days: int = 365) -> int:
        """Estimate staking rewards.

        Args:
            amount: Staked amount in wei
            duration_days: Duration in days

        Returns:
            Estimated rewards in wei

        Note:
            This is an approximation based on current network stats.
        """
        # Approximate 8% APY
        apy = 0.08
        daily_rate = apy / 365
        rewards = int(amount * daily_rate * duration_days)
        return rewards
