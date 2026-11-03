"""Single-process, synthetic-data capture/action experiment; no service or durable storage."""

from copy import deepcopy
from dataclasses import dataclass
from datetime import date, datetime, time, timezone
from hashlib import sha256
import json
import re
from uuid import uuid4
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


class CaptureError(ValueError):
    """Stable, content-free error codes suitable for assertions (not user copy)."""


def require(condition, code):
    if not condition:
        raise CaptureError(code)


def exact_keys(value, expected):
    require(isinstance(value, dict) and set(value) == set(expected), "invalid_shape")


def text(value, limit=20000):
    require(isinstance(value, str) and bool(value.strip()) and len(value) <= limit, "invalid_text")
    return value


def digest(value):
    return sha256(json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False).encode()).hexdigest()


def zone(value):
    text(value, 100)
    try:
        return ZoneInfo(value)
    except (ValueError, ZoneInfoNotFoundError) as exc:
        raise CaptureError("invalid_timezone") from exc


def instant(value):
    require(isinstance(value, datetime) and value.tzinfo is not None and value.utcoffset() is not None,
            "aware_clock_required")
    return value.astimezone(timezone.utc)


def local_instant(day, clock, zone_name):
    """Reject impossible/ambiguous DST wall times instead of guessing a fold."""
    require(isinstance(day, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", day), "invalid_date")
    require(isinstance(clock, str) and re.fullmatch(r"(?:[01]\d|2[0-3]):[0-5]\d", clock), "invalid_time")
    try:
        naive = datetime.combine(date.fromisoformat(day), time.fromisoformat(clock))
    except ValueError as exc:
        raise CaptureError("invalid_date") from exc
    tz = zone(zone_name)
    candidates = set()
    for fold in (0, 1):
        utc = naive.replace(tzinfo=tz, fold=fold).astimezone(timezone.utc)
        if utc.astimezone(tz).replace(tzinfo=None) == naive:
            candidates.add(utc)
    require(len(candidates) == 1, "ambiguous_or_nonexistent_time")
    return candidates.pop().isoformat()


@dataclass(frozen=True)
class Result:
    status: str
    action_id: str | None = None
    item_ids: tuple = ()
    rule_ids: tuple = ()
    questions: tuple = ()
    duplicate_capture_id: str | None = None


class CaptureCore:
    """Caller supplies a trusted principal/clock/resolver context, NOT model identity.

    This is an in-memory policy experiment, not authentication, a production
    validator, a database transaction or a concurrent execution boundary.
    """

    VERSION = "madar.capture-understanding/2.2"
    INTENTS = {"task", "appointment", "reminder", "invoice", "document", "subscription",
               "maintenance", "odometer", "note", "retrieval", "correction", "unsupported", "restricted"}
    FIELDS = {"title", "date", "time", "timezone", "all_day", "original_time_phrase", "reminder_requested"}

    def __init__(self, clock):
        self.clock = clock
        self._captures, self._ingest_keys, self._commits = {}, {}, {}
        self._items, self._rules, self._occurrences, self._actions = {}, {}, {}, {}

    def _owned(self, table, principal, ident):
        text(principal, 200)
        text(ident, 200)
        value = table.get(ident)
        require(value is not None and value["owner"] == principal, "not_found")
        return value

    def receive(self, principal, key, sources, received_at, user_timezone, resolvers=None):
        """Accept synthetic normalized text sources; raw file ingestion is not implemented."""
        text(principal, 200)
        text(key, 200)
        instant(received_at)
        zone(user_timezone)
        require(isinstance(sources, list) and 1 <= len(sources) <= 10, "invalid_sources")
        source_ids = set()
        for source in sources:
            exact_keys(source, ("source_id", "text"))
            text(source["source_id"], 200)
            text(source["text"])
            require(source["source_id"] not in source_ids, "duplicate_source_id")
            source_ids.add(source["source_id"])
        require(sum(len(s["text"]) for s in sources) <= 100000, "source_limit")
        resolvers = {} if resolvers is None else deepcopy(resolvers)
        require(isinstance(resolvers, dict), "invalid_resolvers")
        for ident, value in resolvers.items():
            text(ident, 200)
            require(type(value) in (str, int, bool), "invalid_resolver_value")
        envelope = {"sources": sources, "received_at": received_at.isoformat(),
                    "timezone": user_timezone, "resolvers": resolvers}
        fingerprint = digest(envelope)
        previous = self._ingest_keys.get((principal, key))
        if previous:
            require(previous[0] == fingerprint, "idempotency_conflict")
            return deepcopy(self._captures[previous[1]])
        ident = str(uuid4())
        capture = {"id": ident, "owner": principal, "sources": deepcopy(sources),
                   "received_at": received_at.isoformat(), "timezone": user_timezone,
                   "resolvers": resolvers, "status": "received"}
        self._captures[ident] = capture
        self._ingest_keys[(principal, key)] = (fingerprint, ident)
        return deepcopy(capture)

    def add_clarification(self, principal, capture_id, source):
        capture = self._owned(self._captures, principal, capture_id)
        require(capture["status"] == "awaiting_confirmation", "capture_not_awaiting")
        exact_keys(source, ("source_id", "text"))
        text(source["source_id"], 200)
        text(source["text"])
        old = next((s for s in capture["sources"] if s["source_id"] == source["source_id"]), None)
        if old:
            require(old == source, "source_identity_conflict")
            return
        require(len(capture["sources"]) < 10 and
                sum(len(s["text"]) for s in capture["sources"]) + len(source["text"]) <= 100000,
                "source_limit")
        capture["sources"].append(deepcopy(source))

    def _envelope(self, capture, proposal):
        exact_keys(proposal, ("schema_version", "capture_id", "disposition", "items", "questions", "user_message"))
        require(proposal["schema_version"] == self.VERSION, "schema_version")
        require(proposal["capture_id"] == capture["id"], "capture_identity")
        require(isinstance(proposal["disposition"], str) and proposal["disposition"] in {"ready", "clarify", "retrieve", "keep_source", "unsupported", "restricted"},
                "disposition")
        text(proposal["user_message"], 600)
        require(isinstance(proposal["items"], list) and 1 <= len(proposal["items"]) <= 20, "item_limit")
        require(isinstance(proposal["questions"], list) and len(proposal["questions"]) <= 20, "question_limit")
        ids = set()
        for item in proposal["items"]:
            exact_keys(item, ("item_id", "intent", "status", "fields"))
            text(item["item_id"], 200)
            text(item["intent"], 100)
            text(item["status"], 100)
            require(item["item_id"] not in ids, "duplicate_item_id")
            ids.add(item["item_id"])
            require(item["intent"] in self.INTENTS, "unknown_intent")
            require(item["status"] in {"ready", "needs_clarification", "source_only", "blocked"}, "item_status")
            require(isinstance(item["fields"], list) and len(item["fields"]) <= 30, "field_limit")
        # Unsupported domain families are deferred as a whole; no partial execution.
        if any(item["intent"] not in {"task", "appointment", "reminder"} for item in proposal["items"]):
            return None
        fields_by_id = {}
        sources = {s["source_id"]: s["text"] for s in capture["sources"]}
        for item in proposal["items"]:
            fields = {}
            for field in item["fields"]:
                exact_keys(field, ("key", "value", "confidence", "evidence", "resolver"))
                key = field["key"]
                text(key, 100)
                text(field["confidence"], 100)
                require(key in self.FIELDS and key not in fields, "unsupported_or_duplicate_field")
                require(field["confidence"] in {"source", "derived", "uncertain", "missing"}, "confidence")
                require(isinstance(field["evidence"], list) and len(field["evidence"]) <= 10, "evidence_limit")
                if field["confidence"] == "missing":
                    require(field["value"] is None and not field["evidence"] and field["resolver"] is None,
                            "missing_field_value")
                else:
                    if key in {"all_day", "reminder_requested"}:
                        require(type(field["value"]) is bool, "boolean_field")
                    else:
                        text(field["value"], 600)
                    if field["confidence"] == "derived":
                        text(field["resolver"], 200)
                        require(field["resolver"] in capture["resolvers"] and
                                type(field["value"]) is type(capture["resolvers"][field["resolver"]]) and
                                field["value"] == capture["resolvers"][field["resolver"]], "untrusted_derivation")
                    else:
                        require(bool(field["evidence"]) and field["resolver"] is None, "missing_evidence")
                for evidence in field["evidence"]:
                    exact_keys(evidence, ("source_id", "quote"))
                    text(evidence["quote"])
                    text(evidence["source_id"], 200)
                    require(evidence["source_id"] in sources and
                            evidence["quote"] in sources[evidence["source_id"]], "invalid_evidence")
                fields[key] = field
            fields_by_id[item["item_id"]] = fields
        return fields_by_id

    def submit(self, principal, capture_id, proposal):
        capture = self._owned(self._captures, principal, capture_id)
        fields_by_id = self._envelope(capture, proposal)
        if capture_id in self._commits:
            fingerprint, result = self._commits[capture_id]
            require(fingerprint == digest(proposal), "committed_proposal_conflict")
            if self._actions[result.action_id]["status"] == "reversed":
                return Result("reversed", result.action_id, result.item_ids, result.rule_ids)
            return result
        if fields_by_id is None or proposal["disposition"] not in {"ready", "clarify"}:
            capture["status"] = "deferred"
            return Result("deferred")
        if proposal["disposition"] == "clarify":
            require(bool(proposal["questions"]), "clarification_question_required")
            pending = {i["item_id"] for i in proposal["items"] if i["status"] == "needs_clarification"}
            require(bool(pending), "clarification_item_required")
            answered = set()
            for question in proposal["questions"]:
                exact_keys(question, ("item_id", "field", "text"))
                text(question["text"], 600)
                text(question["item_id"], 200)
                text(question["field"], 100)
                field = fields_by_id.get(question["item_id"], {}).get(question["field"])
                require(question["item_id"] in pending and field is not None and
                        field["confidence"] in {"missing", "uncertain"}, "invalid_clarification_target")
                answered.add(question["item_id"])
            require(answered == pending, "unasked_clarification")
            capture["status"] = "awaiting_confirmation"
            return Result("clarify", questions=tuple(deepcopy(proposal["questions"])))
        require(not proposal["questions"], "ready_with_questions")
        now = instant(self.clock())
        planned = []
        proposed_records = set()
        # Validate the complete group before mutating any domain projection.
        for item in proposal["items"]:
            require(item["status"] == "ready", "item_not_ready")
            fields = fields_by_id[item["item_id"]]
            require(all(f["confidence"] in {"source", "derived"} for f in fields.values()), "uncertain_ready_item")
            values = {k: f["value"] for k, f in fields.items()}
            title = text(values.get("title"), 200)
            if "timezone" in values:
                require(values["timezone"] == capture["timezone"], "timezone_mismatch")
            day, clock = values.get("date"), values.get("time")
            all_day = values.get("all_day", False)
            require(not (all_day and clock), "all_day_with_time")
            require(not (clock and not day), "time_without_date")
            if day:
                require(bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", day)), "invalid_date")
                try:
                    parsed_day = date.fromisoformat(day)
                except ValueError as exc:
                    raise CaptureError("invalid_date") from exc
                require(parsed_day >= now.astimezone(zone(capture["timezone"])).date(), "past_date")
            require(not all_day or day is not None, "all_day_without_date")
            if item["intent"] == "appointment":
                require(day and (clock or all_day), "appointment_time_required")
            wants_reminder = values.get("reminder_requested", False) or item["intent"] == "reminder"
            require(not wants_reminder or (day and clock), "reminder_time_required")
            due_at = None
            if clock:
                require(values.get("timezone") == capture["timezone"], "timezone_mismatch")
                due_at = local_instant(day, clock, values["timezone"])
                require(datetime.fromisoformat(due_at) > now, "past_time")
            identity = (title, day, due_at)
            require(identity not in proposed_records, "duplicate_proposed_item")
            proposed_records.add(identity)
            planned.append({"kind": item["intent"], "title": title, "date": day,
                            "due_at": due_at, "all_day": all_day, "timezone": capture["timezone"],
                            "original_time_phrase": values.get("original_time_phrase"),
                            "wants_reminder": wants_reminder})
        action_id = str(uuid4())
        items, rules, occurrences = {}, {}, {}
        for plan in planned:
            item_id = str(uuid4())
            reminder = plan.pop("wants_reminder")
            items[item_id] = {"id": item_id, "owner": principal, "capture_id": capture_id,
                              "action_id": action_id, "status": "active", **plan}
            if reminder:
                rule_id, occurrence_id = str(uuid4()), str(uuid4())
                rules[rule_id] = {"id": rule_id, "owner": principal, "item_id": item_id,
                                  "action_id": action_id, "status": "active", "due_at": plan["due_at"]}
                occurrences[occurrence_id] = {"id": occurrence_id, "owner": principal, "rule_id": rule_id,
                                             "status": "active", "due_at": plan["due_at"]}
        self._items.update(items)
        self._rules.update(rules)
        self._occurrences.update(occurrences)
        self._actions[action_id] = {"id": action_id, "owner": principal, "capture_id": capture_id,
                                     "type": "capture_saved", "status": "executed", "at": now.isoformat()}
        result = Result("saved_in_memory", action_id, tuple(items), tuple(rules))
        self._commits[capture_id] = (digest(proposal), result)
        capture["status"] = "saved_in_memory"
        return result

    def undo(self, principal, action_id):
        action = self._owned(self._actions, principal, action_id)
        require(action["type"] == "capture_saved", "not_reversible_action")
        if action["status"] == "reversed":
            return action["reversed_by"]
        at = instant(self.clock()).isoformat()
        reversal_id = str(uuid4())
        for item in self._items.values():
            if item["action_id"] == action_id:
                item["status"] = "reversed"
        for rule in self._rules.values():
            if rule["action_id"] == action_id:
                rule["status"] = "reversed"
                for occurrence in self._occurrences.values():
                    if occurrence["rule_id"] == rule["id"]:
                        occurrence["status"] = "cancelled"
        self._actions[reversal_id] = {"id": reversal_id, "owner": principal, "capture_id": action["capture_id"],
                                      "type": "reversal", "status": "executed", "reversal_of": action_id,
                                      "at": at}
        action["status"], action["reversed_by"] = "reversed", reversal_id
        self._captures[action["capture_id"]]["status"] = "reversed"
        return reversal_id

    def capture(self, principal, capture_id):
        return deepcopy(self._owned(self._captures, principal, capture_id))

    def source_for_item(self, principal, item_id):
        item = self._owned(self._items, principal, item_id)
        return self.capture(principal, item["capture_id"])

    def view(self, principal, collection, include_history=False):
        text(principal, 200)
        require(collection in {"items", "rules", "occurrences", "actions"}, "unknown_collection")
        table = {"items": self._items, "rules": self._rules,
                 "occurrences": self._occurrences, "actions": self._actions}[collection]
        return deepcopy([v for v in table.values() if v["owner"] == principal and
                         (include_history or collection == "actions" or v["status"] == "active")])
