"""Synthetic single-process context binding, NOT authentication or a transaction."""

from copy import deepcopy
from uuid import uuid4

from core import digest, require, text


class ProposalGate:
    """Bind a proposed action to the exact source context used to produce it.

    Trusted experiment callers may still use CaptureCore directly. A future
    service must make this policy mandatory inside the persistence transaction;
    these dictionaries provide no concurrent/crash-safe enforcement.
    """

    def __init__(self, core):
        self.core = core
        self._contexts, self._proposals = {}, {}

    @staticmethod
    def _fingerprint(capture):
        # Status changes from clarification/save/reversal are not source changes.
        return digest({k: capture[k] for k in
                       ("id", "owner", "sources", "received_at", "timezone", "resolvers")})

    def _owned(self, table, principal, ident):
        text(principal, 200)
        text(ident, 200)
        entry = table.get(ident)
        require(entry is not None and entry["owner"] == principal, "not_found")
        return entry

    def _current(self, principal, context):
        capture = self.core.capture(principal, context["capture_id"])
        require(self._fingerprint(capture) == context["fingerprint"], "stale_context")
        return capture

    def context(self, principal, capture_id):
        """Issue before proposing; includes synthetic sources, never an auth token."""
        capture = self.core.capture(principal, capture_id)
        ident = str(uuid4())
        self._contexts[ident] = {"owner": principal, "capture_id": capture_id,
                                 "fingerprint": self._fingerprint(capture)}
        return {"context_id": ident, "capture": capture}

    def prepare(self, principal, context_id, proposal):
        """Freeze an untrusted proposal without executing or asserting validity."""
        context = self._owned(self._contexts, principal, context_id)
        self._current(principal, context)
        require(isinstance(proposal, dict) and proposal.get("capture_id") == context["capture_id"],
                "capture_identity")
        ident = str(uuid4())
        self._proposals[ident] = {"owner": principal, "context_id": context_id,
                                  "proposal": deepcopy(proposal)}
        return ident

    def execute(self, principal, proposal_id):
        prepared = self._owned(self._proposals, principal, proposal_id)
        context = self._owned(self._contexts, principal, prepared["context_id"])
        self._current(principal, context)
        # Deterministic business validation remains in the core. Never run a
        # replacement client payload under an already prepared proposal ID.
        return self.core.submit(principal, context["capture_id"], deepcopy(prepared["proposal"]))
