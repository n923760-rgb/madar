# MADAR v2.2 — Universal capture understanding addendum

Date: 2026-10-31. Owner direction: receive natural requests and attachments, classify them, and preserve the correct records. This document refines Product Master v2.1 §§4–22, 24–27 and 33; it does not replace its preserved snapshot. Read v2.1 + accepted Decision Log amendments + this addendum together. The requested capability is accepted scope; the detailed output contract, retention defaults and provider integration remain candidates for implementation review. UX-012/014 hold/release and the approved five-area navigation remain in force.

## 1. One entry point, appropriate results

The user sends content before choosing a category. The central circle captures voice by hold/release; text, image, screenshot, PDF/file and forwarded Telegram messages use the same capture pipeline. The bot accepts content; the Mini App organizes and retrieves it. Input modality is separate from intent. A PDF can be a receipt, an appointment notice or an ordinary document.

“All requests” means broad personal capture coverage with an honest fallback, not a promise to interpret every file or perform external actions. Booking, payment, contacting people, general web answers, accounting, medication advice and government-service execution are outside this capture contract. An instruction to remember an external action becomes a task; it does not execute that action.

| User example | Result | Where it appears |
|---|---|---|
| «أحتاج أرسل عرض السعر» | Undated task; no invented deadline/reminder | Home task summary, Search; Calendar's undated-task list, outside dated cells |
| «ذكّرني اليوم الساعة ٦ مساءً أرسل العرض» | Task with an explicit date/time reminder; one linked rule | Home, Calendar, source detail |
| «عندي موعد أسنان ٥ نوفمبر الساعة ٤ مساءً» | Appointment; reminder only if requested or an approved user default applies | Home, Calendar; source retained |
| «ذكرني الخميس» | Clarify action and, if needed, exact Thursday/time | Inbox needs confirmation |
| Receipt/image | Private original + purchase/expense or asset/document association when supported | Search, related timeline; no Invoices tab |
| «هذي فاتورة التلفزيون، احفظها» | Preserve attachment even without warranty data | Source detail, Search; link only to an unambiguous object |
| Insurance PDF | Document + explicit expiry; renewal reminder according to approved preferences | My Things, Calendar, source |
| «شاهد يتجدد يوم ١٥ بـ٦٥ ريال كل شهر» | Subscription and next renewal rule; amount 6500 halalas, SAR | My Things, Calendar, Search |
| «غيرت الزيت على ٥٣٤٢٠ ويمشي ١٠ آلاف» | Maintenance/reading events after object resolution; next mileage 63420 | Vehicle timeline; no fabricated calendar date |
| «مقاس فلتر السيارة ABC-42، احفظه» | Searchable saved capture/note, optionally linked | Search/source; no new top-level Note object type |
| «وين فاتورة التلفزيون؟» | Retrieval request over authorized records | Ask MADAR with source or honest no-result |

No Tasks/Appointments/Invoices/Notes permanent tabs are added. Invoice, document and note originals remain accessible through Search/source and relevant objects. Preserve the v2.1 four object types: vehicle, document, subscription, asset. A saved note is a retained capture, not a fifth unrestricted object type.

## 2. Capture lifecycle and truthful saving

1. Authenticate the sender; assign capture ID, owner, received timestamp/timezone and stable Telegram/update idempotency key outside the model.
2. Validate attachment size/content/type, preserve the private original when allowed, and mark processing state. Unsupported or unreadable files remain recoverable according to ingestion policy; prohibited executable/unsafe content is rejected or quarantined and may retain metadata only. Never claim its contents were read.
3. Normalize text/transcript/OCR into source segments with IDs. Keep the original separately. Forwarded timestamps are evidence, not a replacement for received time when resolving “today”.
4. The model returns a versioned proposal using [UNDERSTANDING-PROMPT.md](UNDERSTANDING-PROMPT.md) and [contract.schema.json](contract.schema.json). It does not write data or send notifications.
5. Deterministic validation checks evidence, date/time, currency/money, known object IDs, permissions, duplicate candidates and reminder invariants. Field confidence is a model signal, not permission to bypass validation.
6. Clear low-risk groups commit once through the action layer. Missing/uncertain required details ask a compact item-specific question. Keep all content recoverable while awaiting clarification.
7. Show concise results, resolved date/time when relevant, View/Edit and action-specific Undo. Say “saved” only after committed storage; track reminder creation separately from actual delivery.

A multi-intent capture is proposed as one atomic group in this candidate: if any required clarification remains, disposition is `clarify` and no domain actions execute yet. The raw capture is already retained. Do not silently save half the message. Later independent group execution requires a separately reviewed contract.

## 3. Classification and field policy

Supported item intents: `task`, `appointment`, `reminder`, `invoice`, `document`, `subscription`, `maintenance`, `odometer`, `note`. Retrieval is an envelope disposition and creates no new records. Correction/deletion requests must identify an existing action/record through the action layer; do not convert them into a new note or blindly update a matching name.

