"""Network type definitions."""

from enum import Enum
from pydantic import BaseModel


class Network(str, Enum):
    """Supported networks."""

    LOCALHOST = "localhost"
    TESTNET = "testnet"
    MAINNET = "mainnet"


class NetworkConfig(BaseModel):
    """Network configuration."""

    name: str
    chain_id: int
    rpc_url: str
    ws_url: str | None = None
    explorer_url: str | None = None
    faucet_url: str | None = None
    currency_symbol: str = "QFC"
    currency_decimals: int = 18
