"""Execute reviewed synthetic proposals, not natural-language model predictions."""

from datetime import datetime
import json
from pathlib import Path

from core import CaptureCore


def main():
    root = Path(__file__).resolve().parents[2]
    corpus = json.loads((root / "docs/product/capture-v2.2/cases.json").read_text())
    core = CaptureCore(lambda: datetime.fromisoformat("2026-10-31T09:00:00+03:00"))
    trace = []
    target = None
    for name in ("task-undated", "task-timed-reminder", "appointment-explicit", "today-reminder-no-time", "invoice-expense"):
        case = next(c for c in corpus["cases"] if c["id"] == name)
        context = case["input"]
        capture = core.receive("demo-owner", name, context["sources"],
                               datetime.fromisoformat(context["received_at"]), context["user_timezone"],
                               {r["resolver_id"]: r["value"] for r in context["resolver_results"]})
        proposal = case["expected"]
        proposal["capture_id"] = capture["id"]
        result = core.submit("demo-owner", capture["id"], proposal)
        retry = core.submit("demo-owner", capture["id"], proposal)
        assert result == retry
        trace.append({"case": name, "result": result.status, "items": len(result.item_ids),
                      "rules": len(result.rule_ids), "retry": "same result"})
        if name == "task-timed-reminder":
            target = result
    core.undo("demo-owner", target.action_id)
    print(json.dumps({"mode": "synthetic proposals / session memory only", "trace": trace,
                      "after_targeted_undo": {"active_items": len(core.view("demo-owner", "items")),
                                              "active_occurrences": len(core.view("demo-owner", "occurrences")),
                                              "actions_including_reversal": len(core.view("demo-owner", "actions"))},
                      "not_implemented": ["natural language understanding", "real authentication", "durable storage",
                                          "invoice ingestion", "audio/OCR", "notifications", "UI integration"]},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
