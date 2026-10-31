"""Behavior tests of the local experiment; no service, credentials or model calls."""

from datetime import datetime
import unittest

from core import CaptureCore, CaptureError, local_instant


NOW = datetime.fromisoformat("2026-10-31T09:00:00+03:00")
SOURCE = "أحتاج أرسل العرض، وعندي موعد يوم ٥ نوفمبر ٢٠٢٦ الساعة ٤ مساءً، ذكرني."


def field(key, value, quote=SOURCE, confidence="source", resolver=None):
    return {"key": key, "value": value, "confidence": confidence,
            "evidence": [{"source_id": "s1", "quote": quote}] if quote else [], "resolver": resolver}


def item(kind="task", ident="i1", **values):
    return {"item_id": ident, "intent": kind, "status": "ready",
            "fields": [field(k, v) for k, v in {"title": "إرسال العرض", **values}.items()]}


def proposal(capture, *items):
    return {"schema_version": CaptureCore.VERSION, "capture_id": capture["id"], "disposition": "ready",
            "items": list(items or [item()]), "questions": [], "user_message": "اقتراح لم يُحفظ بعد."}


class CoreTests(unittest.TestCase):
    def setUp(self):
        self.core = CaptureCore(lambda: NOW)
        self.capture = self.receive("alice", "update-1")

    def receive(self, user, key, source=SOURCE, resolvers=None):
        return self.core.receive(user, key, [{"source_id": "s1", "text": source}], NOW, "Asia/Riyadh", resolvers)

    def save(self, *items, capture=None, user="alice"):
        capture = capture or self.capture
        p = proposal(capture, *items)
        return self.core.submit(user, capture["id"], p), p

    def assert_empty(self):
        for collection in ("items", "rules", "occurrences", "actions"):
            self.assertEqual([], self.core.view("alice", collection, include_history=True))

    def test_undated_task_does_not_invent_time_or_reminder(self):
        result, _ = self.save()
        saved = self.core.view("alice", "items")[0]
        self.assertEqual("saved_in_memory", result.status)
        self.assertIsNone(saved["date"])
        self.assertIsNone(saved["due_at"])
        self.assertEqual([], self.core.view("alice", "rules"))

    def test_date_only_task_has_no_fake_midnight(self):
        self.save(item(date="2026-11-05"))
        self.assertIsNone(self.core.view("alice", "items")[0]["due_at"])

    def test_timed_task_has_exact_utc_and_one_occurrence(self):
        result, p = self.save(item(date="2026-11-05", time="16:00", timezone="Asia/Riyadh", reminder_requested=True))
        self.assertEqual("2026-11-05T13:00:00+00:00", self.core.view("alice", "items")[0]["due_at"])
        for _ in range(5):
            self.assertEqual(result, self.core.submit("alice", self.capture["id"], p))
        self.assertEqual(1, len(self.core.view("alice", "rules")))
        self.assertEqual(1, len(self.core.view("alice", "occurrences")))

    def test_appointment_has_no_unrequested_reminder(self):
        self.save(item("appointment", date="2026-11-05", time="16:00", timezone="Asia/Riyadh"))
        self.assertEqual([], self.core.view("alice", "rules"))

    def test_all_day_appointment_has_date_not_invented_time(self):
        self.save(item("appointment", date="2026-11-05", all_day=True))
        saved = self.core.view("alice", "items")[0]
        self.assertTrue(saved["all_day"])
        self.assertIsNone(saved["due_at"])

    def test_standalone_reminder_requires_time_and_creates_one_rule(self):
        with self.assertRaisesRegex(CaptureError, "reminder_time_required"):
            self.save(item("reminder", date="2026-11-05"))
        self.assert_empty()
        self.save(item("reminder", date="2026-11-05", time="16:00", timezone="Asia/Riyadh"))
        self.assertEqual(1, len(self.core.view("alice", "occurrences")))

    def test_invalid_dates_times_and_conflicting_all_day_fail_atomically(self):
        for values in ({"date": "2026-02-30"}, {"date": "20261105"},
                       {"date": "2026-11-05", "time": "25:00", "timezone": "Asia/Riyadh"},
                       {"time": "16:00"}, {"all_day": True},
                       {"date": "2026-11-05", "time": "16:00", "all_day": True}):
            with self.subTest(values=values), self.assertRaises(CaptureError):
                self.save(item(**values))
            self.assert_empty()

    def test_past_time_is_not_silently_rescheduled(self):
        with self.assertRaisesRegex(CaptureError, "past_time"):
            self.save(item(date="2026-10-31", time="08:00", timezone="Asia/Riyadh"))
        self.assert_empty()
        self.assertEqual("received", self.core.capture("alice", self.capture["id"])["status"])

    def test_timezone_mismatch_is_not_silently_accepted(self):
        with self.assertRaisesRegex(CaptureError, "timezone_mismatch"):
            self.save(item(date="2026-11-05", time="16:00", timezone="UTC"))
        self.assert_empty()

    def test_dst_gap_and_fold_require_resolution(self):
        for day, clock in [("2026-03-08", "02:30"), ("2026-11-01", "01:30")]:
            with self.subTest(day=day), self.assertRaisesRegex(CaptureError, "ambiguous_or_nonexistent_time"):
                local_instant(day, clock, "America/New_York")

    def test_ingest_retry_same_key_returns_same_capture(self):
        retry = self.receive("alice", "update-1")
        self.assertEqual(self.capture["id"], retry["id"])
        with self.assertRaisesRegex(CaptureError, "idempotency_conflict"):
            self.receive("alice", "update-1", source="محتوى مختلف")

    def test_same_ingest_key_is_scoped_to_owner(self):
        bob = self.receive("bob", "update-1")
        self.assertNotEqual(self.capture["id"], bob["id"])
        self.save(capture=bob, user="bob")
        self.assertEqual([], self.core.view("alice", "items"))

    def test_cross_owner_reads_submit_source_and_undo_are_rejected(self):
        result, p = self.save()
        for fn in (lambda: self.core.capture("bob", self.capture["id"]),
                   lambda: self.core.submit("bob", self.capture["id"], p),
                   lambda: self.core.source_for_item("bob", result.item_ids[0]),
                   lambda: self.core.undo("bob", result.action_id)):
            with self.subTest(fn=fn), self.assertRaisesRegex(CaptureError, "not_found"):
                fn()
        self.assertEqual([], self.core.view("bob", "actions"))

    def test_source_and_projection_copies_do_not_mutate_internal_state(self):
        result, _ = self.save()
        source = self.core.source_for_item("alice", result.item_ids[0])
        source["sources"][0]["text"] = "changed"
        self.core.view("alice", "items")[0]["title"] = "changed"
        self.assertEqual(SOURCE, self.core.source_for_item("alice", result.item_ids[0])["sources"][0]["text"])
        self.assertEqual("إرسال العرض", self.core.view("alice", "items")[0]["title"])

    def test_forged_capture_version_owner_field_or_quote_rejected(self):
        mutations = [lambda p: p.update(schema_version="wrong"), lambda p: p.update(owner="bob"),
                     lambda p: p.update(capture_id="forged"),
                     lambda p: p["items"][0]["fields"][0]["evidence"][0].update(quote="not in source")]
        for mutate in mutations:
            p = proposal(self.capture)
            mutate(p)
            with self.subTest(mutate=mutate), self.assertRaises(CaptureError):
                self.core.submit("alice", self.capture["id"], p)
            self.assert_empty()

    def test_derived_values_must_match_trusted_context(self):
        capture = self.receive("alice", "derived", resolvers={"today": "2026-10-31"})
        p = proposal(capture)
        f = field("date", "2026-11-01", quote=None, confidence="derived", resolver="today")
        p["items"][0]["fields"].append(f)
        with self.assertRaisesRegex(CaptureError, "untrusted_derivation"):
            self.core.submit("alice", capture["id"], p)
        f["value"] = "2026-10-31"
        self.assertEqual("saved_in_memory", self.core.submit("alice", capture["id"], p).status)

    def test_duplicate_item_or_field_ids_rejected(self):
        duplicate_items = proposal(self.capture, item(), item())
        duplicate_fields = proposal(self.capture)
        duplicate_fields["items"][0]["fields"] *= 2
        for p in (duplicate_items, duplicate_fields):
            with self.assertRaises(CaptureError):
                self.core.submit("alice", self.capture["id"], p)
            self.assert_empty()

    def test_invalid_second_item_leaves_no_partial_writes(self):
        with self.assertRaises(CaptureError):
            self.save(item(), item("appointment", ident="i2", date="2026-11-05"))
        self.assert_empty()
        self.assertEqual(SOURCE, self.core.capture("alice", self.capture["id"])["sources"][0]["text"])

    def test_clarification_retains_source_then_resolves_as_same_capture(self):
        p = proposal(self.capture, item("appointment", date="2026-11-05"))
        p["disposition"] = "clarify"
        p["items"][0]["status"] = "needs_clarification"
        p["items"][0]["fields"].append(field("time", None, quote=None, confidence="missing"))
        p["questions"] = [{"item_id": "i1", "field": "time", "text": "الساعة كم؟"}]
        self.assertEqual("clarify", self.core.submit("alice", self.capture["id"], p).status)
        self.assert_empty()
        source = {"source_id": "answer-1", "text": "٤ مساءً بتوقيت الرياض"}
        self.core.add_clarification("alice", self.capture["id"], source)
        self.core.add_clarification("alice", self.capture["id"], source)
        ready = proposal(self.capture, item("appointment", date="2026-11-05", time="16:00", timezone="Asia/Riyadh"))
        for f in ready["items"][0]["fields"]:
            if f["key"] in ("time", "timezone"):
                f["evidence"] = [{"source_id": "answer-1", "quote": source["text"]}]
        result = self.core.submit("alice", self.capture["id"], ready)
        self.assertEqual("saved_in_memory", result.status)
        self.assertEqual(2, len(self.core.source_for_item("alice", result.item_ids[0])["sources"]))

    def test_clarification_cannot_overwrite_original(self):
        p = proposal(self.capture)
        p["disposition"] = "clarify"
        p["items"][0]["status"] = "needs_clarification"
        p["items"][0]["fields"].append(field("time", None, quote=None, confidence="missing"))
        p["questions"] = [{"item_id": "i1", "field": "time", "text": "أي وقت؟"}]
        self.core.submit("alice", self.capture["id"], p)
        with self.assertRaisesRegex(CaptureError, "source_identity_conflict"):
            self.core.add_clarification("alice", self.capture["id"], {"source_id": "s1", "text": "overwrite"})

    def test_unsupported_invoice_defers_whole_group_without_fake_asset(self):
        result, _ = self.save(item(), item("invoice", ident="i2"))
        self.assertEqual("deferred", result.status)
        self.assert_empty()
        self.assertEqual("deferred", self.core.capture("alice", self.capture["id"])["status"])

    def test_uncertain_or_malformed_proposals_fail_without_writes(self):
        for mutate in (lambda p: p["items"][0]["fields"][0].update(confidence="uncertain"),
                       lambda p: p.update(disposition=[]),
                       lambda p: p["items"][0].update(intent=[]),
                       lambda p: p["items"][0]["fields"][0].update(key=[])):
            p = proposal(self.capture)
            mutate(p)
            with self.assertRaises(CaptureError):
                self.core.submit("alice", self.capture["id"], p)
            self.assert_empty()

    def test_undo_specific_action_does_not_touch_later_capture(self):
        first, p = self.save(item(date="2026-11-05", time="16:00", timezone="Asia/Riyadh", reminder_requested=True))
        second, _ = self.save(capture=self.receive("alice", "update-2"))
        reversal = self.core.undo("alice", first.action_id)
        self.assertEqual(reversal, self.core.undo("alice", first.action_id))
        self.assertEqual([second.item_ids[0]], [i["id"] for i in self.core.view("alice", "items")])
        self.assertEqual([], self.core.view("alice", "occurrences"))
        self.assertEqual("cancelled", self.core.view("alice", "occurrences", include_history=True)[0]["status"])
        self.assertEqual(SOURCE, self.core.capture("alice", self.capture["id"])["sources"][0]["text"])
        self.assertEqual("reversed", self.core.submit("alice", self.capture["id"], p).status)
        self.assertEqual(3, len(self.core.view("alice", "actions")))

    def test_changed_committed_proposal_does_not_create_another_action(self):
        _, p = self.save()
        p["items"][0]["fields"][0]["value"] = "عنوان مختلف"
        with self.assertRaisesRegex(CaptureError, "committed_proposal_conflict"):
            self.core.submit("alice", self.capture["id"], p)
        self.assertEqual(1, len(self.core.view("alice", "items")))

    def test_bad_undo_clock_does_not_partially_reverse(self):
        result, _ = self.save()
        self.core.clock = lambda: datetime(2026, 10, 31)
        with self.assertRaisesRegex(CaptureError, "aware_clock_required"):
            self.core.undo("alice", result.action_id)
        self.assertEqual(1, len(self.core.view("alice", "items")))
        self.assertEqual("executed", self.core.view("alice", "actions")[0]["status"])

    def test_fresh_process_store_has_no_persistence(self):
        self.save()
        other = CaptureCore(lambda: NOW)
        self.assertEqual([], other.view("alice", "items"))
        with self.assertRaisesRegex(CaptureError, "not_found"):
            other.capture("alice", self.capture["id"])

    def test_source_limits_and_invalid_context_are_rejected(self):
        for source, resolvers in [("x" * 20001, None), (SOURCE, []), (SOURCE, {"resolver": []})]:
            with self.subTest(resolvers=resolvers), self.assertRaises(CaptureError):
                self.receive("alice", "invalid-context", source=source, resolvers=resolvers)
        with self.assertRaisesRegex(CaptureError, "duplicate_source_id"):
            self.core.receive("alice", "duplicate-source", [{"source_id": "s1", "text": "a"},
                              {"source_id": "s1", "text": "b"}], NOW, "Asia/Riyadh")

    def test_clarification_questions_must_target_unresolved_fields(self):
        p = proposal(self.capture)
        p["disposition"] = "clarify"
        p["items"][0]["status"] = "needs_clarification"
        p["questions"] = [{"item_id": "i1", "field": "title", "text": "كرر العنوان؟"}]
        with self.assertRaisesRegex(CaptureError, "invalid_clarification_target"):
            self.core.submit("alice", self.capture["id"], p)
        self.assert_empty()

    def test_duplicate_record_proposals_with_different_item_ids_are_rejected(self):
        with self.assertRaisesRegex(CaptureError, "duplicate_proposed_item"):
            self.save(item(ident="i1"), item(ident="i2"))
        self.assert_empty()

    def test_valid_multi_item_group_saves_and_reverses_together(self):
        result, _ = self.save(item(), item("appointment", ident="i2", title="موعد",
                                          date="2026-11-05", time="16:00", timezone="Asia/Riyadh",
                                          reminder_requested=True))
        self.assertEqual(2, len(result.item_ids))
        self.assertEqual(1, len(result.rule_ids))
        self.assertEqual(2, len(self.core.view("alice", "items")))
        self.core.undo("alice", result.action_id)
        self.assertEqual([], self.core.view("alice", "items"))
        self.assertEqual([], self.core.view("alice", "occurrences"))


if __name__ == "__main__":
    unittest.main()
