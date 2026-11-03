# Capture integration boundary — candidate v2.2

Reviewable design for connecting the synthetic action core to the approved MADAR interface. No server, authentication implementation, migration, provider or live UI connection is introduced. Product v2.1 and UX-012/014 remain authoritative. Broad capture stays in scope; the first vertical slice is text → task/appointment/reminder, with honest deferral for other families.

## 1. Experiment review

The [action core](../../../experiments/capture_core/README.md) demonstrates evidence/field/time checks, trusted-caller ownership policy, grouped execution, retry identity and targeted reversal. It is not a persistence or authentication boundary.

| Integration gap | Required behavior |
|---|---|
| Caller supplies principal | Authenticate at ingress; resolve internal owner outside request/model payloads |
| Dictionaries disappear on restart | Durably preserve permitted source, action and projections; acknowledge storage stages accurately |
| Sources change during inference | Bind results to source/context revision; reject stale results before writes |
| Direct `submit` entry point | All production mutation paths use the same mandatory action boundary |
| Single-process validation/mutation | Check authority, revision, invariants and writes under a database transaction |
| Ingest fingerprint includes supplied received time | Assign server received time once; retries reuse it instead of sampling a new clock |
| Only exact retry detection | Separate transport replay from probable semantic duplicates across captures |
| Exact evidence quote | Evaluate extraction semantics separately; a quote does not prove the value is correct |
| `saved_in_memory` result | Never translate it to a production «تم الحفظ» receipt |
| Undo without downstream edits | Detect dependencies; reverse eligible effects only; disclose already sent notifications |

`ProposalGate` is an optional local context-binding experiment. Obtain an owner-scoped context handle before generating a proposal, freeze a separate payload copy with `prepare`, then call `execute`. Source changes reject old context before both preparation and execution. Preparing is neither validation nor saving. The model schema is unchanged; context/run identity belongs to the adapter. This gate has no HTTP, real identity, expiration policy, durable storage or concurrent enforcement. Direct core calls remain possible locally; a future service must eliminate this bypass.

## 2. Identity and trust

Mini App ingress submits raw Telegram `initData` to the server for validation using the official algorithm for the configured bot. Reject invalid/missing signatures and apply an explicitly configured freshness/future-clock policy before session creation. `initDataUnsafe`, URL user IDs, chat IDs, model output and client `owner_id` are not authorization. Never log the raw credential, send it to an AI provider or expose a bot token in the client.

Map the verified Telegram user to an internal owner. Check ownership on every capture, proposal, action, object, source URL and query. A forwarded author never replaces the authenticated sender. Bot updates need their own verified ingress and bot/update identity; Mini App validation does not authenticate webhook JSON.

Select session transport, expiry, revocation and CSRF protection before implementation. Cookie and bearer choices remain open. Unknown and other-owner IDs share a resource-not-found response; expired authentication returns a separate reauthentication response. Issue short-lived source access only after ownership checks. Trusted server context supplies received time, timezone provenance, resolver results, known-object candidates, context revision and provider-run identity. Attachments and proposals cannot supply these authorities. A timezone/context change invalidates uncommitted proposals without silently reinterpreting committed appointments.

## 3. Ingest, propose and commit

1. Authenticate, bound request size, normalize transport identity and validate source policy. Start with text; keep file/audio ingress unavailable until policies and adapters exist.
2. In a short ingest transaction reserve `(owner, channel, ingest_key)`, persist permitted source with immutable IDs, assign received time once and record payload fingerprint. Same key/payload returns the original capture; changed payload conflicts without overwriting. Telegram identity also includes the configured bot. Client timestamps remain evidence.
3. Commit ingest before claiming source receipt. Database failure is retryable failure, not a receipt. A local unsent draft is labelled local; survival after app closure is not promised without an implemented draft policy.
4. Read a trusted context snapshot/version, release locks before slow inference, and correlate the run to that snapshot. Opaque context handles are references, not auth credentials. Authenticate provider callbacks separately; naming a capture ID is insufficient.
5. Validate full schema, evidence, semantic constraints, owner-scoped object resolution and domain invariants. Unsupported families defer the whole group. Required ambiguity goes to Inbox without partial domain writes. Append clarification as a new immutable source, increment context version and invalidate old uncommitted proposals.
6. Clear low-risk proposals may execute automatically under UX-005; do not require confirmation for every task. Material risk/uncertainty gets compact review. Edits and clarification answers undergo validation again.
7. Commit through the action boundary, then return authoritative record/action IDs and resolved timing. Model prose is never an execution receipt.

