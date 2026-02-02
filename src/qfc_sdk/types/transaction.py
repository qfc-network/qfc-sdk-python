"""Transaction type definitions."""

from pydantic import BaseModel, Field


class TransactionRequest(BaseModel):
    """Transaction request for sending."""

    to: str | None = None
    value: int = 0
    data: str = "0x"
    gas: int | None = None
    gas_price: int | None = None
    max_fee_per_gas: int | None = None
    max_priority_fee_per_gas: int | None = None
    nonce: int | None = None


class Transaction(BaseModel):
    """Transaction information."""

    hash: str
    block_number: int | None = None
    block_hash: str | None = None
    from_address: str = Field(alias="from")
    to: str | None = None
    value: int
    gas: int
    gas_price: int | None = None
    max_fee_per_gas: int | None = None
    max_priority_fee_per_gas: int | None = None
    nonce: int
    data: str
    transaction_index: int | None = None

    class Config:
        """Pydantic config."""

        populate_by_name = True


class Log(BaseModel):
    """Transaction log entry."""

    address: str
    topics: list[str]
    data: str
    block_number: int
    transaction_hash: str
    transaction_index: int
    block_hash: str
    log_index: int
    removed: bool = False


class TransactionReceipt(BaseModel):
    """Transaction receipt."""

    transaction_hash: str
    transaction_index: int
    block_hash: str
    block_number: int
    from_address: str = Field(alias="from")
    to: str | None = None
    gas_used: int
    cumulative_gas_used: int
    effective_gas_price: int
    status: int
    logs: list[Log] = []
    contract_address: str | None = None

    class Config:
        """Pydantic config."""

        populate_by_name = True

    @property
    def success(self) -> bool:
        """Check if transaction was successful."""
        return self.status == 1