- A timed request to do something becomes a task plus linked reminder; it must not create a duplicate standalone reminder item for the same instruction. An appointment reminder links to that appointment.
- A standalone reminder is for a reminder without a task/appointment domain entity, such as an explicit expiry alert. One next active occurrence per rule; calendar previews are calculated.
- Required task content: meaningful title. A deadline is optional. Required appointment fields: purpose, date and either explicit time or explicit all-day intent. No automatic “9 AM”.
- “Today” without a time can be a dated task. “Remind me today” requires an intended reminder time, unless the user has explicitly configured a usable default. Do not reuse appointment notification lead time as a task due time.
- Arabic/English numerals normalize; date-only values remain local dates. Timed values require timezone. Resolve relative dates against the supplied received time in the user's timezone. Missing anchor/timezone asks, it does not use model/server time.
- “8” without AM/PM is ambiguous. “Thursday next”, Hijri/numeric dates and prayer/salary-relative phrases require compact clarification or authoritative supplied context. Past explicit time asks; do not silently roll it forward. Retain original time phrase and resolution provenance.
- Money uses integer minor units and explicit currency. Never infer a currency from a bare number without safe context. Multiple totals/credit notes require their correct semantics; do not choose the largest number by default.
- Receipts need no invented warranty or expiry. An unreadable receipt may be retained as a source-only capture; this is not successful extraction. Plain expenses are unlinked expense events. Assets require user intent/evidence; existing object candidates are resolved before proposing creation.
- Documents without expiry may be saved without a renewal reminder. If a renewal reminder is explicitly requested, ask only for expiry/timing. Never fabricate a date from a filename.
- Maintenance needs object resolution and required service fields. An interval is required to create the next mileage rule. No next due date from mileage alone. Lower odometer readings than current evidence need review, not automatic projection overwrite.
- Notes preserve stated content and source. Secrets/OTP/password/card data are not normalized into notes. Reject unnecessary sensitive storage, minimize retention and avoid echoing secrets in replies/logs.

All fields carry `source`, `derived`, `uncertain` or `missing` confidence plus source evidence where applicable. Only source/derived required fields may pass automatic validation. Derived values identify their deterministic resolver; the model never invents the resolver result.

## 4. Proposed storage effects

| Intent | Authorized executor effects after validation |
|---|---|
| Task/appointment | Domain row + action/audit links + optional linked reminder rule/one occurrence |
| Reminder | Rule + one active occurrence; no delivery success until channel acknowledgement |
| Invoice | Private attachment + purchase/expense event; optional resolved asset/document link |
| Document/subscription/asset | Existing/create-resolved object + typed extension + event history + supported reminder |
| Maintenance/odometer | Append event(s), transactionally update reading projection, evaluate affected rules |
| Note | Retained searchable capture and optional authorized object link |
| Retrieval | Read-only query over the user's records, sourced answer or no-result; no writes |
| Correction/reversal | Explicit action referencing target + preview when material; preserve history |

These are design contracts, not implemented database tables or persistence. Idempotency keys belong to trusted ingestion/executor code. Probable duplicates offer Open existing / Save as new / Cancel. An object alias such as “my car” does not authorize creation of a new vehicle.

## 5. Failure, privacy and implementation boundary

Do not lose a capture on parse, provider or upload failure. Report local/uploading/processing/needs clarification/saved/failed accurately. A retry reuses capture/action identity and does not duplicate financial events or reminders. Deleting a raw attachment is a separate explicit operation from reversing a business action.

Attachment policy must be configured before real ingestion: allowed content types and size limits, private storage, malware policy, signed access, raw audio/transcript retention, export and deletion. Exact limits/retention are OPEN and no production acceptance of arbitrary file types is claimed. Embedded file/transcript instructions are untrusted data; they cannot replace system instructions or authorize external actions.

## 6. Evaluation and rollout

[cases.json](cases.json) is a synthetic Saudi Arabic golden set with expected intents/dispositions. [check.cjs](check.cjs) validates fixture contracts and rejection cases locally. Passing it means the specification examples are internally consistent, not that a model understood them. No model/provider, audio/OCR, database, Telegram runtime or delivery is exercised.

Run from repository root: `node docs/product/capture-v2.2/check.cjs`. This checks 46 expected-output fixtures, 17 deliberately invalid proposals and original reference integrity. Its schema walker implements only the keywords used here and fails on unknown keywords; it is a specification verifier, not a production JSON Schema/security validator. Production must use a reviewed validator plus domain/authorization checks and actual model evaluations.

Next implementation candidate: authenticated deterministic text capture → validated task/appointment → durable source → correct single reminder occurrence → Edit/Undo, before voice/OCR integration. Add real extraction only behind a versioned adapter after golden-set evaluation; report per-field errors, wrong-object/duplicate rate, unnecessary questions, source correctness and provider cost/latency. No percentage of production readiness is inferred from this documentation packet.