Candidate service operations: receive capture, read capture status, append clarification, read proposal, execute proposal, read action, reverse action. These are behaviors, not implemented URLs. Execution takes proposal ID, expected context version and idempotency key; it accepts no replacement model payload or owner. Automatic execution uses the same boundary. Reads never start execution.

## 4. Durable transaction contract

Preserve the v2.1 modular monolith/PostgreSQL baseline. Do not persist dictionary snapshots or substitute another database architecture. These are conceptual migration constraints, not executable SQL:

| Constraint | Purpose |
|---|---|
| Unique `(owner, channel, ingest_key)` | One capture for transport replay |
| Unique `(owner, action_key)` + canonical command fingerprint | Same command returns same outcome; changed command conflicts |
| One successful create-group execution per `(owner, capture, group_version)` | Competing proposals cannot both create the same group |
| Owner-inclusive foreign keys where applicable | No cross-owner source/action/rule/record links |
| Unique active occurrence per `(owner, rule_id)` | One active current/future occurrence invariant |
| Unique `(owner, reversal_of_action_id)` | Repeated Undo returns existing reversal |
| Unique outbox event/delivery identity | Dispatch retry cannot create extra business rules |

Lock the capture row first, then affected records/rules in stable order. Re-read owner, current context version, proposal identity, execution ledger and active occurrences under the lock. A previously committed identical command returns its outcome after response loss; a reversed outcome stays reversed. Stale uncommitted proposals conflict and refresh context instead of silently changing interpretation.

Revalidate time against trusted execution time and the resolved timezone; delayed past reminders ask rather than roll forward. Validate the entire group. Write domain projections, source links, action/audit events, reminder rule/single occurrence, execution receipt and any outbox event in **one transaction**. Rollback exposes none of those domain effects; previously retained source remains available with accurate retry/clarification state. Release locks before channel/provider calls. Reconcile uniqueness violations to a known retry or conflict, never unconditional success.

Database and private object storage do not share one transaction. Future file ingestion needs staged upload/finalization, integrity/ownership checks, quarantine, orphan cleanup and retention. A metadata row alone is not a usable original. Exact limits and retention remain open; text-only execution must not advertise file acceptance.

Outbox creation means queued, not delivered. Recheck occurrence/cancellation before dispatch and record channel acknowledgement separately. Undo cancels pending work atomically with reversal, but cannot promise recall after external send. A crash between send and acknowledgement can leave uncertain delivery; do not claim universal exactly-once external delivery without channel support/reconciliation. Workers and delivery remain outside this slice.

Reversal locks the explicit action and affected records, appends a reversal event, updates projections and cancels eligible occurrences while preserving source/history. If later independent edits/dependent events would be overwritten, return a conflict for review. Edit is a separate validated action, never source replacement or “undo last”.

## 5. Five-view interface contract

Preserve the central circle, hold/release, configurable physical directions and tap alternatives. Release ends capture and starts submission; it is not proof of storage. Keep the approved internal composer and RTL navigation. Add no Tasks, Appointments or Invoices tab.

