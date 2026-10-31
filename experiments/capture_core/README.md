# Local capture/action core experiment

2026-10-31. Bounded executable follow-up to the v2.2 understanding contract in PR #5. Uses synthetic normalized text and reviewed structured proposals. It does **not** classify arbitrary text, call an AI model, record audio, process invoice files or run a server. No production services, backend deployment, durable database or UI integration are introduced.

## Run

Python 3.12+ with IANA timezone data (available in the tested Linux environment); no third-party Python dependencies.

```sh
python -m unittest discover -s experiments/capture_core -p 'test_*.py' -v
python experiments/capture_core/demo.py
node docs/product/capture-v2.2/check.cjs
```

The demo executes five golden proposals: undated task, timed task/reminder, appointment, missing-time clarification and an invoice deferred without domain writes. Replaying each yields the same result. Reversing the timed task leaves the two unrelated records active and cancels its single reminder occurrence. The fixed synthetic clock is 31 October 2026 at 09:00 in Riyadh; no real notification is sent.

## What actually executes

| Behavior | Local implementation |
|---|---|
| Source ingestion | Bounded normalized text segments copied into session memory with immutable source identity |
| Retry identity | Owner-scoped ingestion key; exact retry returns the same capture; changed payload conflicts; identical title/date/time proposals in one group are rejected |
| Proposal validation | Narrow task/appointment/reminder adapter; version/capture identity, allowed fields, evidence quotes, trusted resolver results and field confidence |
| Date/time | Strict dates/24-hour times, explicit all-day, required reminder time, UTC conversion, past-time and DST gap/fold rejection |
| Save | Validate the whole supported group, then create in-memory records and action trace; no partial supported group save |
| Reminders | One in-memory rule and one active occurrence per requested reminder; replay creates no additional occurrence |
| Clarification | Keep the original, append the answer as a new source, then resubmit under the same capture ID |
| View/source | Owner-scoped projections and source links; returned copies cannot mutate internal state |
| Undo | Explicit action ID, reversal trace and retained original; unrelated later captures remain active; repeats are idempotent |
| Other intents | Defer the whole proposal; invoice/asset/document/subscription/maintenance handling is not implemented here |

`principal`, received timestamps, timezone and resolver context must come from a future trusted adapter. Passing a user ID is **not authentication**. Tests establish local owner-policy behavior, not Telegram `initData` validation, HTTP authorization or a deployable security boundary. Unsupported intents are deferred before field-level validation because no domain execution occurs; this is not a full implementation of the v2.2 schema.

## Verification and limits

30 Python behavior tests PASS, including no partial writes, exact retry, cross-owner access denial, source preservation, clarification round-trip, timezone/DST/past-time cases, duplicate proposal rejection, atomic multi-item save/reversal and targeted reversal. The demo PASS, v2.2 fixture verifier PASS (46 expected outputs / 17 rejection fixtures), and `git diff --check` PASS. Original product/UX reference hashes remain unchanged.

All records disappear when the `CaptureCore` instance/process ends. Single-process synchronous code is not thread-safe, transactional durable storage or crash recovery. Only exact retry identity is handled: similar-content/semantic duplicate detection across distinct capture keys is NOT implemented. The model's semantic correctness is not established by an exact quote, confidence label or passing this adapter. Reviewable proposals still require real provider evaluation.

**NOT RUN / not implemented:** real authentication/Telegram, arbitrary Arabic parsing, actual microphone/transcription/OCR, file upload/private object storage, durable persistence, concurrency/crash recovery, editing/snooze/recurrence, actual notification delivery, invoice routing execution and browser/mobile integration. Do not connect personal data or deploy this experiment as production. Current project status and next task belong only in `ENGINEERING/MASTER_ROADMAP.md`.
