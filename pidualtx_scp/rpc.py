"""Soroban JSON-RPC client for Pi Network."""

from typing import Any, Dict, List, Optional

from .errors import RpcError
from .transport import Transport, UrllibTransport


class SorobanRPC:
    """
    Minimal, correct JSON-RPC 2.0 client for a Soroban endpoint.

    Only the methods this project actually needs are implemented; unknown
    methods can be reached via `call()`.
    """

    def __init__(self, url: str, transport: Optional[Transport] = None, timeout: int = 20):
        if not url:
            raise ValueError("rpc url is required (Pi mainnet has no public RPC)")
        self.url = url
        self.transport = transport or UrllibTransport()
        self.timeout = timeout
        self._id = 0

    def call(self, method: str, params: Optional[Dict[str, Any]] = None) -> Any:
        self._id += 1
        payload = {
            "jsonrpc": "2.0",
            "id": self._id,
            "method": method,
            "params": params or {},
        }
        status, body = self.transport.post_json(self.url, payload, self.timeout)

        if not isinstance(body, dict):
            raise RpcError(-1, f"non-JSON response (http {status})", body)

        if "error" in body and body["error"] is not None:
            err = body["error"]
            raise RpcError(err.get("code", -1), err.get("message", "unknown"), err.get("data"))

        if "result" not in body:
            raise RpcError(-1, "malformed JSON-RPC envelope", body)

        return body["result"]

    def get_health(self) -> Dict[str, Any]:
        return self.call("getHealth")

    def get_latest_ledger(self) -> Dict[str, Any]:
        return self.call("getLatestLedger")

    def get_network(self) -> Dict[str, Any]:
        return self.call("getNetwork")

    def get_version_info(self) -> Dict[str, Any]:
        return self.call("getVersionInfo")

    def get_fee_stats(self) -> Dict[str, Any]:
        return self.call("getFeeStats")

    def get_transaction(self, tx_hash: str) -> Dict[str, Any]:
        return self.call("getTransaction", {"hash": tx_hash})

    def simulate_transaction(self, xdr: str) -> Dict[str, Any]:
        return self.call("simulateTransaction", {"transaction": xdr})

    def send_transaction(self, xdr: str) -> Dict[str, Any]:
        return self.call("sendTransaction", {"transaction": xdr})

    def get_events(self, start_ledger: int, filters: Optional[List[dict]] = None,
                   limit: int = 100) -> Dict[str, Any]:
        params: Dict[str, Any] = {"startLedger": start_ledger, "pagination": {"limit": limit}}
        if filters:
            params["filters"] = filters
        return self.call("getEvents", params)

    def is_healthy(self) -> bool:
        try:
            return self.get_health().get("status") == "healthy"
        except RpcError:
            return False

    def latest_ledger_sequence(self) -> int:
        led = self.get_latest_ledger()
        seq = led.get("sequence") or led.get("latestLedger")
        if seq is None:
            raise RpcError(-1, "getLatestLedger returned no sequence", led)
        return int(seq)
