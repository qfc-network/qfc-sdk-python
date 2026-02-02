"""Block type definitions."""

from pydantic import BaseModel


class Block(BaseModel):
    """Block information."""

    number: int
    hash: str
    parent_hash: str
    timestamp: int
    producer: str
    gas_limit: int
    gas_used: int
    base_fee_per_gas: int | None = None
    transaction_count: int
    transactions: list[str] | None = None

    class Config:
        """Pydantic config."""

        populate_by_name = True
