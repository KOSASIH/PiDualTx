"""Typed errors. No bare `except:` swallowing anywhere in this package."""


class PiDualTxError(Exception):
    """Base class for all package errors."""


class RpcError(PiDualTxError):
    """A Soroban RPC call returned a JSON-RPC error or a bad envelope."""

    def __init__(self, code, message, data=None):
        self.code = code
        self.message = message
        self.data = data
        super().__init__(f"rpc error {code}: {message}")


class HorizonError(PiDualTxError):
    """Horizon returned a non-2xx status."""

    def __init__(self, status, title="", detail="", url=""):
        self.status = status
        self.title = title
        self.detail = detail
        self.url = url
        super().__init__(f"horizon {status} {title}: {detail} ({url})")


class FinalityTimeout(PiDualTxError):
    """A transaction did not reach a terminal state inside the deadline."""


class LedgerRegression(PiDualTxError):
    """
    The observed ledger sequence went backwards.

    On a healthy SCP network ledger sequence is monotonic. A regression means
    we are reading from an inconsistent or lagging node, and any finality
    conclusion drawn from it is unsafe.
    """
