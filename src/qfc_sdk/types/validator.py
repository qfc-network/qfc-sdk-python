"""Validator and staking type definitions."""

from pydantic import BaseModel


class ContributionScore(BaseModel):
    """Contribution score breakdown."""

    total: int
    staking: int
    computation: int
    uptime: int
    validation: int
    network: int
    storage: int
    reputation: int


class Validator(BaseModel):
    """Validator information."""

    address: str
    status: str  # "active", "inactive", "jailed"
    total_stake: int
    self_stake: int
    delegated_stake: int
    commission_rate: int  # basis points (100 = 1%)
    contribution_score: int
    blocks_produced: int
    uptime: float
    jailed: bool = False
    jail_end_time: int | None = None


class StakeInfo(BaseModel):
    """Staking information for an address."""

    address: str
    staked_amount: int
    delegated_amount: int
    pending_rewards: int
    unstaking_amount: int
    unstaking_release_time: int | None = None
    is_validator: bool = False


class Delegation(BaseModel):
    """Delegation information."""

    delegator: str
    validator: str
    amount: int
    pending_rewards: int
    created_at: int


class UnstakeRequest(BaseModel):
    """Unstake request information."""

    amount: int
    release_time: int
    completed: bool = False
