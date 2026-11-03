"""Context race policy tests, not real concurrent service/database tests."""

from copy import deepcopy
import unittest

from core import CaptureCore, CaptureError
from proposal_gate import ProposalGate
from test_core import NOW, SOURCE, field, proposal


class ProposalGateTests(unittest.TestCase):
    def setUp(self):
        self.core = CaptureCore(lambda: NOW)
        self.gate = ProposalGate(self.core)
        self.capture = self.core.receive("alice", "u1", [{"source_id": "s1", "text": SOURCE}],
                                         NOW, "Asia/Riyadh")
        self.context = self.gate.context("alice", self.capture["id"])
        self.p = proposal(self.capture)

    def prepare(self):
        return self.gate.prepare("alice", self.context["context_id"], self.p)

    def clarify_and_append(self):
        p = deepcopy(self.p)
        p["disposition"] = "clarify"
        p["items"][0]["status"] = "needs_clarification"
        p["items"][0]["fields"].append(field("date", None, quote=None, confidence="missing"))
        p["questions"] = [{"item_id": "i1", "field": "date", "text": "أي يوم؟"}]
        self.core.submit("alice", self.capture["id"], p)
        self.core.add_clarification("alice", self.capture["id"], {"source_id": "s2", "text": "٥ نوفمبر"})

    def test_preparing_does_not_write_domain_records(self):
        self.prepare()
        self.assertEqual([], self.core.view("alice", "items"))
        self.assertEqual("received", self.core.capture("alice", self.capture["id"])["status"])

    def test_execute_retry_is_same_action_and_reversal_does_not_resurrect(self):
        ident = self.prepare()
        saved = self.gate.execute("alice", ident)
        self.assertEqual(saved, self.gate.execute("alice", ident))
        self.core.undo("alice", saved.action_id)
        self.assertEqual("reversed", self.gate.execute("alice", ident).status)
        self.assertEqual([], self.core.view("alice", "items"))

    def test_late_result_after_clarification_is_rejected_before_prepare(self):
        self.clarify_and_append()
        with self.assertRaisesRegex(CaptureError, "stale_context"):
            self.prepare()
        self.assertEqual([], self.core.view("alice", "actions"))

    def test_source_change_between_prepare_and_execute_is_rejected(self):
        ident = self.prepare()
        self.clarify_and_append()
        with self.assertRaisesRegex(CaptureError, "stale_context"):
            self.gate.execute("alice", ident)
        self.assertEqual([], self.core.view("alice", "items"))
        fresh = self.gate.context("alice", self.capture["id"])
        ident = self.gate.prepare("alice", fresh["context_id"], self.p)
        self.assertEqual("saved_in_memory", self.gate.execute("alice", ident).status)

    def test_proposal_and_context_return_values_are_defensive_copies(self):
        ident = self.prepare()
        self.p["items"][0]["fields"][0]["value"] = "تعديل متأخر"
        self.context["capture"]["sources"][0]["text"] = "مصدر معدّل"
        self.gate.execute("alice", ident)
        self.assertEqual("إرسال العرض", self.core.view("alice", "items")[0]["title"])

    def test_other_owner_cannot_get_prepare_or_execute_context(self):
        ident = self.prepare()
        calls = [lambda: self.gate.context("bob", self.capture["id"]),
                 lambda: self.gate.prepare("bob", self.context["context_id"], self.p),
                 lambda: self.gate.execute("bob", ident)]
        for call in calls:
            with self.subTest(call=call), self.assertRaisesRegex(CaptureError, "not_found"):
                call()
        self.assertEqual([], self.core.view("alice", "actions"))

    def test_wrong_capture_cannot_be_substituted(self):
        self.p["capture_id"] = "another-capture"
        with self.assertRaisesRegex(CaptureError, "capture_identity"):
            self.prepare()

    def test_prepare_is_not_validation_and_invalid_payload_cannot_execute(self):
        self.p["owner"] = "bob"
        ident = self.prepare()
        with self.assertRaisesRegex(CaptureError, "invalid_shape"):
            self.gate.execute("alice", ident)
        self.assertEqual([], self.core.view("alice", "actions"))


if __name__ == "__main__":
    unittest.main()