| State | Arabic copy candidate | Controls/effect |
|---|---|---|
| Local unsent draft | «لم يُرسل بعد» | Retry/Cancel; no saved pulse/calendar record |
| Sending | «جارٍ إرسال طلبك…» | Keep operation identity; gesture cancellation only before submission |
| Source durably received | «وصل طلبك، جارٍ تنظيمه…» | Reopen status by capture ID; no task/reminder claim yet |
| Clarification | «متى تبغاني أذكّرك؟» | Compact contextual question, source access, Inbox badge |
| Duplicate candidate | «قد يكون محفوظًا من قبل» | Open existing / Save as new / Cancel; no silent merge |
| Committing | «جارٍ الحفظ…» | Repeated presses reuse the same operation |
| Timeout, outcome unknown | «نتحقق من حالة الحفظ…» | Query status; retry same command; no blind new key or false failure |
| Committed task | «حُفظت المهمة» | View/Edit/Undo from receipt; no reminder claim without committed rule |
| Committed reminder | «حُفظ التذكير» + date/time | Reminder configured, not notification delivered |
| Unsupported/extraction failed | «لم نتمكن من تنظيم هذا الطلب بعد» | Report only what was retained; inspect source/retry when available |
| Session expired | «افتح مدار من تيليجرام للمتابعة» | Preserve screen where feasible; no replay under a new identity |
| Reversal committed | «تم التراجع عن هذه العملية» | Refresh affected projections; source/history stay accessible |

Home shows committed summaries and a discreet processing/clarification link. Inbox owns pending captures, compact questions and recoverable failures. My Things receives only resolved object associations; a task does not create an asset. Calendar shows committed dated items, date-only entries without fake midnight, and separate undated tasks. Ask MADAR searches authorized committed records with sources; no cross-owner processing content or general-chat fallback.

View/Edit/Undo retain explicit IDs across navigation/reopening. Refresh authoritative projections after commit/reversal. Any optimistic pending item stays visibly pending and excluded from saved counts. Back closes the current sheet first; it does not cancel a submitted server action. Use visible status text, polite live regions, keyboard-accessible controls, suitable focus on questions/results, inline errors, reduced motion and contrasting tokens in both modes. UI/assistive-technology qualification is separate work.

## 6. Acceptance evidence required for real integration

| Area | Required evidence |
|---|---|
| Authentication/ownership | Valid credentials; invalid/expired/future/wrong-bot rejection; owner-isolated resources and queries |
| Restart durability | Source/commit survive restart; failed commit keeps source and no partial effects |
| Concurrency | Identical/different simultaneous commands, two provider results, clarification during inference, commit/Undo contention, single occurrence |
| Crash recovery | Faults around commit/response, stable receipts, outbox recovery without duplicate business actions |
| Revision | Late results rejected at preparation/execution; newer sources not overwritten |
| Undo dependencies | Explicit target, repeated reversal, conflict across dependent edits |
| UI truthfulness | Timeout reconciliation, retry, clarification, duplicate and reversal; no timer/model-generated success |
| Mobile/accessibility | Real Telegram touch/keyboard, interrupted hold, RTL Back, screen readers, reduced motion, dark/light/narrow layouts |
| Provider quality | Held-out Arabic extraction, temporal/object errors, false saves, source fidelity, unnecessary questions |

Local gate tests cover ordered source changes, trusted-principal owner policy, frozen payloads, validation deferral and retry/reversal. They are not auth, PostgreSQL, restart, actual concurrency, delivery, model or browser evidence. Execution checkpoints and next work belong only in [MASTER_ROADMAP](../../../ENGINEERING/MASTER_ROADMAP.md).

## Primary technical references

Consulted 2026-10-31; support platform mechanics, not MADAR design approval:

- [Telegram validation](https://core.telegram.org/bots/webapps#validating-data-received-via-the-mini-app): raw init data/server validation and authentication timestamp.
- [PostgreSQL explicit locking](https://www.postgresql.org/docs/18/explicit-locking.html): row locks and contention; application behavior still needs testing.
- [PostgreSQL partial indexes](https://www.postgresql.org/docs/18/indexes-partial.html): basis for a unique index over a reviewed active-occurrence predicate; exact migration/status predicate still needs review.
