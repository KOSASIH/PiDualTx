"""
pidualtx_scp — SCP-native ledger client for Pi Network.

Pi Network is a fork of `stellar-core` secured by the Stellar Consensus
Protocol (SCP). This package talks to Pi the way Pi actually works:

  * Horizon  — the classic HTTP API for accounts, ledgers, transactions.
  * Soroban RPC — JSON-RPC for smart-contract reads/writes and health.

It adds the thing the original PiDualTx never had: awareness that a
transaction is only *final* once SCP has closed the ledger containing it.
A submitted hash is not a settled payment.

Verified endpoints (probed live):
    Horizon mainnet  https://api.mainnet.minepi.com
    Horizon testnet  https://api.testnet.minepi.com
    Horizon testnet2 https://api.testnet2.minepi.com
    Soroban RPC      https://rpc.testnet.minepi.com
"""

from .network import Network, NetworkProfile, NETWORKS
from .transport import Transport, UrllibTransport
from .errors import RpcError, HorizonError, FinalityTimeout, LedgerRegression
from .rpc import SorobanRPC
from .horizon import HorizonClient
from .finality import (
    FinalityTracker,
    TxState,
    FinalityResult,
    LedgerClock,
    LedgerSample,
    to_epoch_seconds,
)
from .client import PiClient

__all__ = [
    "Network", "NetworkProfile", "NETWORKS",
    "Transport", "UrllibTransport",
    "RpcError", "HorizonError", "FinalityTimeout", "LedgerRegression",
    "SorobanRPC", "HorizonClient",
    "FinalityTracker", "TxState", "FinalityResult", "LedgerClock", "LedgerSample",
    "to_epoch_seconds",
    "PiClient",
]

__version__ = "2.0.0"
