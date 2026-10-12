"""One object that wires Horizon + RPC + finality together."""

from typing import Any, Dict, Optional

from .finality import FinalityTracker, LedgerClock
from .horizon import HorizonClient
from .network import Network, NetworkProfile
from .rpc import SorobanRPC
from .transport import Transport, UrllibTransport


class PiClient:
    def __init__(
        self,
        network: str = "testnet",
        *,
        horizon_url: Optional[str] = None,
        rpc_url: Optional[str] = None,
        transport: Optional[Transport] = None,
        timeout: int = 20,
    ):
        self.transport = transport or UrllibTransport()
        self.profile: NetworkProfile = Network.get(
            network, horizon_url=horizon_url, rpc_url=rpc_url
        )
        self.horizon = HorizonClient(self.profile.horizon_url, self.transport, timeout)
        self.rpc = (
            SorobanRPC(self.profile.rpc_url, self.transport, timeout)
            if self.profile.rpc_url
            else None
        )
        self.clock = LedgerClock()

    def health(self) -> Dict[str, Any]:
        out: Dict[str, Any] = {
            "network": self.profile.name,
            "passphrase": self.profile.passphrase,
            "horizon_url": self.profile.horizon_url,
            "horizon_reachable": self.horizon.reachable(),
        }
        if self.rpc is not None:
            out["rpc_url"] = self.rpc.url
            out["rpc_healthy"] = self.rpc.is_healthy()
        else:
            out["rpc_url"] = None
            out["rpc_healthy"] = None
            out["rpc_note"] = "no RPC endpoint configured for this network"
        return out

    def sync_ledger(self):
        """Sample the latest ledger and feed the clock (monotonicity enforced)."""
        led = self.horizon.latest_ledger()
        seq = int(led["sequence"])
        closed = led.get("closed_at")
        if closed is None:
            closed = led.get("close_time", 0)
        # Pass through verbatim: Horizon sends ISO-8601, RPC sends epoch
        # seconds. LedgerSample.close_time normalises either form.
        return self.clock.observe(seq, closed)

    def finality_tracker(self, poll_interval: float = 1.0, timeout: float = 30.0):
        """Poll via RPC when present, else fall back to Horizon."""
        if self.rpc is not None:
            return FinalityTracker(self.rpc.get_transaction,
                                   poll_interval=poll_interval, timeout=timeout)
        return FinalityTracker(self.horizon.transaction,
                               poll_interval=poll_interval, timeout=timeout)
