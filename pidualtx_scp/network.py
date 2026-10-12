"""Network profiles for Pi Network.

Endpoint URLs below were verified by live probe. The network passphrase is the
value Pi's own integration guide passes to TransactionBuilder; it is used as
the seed for the master network key and as the hash salt for transaction
signing, so getting it wrong makes every signature invalid — silently.
"""

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass(frozen=True)
class NetworkProfile:
    name: str
    passphrase: str
    horizon_url: str
    rpc_url: Optional[str]
    protocol_floor: int
    """Minimum protocol version we expect; used to detect stale tooling."""

    explorer_url: Optional[str] = None
    notes: str = ""


NETWORKS: Dict[str, NetworkProfile] = {
    "mainnet": NetworkProfile(
        name="mainnet",
        passphrase="Pi Network",
        horizon_url="https://api.mainnet.minepi.com",
        rpc_url=None,  # not publicly confirmed; supply your own node
        protocol_floor=23,
        explorer_url="https://blockexplorer.minepi.com",
        notes=(
            "Soroban contracts live on Pi Mainnet since Protocol 23 (2026-05-11). "
            "Mainnet RPC is not a confirmed public endpoint — pass an explicit "
            "rpc_url if you run or rent a node."
        ),
    ),
    "testnet": NetworkProfile(
        name="testnet",
        passphrase="Pi Testnet",
        horizon_url="https://api.testnet.minepi.com",
        rpc_url="https://rpc.testnet.minepi.com",
        protocol_floor=23,
        notes="Public Soroban RPC confirmed healthy by live probe.",
    ),
    "testnet2": NetworkProfile(
        name="testnet2",
        passphrase="Pi Testnet",
        horizon_url="https://api.testnet2.minepi.com",
        rpc_url=None,
        protocol_floor=23,
        notes="Secondary testnet. RPC not publicly confirmed.",
    ),
}


class Network:
    """Resolve a profile by name, with optional endpoint overrides."""

    @staticmethod
    def get(
        name: str = "testnet",
        *,
        horizon_url: Optional[str] = None,
        rpc_url: Optional[str] = None,
    ) -> NetworkProfile:
        key = (name or "").strip().lower()
        if key not in NETWORKS:
            raise ValueError(
                f"unknown network {name!r}; expected one of {sorted(NETWORKS)}"
            )
        base = NETWORKS[key]
        if horizon_url is None and rpc_url is None:
            return base
        return NetworkProfile(
            name=base.name,
            passphrase=base.passphrase,
            horizon_url=horizon_url or base.horizon_url,
            rpc_url=rpc_url or base.rpc_url,
            protocol_floor=base.protocol_floor,
            explorer_url=base.explorer_url,
            notes=base.notes,
        )
