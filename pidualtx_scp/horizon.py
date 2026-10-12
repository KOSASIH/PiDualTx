"""Horizon client for Pi Network (classic accounts, ledgers, transactions)."""

from typing import Any, Dict, List, Optional

from .errors import HorizonError
from .transport import Transport, UrllibTransport


class HorizonClient:
    def __init__(self, base_url: str, transport: Optional[Transport] = None, timeout: int = 20):
        self.base_url = base_url.rstrip("/")
        self.transport = transport or UrllibTransport()
        self.timeout = timeout

    def _get(self, path: str) -> Any:
        url = f"{self.base_url}{path}"
        status, body = self.transport.get_json(url, self.timeout)
        if status is None or status >= 400:
            title = detail = ""
            if isinstance(body, dict):
                title = body.get("title", "")
                detail = body.get("detail", "")
            raise HorizonError(status, title, detail, url)
        return body

    def root(self) -> Dict[str, Any]:
        """Capabilities document. Doubles as a reachability probe."""
        return self._get("/")

    def latest_ledger(self) -> Dict[str, Any]:
        return self._get("/ledgers?order=desc&limit=1")["_embedded"]["records"][0]

    def ledger(self, sequence: int) -> Dict[str, Any]:
        return self._get(f"/ledgers/{sequence}")

    def fee_stats(self) -> Dict[str, Any]:
        return self._get("/fee_stats")

    def account(self, account_id: str) -> Dict[str, Any]:
        return self._get(f"/accounts/{account_id}")

    def transactions_for_account(self, account_id: str, limit: int = 20) -> List[Dict[str, Any]]:
        body = self._get(
            f"/accounts/{account_id}/transactions?order=desc&limit={int(limit)}"
        )
        return body.get("_embedded", {}).get("records", [])

    def transaction(self, tx_hash: str) -> Dict[str, Any]:
        return self._get(f"/transactions/{tx_hash}")

    def reachable(self) -> bool:
        try:
            self.root()
            return True
        except HorizonError:
            return False
