"""
Finality tracking - the part the original PiDualTx never had.

On SCP no single node declares a payment valid. Validators agree on a ledger
close; once the ledger holding your transaction is closed and the network has
moved past it, the outcome is settled. A submitted hash is *pending*.

This module models exactly that:

    SUBMITTED -> PENDING -> (SUCCESS | FAILED | NOT_FOUND-at-deadline)

and separately tracks ledger closes so callers can reason about how much
confirmation depth a result actually carries.
"""

import calendar
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Callable, List, Optional

from .errors import FinalityTimeout, LedgerRegression


class TxState(str, Enum):
    SUBMITTED = "SUBMITTED"
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"

    @property
    def terminal(self) -> bool:
        return self in (TxState.SUCCESS, TxState.FAILED)


def to_epoch_seconds(value) -> float:
    """
    Normalise a ledger close time to epoch seconds.

    Pi's Horizon returns an ISO-8601 string (e.g. '2026-10-12T12:01:05Z')
    while Soroban RPC returns epoch seconds. Both appear in the wild, so both
    are accepted here.

    Anything unparseable raises ValueError rather than silently returning 0 -
    a wrong close time would corrupt every drift calculation downstream, and
    a silent zero is exactly the kind of bug that hides until it matters.
    """
    if isinstance(value, bool):
        raise ValueError("boolean is not a valid close time")

    if isinstance(value, (int, float)):
        return float(value)

    if not isinstance(value, str):
        raise ValueError("unsupported close-time type: " + type(value).__name__)

    text = value.strip()
    if not text:
        raise ValueError("empty close-time string")

    try:
        return float(text)
    except ValueError:
        pass

    iso = text[:-1] + "+00:00" if text.endswith("Z") else text
    try:
        dt = datetime.fromisoformat(iso)
    except ValueError as exc:
        raise ValueError("unparseable close time: " + repr(text)) from exc

    if dt.tzinfo is None:
        return float(calendar.timegm(dt.timetuple()))
    return dt.timestamp()


@dataclass
class FinalityResult:
    state: TxState
    tx_hash: str
    ledger: Optional[int] = None
    attempts: int = 0
    elapsed_seconds: float = 0.0
    raw: Optional[dict] = None

    @property
    def confirmed(self) -> bool:
        return self.state is TxState.SUCCESS


@dataclass
class LedgerSample:
    sequence: int
    closed_at: object
    """Ledger close time. Horizon sends ISO-8601; RPC sends epoch seconds."""

    observed_at: float = field(default_factory=time.time)

    @property
    def close_time(self) -> float:
        """Close time as epoch seconds, whatever form the node used."""
        return to_epoch_seconds(self.closed_at)


class FinalityTracker:
    """
    Polls a source (Soroban RPC `getTransaction`, or Horizon) until a
    transaction reaches a terminal state or the deadline expires.

    `fetch` must return a dict shaped like a Soroban getTransaction result:
        {"status": "SUCCESS"|"FAILED"|"NOT_FOUND", "ledger": 123, ...}

    The clock and sleep function are injectable so the state machine can be
    tested deterministically without waiting on wall time.
    """

    def __init__(
        self,
        fetch: Callable[[str], dict],
        poll_interval: float = 1.0,
        timeout: float = 30.0,
        sleep: Callable[[float], None] = time.sleep,
        now: Callable[[], float] = time.time,
    ):
        self.fetch = fetch
        self.poll_interval = poll_interval
        self.timeout = timeout
        self._sleep = sleep
        self._now = now

    def await_finality(self, tx_hash: str) -> FinalityResult:
        start = self._now()
        attempts = 0
        last = None

        while True:
            elapsed = self._now() - start
            if elapsed > self.timeout:
                raise FinalityTimeout(
                    tx_hash + " not final after " + str(self.timeout) + "s ("
                    + str(attempts) + " attempts, last="
                    + str(last.get("status") if last else None) + ")"
                )

            attempts += 1
            last = self.fetch(tx_hash) or {}
            status = str(last.get("status", "NOT_FOUND")).upper()

            if status == "SUCCESS":
                return FinalityResult(TxState.SUCCESS, tx_hash,
                                      ledger=last.get("ledger"),
                                      attempts=attempts,
                                      elapsed_seconds=self._now() - start,
                                      raw=last)
            if status == "FAILED":
                return FinalityResult(TxState.FAILED, tx_hash,
                                      ledger=last.get("ledger"),
                                      attempts=attempts,
                                      elapsed_seconds=self._now() - start,
                                      raw=last)

            # NOT_FOUND / PENDING / anything unrecognised: the ledger holding
            # this transaction may not have closed yet. Keep waiting rather
            # than guessing at an outcome.
            self._sleep(self.poll_interval)


class LedgerClock:
    """
    Tracks ledger closes and enforces the invariant that matters: sequence
    numbers move forward.

    SCP targets ~5s closes on Stellar-lineage chains, so a persistent drift
    away from that is worth surfacing to the caller.
    """

    def __init__(self, expected_close_seconds: float = 5.0, max_samples: int = 64):
        self.expected_close_seconds = expected_close_seconds
        self.max_samples = max_samples
        self._samples: List[LedgerSample] = []

    def observe(self, sequence: int, closed_at) -> LedgerSample:
        if self._samples:
            last = self._samples[-1]
            if sequence < last.sequence:
                raise LedgerRegression(
                    "ledger went backwards: saw " + str(sequence) + " after "
                    + str(last.sequence) + "; node is inconsistent - do not "
                    "trust finality conclusions drawn from it"
                )
        sample = LedgerSample(sequence=sequence, closed_at=closed_at)
        self._samples.append(sample)
        if len(self._samples) > self.max_samples:
            self._samples = self._samples[-self.max_samples:]
        return sample

    @property
    def samples(self) -> List[LedgerSample]:
        return list(self._samples)

    def latest(self) -> Optional[LedgerSample]:
        return self._samples[-1] if self._samples else None

    def intervals(self) -> List[float]:
        out = []
        for a, b in zip(self._samples, self._samples[1:]):
            delta = b.close_time - a.close_time
            if delta > 0:
                out.append(delta)
        return out

    def mean_close_seconds(self) -> Optional[float]:
        iv = self.intervals()
        if not iv:
            return None
        return sum(iv) / len(iv)

    def drift_ratio(self) -> Optional[float]:
        """Mean close interval divided by expectation. 1.0 is nominal."""
        mean = self.mean_close_seconds()
        if mean is None or self.expected_close_seconds <= 0:
            return None
        return mean / self.expected_close_seconds

    def confirmation_depth(self, tx_ledger: int) -> int:
        """How many ledgers have closed since the transaction's ledger."""
        latest = self.latest()
        if latest is None:
            return 0
        return max(0, latest.sequence - int(tx_ledger))
