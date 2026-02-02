"""Account type definitions."""

from pydantic import BaseModel


class Account(BaseModel):
    """Account information."""

    address: str
    balance: int
    nonce: int
    is_contract: bool = False
    code: str | None = None
