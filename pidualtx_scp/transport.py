"""Injectable HTTP transport.

The client must be testable without a network, so every call goes through a
Transport. The default implementation uses only the standard library.
"""

import json
import urllib.error
import urllib.request
from typing import Any, Dict, Optional


class Transport:
    """Interface: POST or GET and return (status_code, parsed_json_or_text)."""

    def post_json(self, url: str, payload: Dict[str, Any], timeout: int = 20):
        raise NotImplementedError

    def get_json(self, url: str, timeout: int = 20):
        raise NotImplementedError


class UrllibTransport(Transport):
    def __init__(self, user_agent: str = "pidualtx-scp/2.0"):
        self.user_agent = user_agent
        self.call_count = 0

    def post_json(self, url, payload, timeout=20):
        self.call_count += 1
        body = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=body,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": self.user_agent,
            },
        )
        return self._send(req, timeout)

    def get_json(self, url, timeout=20):
        self.call_count += 1
        req = urllib.request.Request(
            url,
            headers={"Accept": "application/json", "User-Agent": self.user_agent},
        )
        return self._send(req, timeout)

    @staticmethod
    def _send(req, timeout):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                raw = resp.read().decode("utf-8", "replace")
                return resp.status, _maybe_json(raw)
        except urllib.error.HTTPError as exc:
            raw = exc.read().decode("utf-8", "replace")
            return exc.code, _maybe_json(raw)


def _maybe_json(raw: str):
    try:
        return json.loads(raw)
    except (ValueError, TypeError):
        return raw
