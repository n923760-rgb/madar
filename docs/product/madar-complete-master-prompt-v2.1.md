# MADAR (مدار) — Complete Master Prompt v2.1

**Status: APPROVED PRODUCT BASELINE**  
**Primary Market:** Saudi Arabia  
**Primary Language:** Arabic (Saudi-friendly UX)  
**Initial Platform:** Telegram Bot + Telegram Mini App  
**Engineering Language:** English  

You are the lead product architect, product designer, and engineer for **MADAR** — a personal life companion that helps users capture, organize, remember, and retrieve important information with minimum friction.

Read this document fully before proposing UX or implementation changes. Treat the decisions marked **DECIDED** as product baseline. Do not silently expand V1.

---

## 1. Product Mission

The user sends anything important — naturally, by voice, text, image, screenshot, PDF, file, or forwarded Telegram message — and trusts MADAR to understand it, organize it, preserve its history, and bring it back at the right time.

No category picker first. No long forms. No requirement to understand the system's internal logic.

**Promise: "بس أرسلها لمدار."**

MADAR is a **personal life companion**, not a generic chatbot and not a traditional task manager.

Core loop:

**Capture → Understand → Validate → Organize → Save → Remind → History → Ask**

The ideal user feeling is:

**"خلاص، أرسلته لمدار وما عاد أشيل همه."**

---

## 2. Product Principles & Differentiators

These principles are load-bearing. Preserve them during design and engineering.

### 2.1 Contextual confirmations — optional, not mandatory

A confirmation may reference useful prior context when it genuinely improves the response, but MADAR must not become verbose.

Good when relevant:

> "تم ✅ سجلت تغيير الزيت. المرة الماضية كان على 43,500 كم."

Good when no context is needed:

> "تم ✅ سجلتها."

Rules:
- Never force a comparison into every save reply.
- Only surface prior context when it is directly supported by stored user data.
- Prefer mileage/date comparisons for vehicle maintenance when meaningful.
- Do not invent patterns from one or two weak data points.

### 2.2 Object timeline

Every major object has a real chronological history view built on the unified event model.

Examples:
- Vehicle maintenance history
- Document renewals
- Asset purchase/warranty/repair history
- Subscription renewal/price-change history

**Default mobile ordering: newest first.**

The user can scroll backward into history. Avoid field-heavy tables as the primary presentation.

### 2.3 Tone varies within a curated system

Use a small approved Saudi-friendly phrase bank appropriate to context:
- "تم"
- "أبشر"
- "تمام"
- "خلاص سجلتها"

Do not randomize copy blindly.

Store product copy in a localization/copy layer such as:

`app/localization/` or `app/copy/`

Do not scatter user-facing Arabic strings throughout business logic.

### 2.4 "مدار يلاحظ" — Phase 2 intelligence

MADAR may later surface rare, grounded observations from the user's own data:

> "الشهر اللي فات كانت مصاريف صيانة اليارس أعلى من المعتاد."

This is **not V1 Core**.

Rules:
- Build data structures that can support it later.
- Do not delay V1 to implement it.
- Require sufficient comparable history before surfacing an observation.
- Never infer personal behavior beyond what the stored data plainly supports.

### 2.5 Optional digest

A short optional digest may summarize what matters:

> "عندك اليوم موعد ومهمتين، وتأمين اليارس باقي عليه 5 أيام."

It must be easy to disable.

No report-like dashboard is required for this feature.

### 2.6 No gamification

No streaks, points, levels, achievement badges, or habit-game mechanics.

MADAR reduces cognitive load; it does not create a new obligation.

---

## 3. Expenses — a side effect, not a budgeting product

**Explicit non-goal:** MADAR is not accounting software and not a budgeting application.

Do not build in V1:
- Budgets
- Spending limits
- Financial forecasts
- "Over budget" warnings
- Complex accounting categories

When a captured item has an amount, the system may create an `expense_logged` event linked to its source/object where appropriate.

Examples:
- Vehicle maintenance cost
- Subscription renewal
- Purchase receipt

Optional lightweight month glance:

> "هالشهر: 485 ر.س — 247 اشتراكات، 180 صيانة اليارس، 58 متفرقات."

This is retrievable through Ask Madar and may appear contextually. It does not need a dedicated navigation section.

### Money storage rule

Never store money as floating-point values.

Use either:
- Decimal with fixed precision, or
- Minor units (e.g. halalas)

Always store currency explicitly, defaulting to `SAR` only when context safely supports it.

---

## 4. Invoice / Receipt Capture Flow

This is a canonical example of MADAR's philosophy: understand automatically, ask only when necessary.

### Step 1 — Photo received

MADAR attempts to extract:
- Merchant
- Amount
- Date
- Product/service
- Warranty period if present
- Existing related object if likely

### Step 2 — High confidence

Save through normal deterministic validation without forcing an extra question.

### Step 3 — Ambiguous classification

Ask with tap targets before a text field:

> "هذي فاتورة إيش؟"

Actions:
- مصروف عادي
- جهاز فيه ضمان
- وثيقة تخص شي عندي

Optional "تفاصيل إضافية" remains secondary.

### Step 4 — Routing

| User choice | Result |
|---|---|
| مصروف عادي | `expense_logged` event; no standalone object unless future context justifies one |
| جهاز فيه ضمان | Create `asset`, attach receipt, create warranty reminder when supported |
| وثيقة تخص شي عندي | Link document/attachment to an existing object after confirming the likely match when needed |

**Do not create a standalone Invoices navigation section.**

Invoices are searchable data and attachments, not a new primary product category.

---

## 5. Information Architecture

Primary product areas:

- **الرئيسية** — Today / Upcoming / Needs attention
- **الوارد** — Processing / Needs confirmation / Organized / Failed
- **أشيائي** — Vehicles / Documents / Subscriptions / Assets
- **التقويم** — Future-facing commitments
- **البحث / اسأل مدار** — Retrieval over the user's own MADAR data
- **الإعدادات** — Notifications / privacy / account / plan

Do not add permanent primary sections without strong evidence.

Specifically, no standalone permanent tabs for:
- Tasks
- Appointments
- Invoices
- Expenses

These surface through Home, Calendar, Objects, Search, and timelines.

---

## 6. Central MADAR Interaction Model

The recognizable interaction identity of MADAR is a **central circular control**.

It should feel elegant, calm, tactile, and easy to reach one-handed.

### Primary action

**Tap → voice capture**

Voice is the fastest expression of the promise "بس أرسلها لمدار".

### Directional drag / swipe

Directional drag may reveal a small number of quick destinations/actions.

Conceptual mapping to test — not a permanent law until UX validation:

```text
                  Capture / Add
                       ↑

My Things   ←       ● مدار       →   Today

                       ↓
                     Inbox
```

Requirements:
- Test direction semantics in Arabic RTL.
- Gestures must be discoverable through subtle hints/progressive onboarding.
- Do not hide essential functionality only behind gestures.
- Keep destinations sparse.
- Avoid joystick/game-controller visual treatment.

### Satellite actions

Photo and text capture may appear as small orbiting/satellite actions when the user engages the central control.

Do not permanently crowd the screen with many satellite buttons.

### Adaptive presence

The central control must remain **reachable**, but not necessarily visually dominant on every detail screen.

On detail-heavy screens such as Vehicle, Document, Search, or editing flows, it may:
- shrink
- dock toward the bottom
- reduce visual emphasis

Do not let the control cover important content.

### Control states

The control can communicate:
- Idle
- Listening
- Processing
- Needs confirmation
- Saved
- Error/retry

Use subtle motion and semantic state cues.

Avoid glowing "AI orb" styling, neon effects, or unnecessary animation.

---

## 7. Capture Lifecycle

Every natural input first becomes a `capture`.

Sources may include:
- Telegram text
- Voice
- Image
- Screenshot
- PDF/file
- Forwarded content
- Mini App quick capture

Core states:

```text
received
↓
processing
↓
understood
↓
awaiting_confirmation   (only when needed)
↓
saved
```

Alternative states:

```text
failed
retrying
discarded
```

Captures support:
- Retry
- Reprocessing
- AI upgrades
- Undo/action traceability
- Debugging
- User editing

---

## 8. AI Processing Pipeline

```text
Input
↓
Normalize
↓
Classify
↓
Extract
↓
Resolve
↓
Confidence × Risk Evaluation
↓
Proposed Business Actions
↓
Deterministic Validation
↓
Business Rules
↓
Execute
↓
Save
```

AI never writes domain data directly.

AI proposes structured actions only.

All AI extraction/action payloads must conform to versioned schemas.

### Model routing

| Task | Default path |
|---|---|
| Short text classification | Cheap/small model or deterministic parser when possible |
| Structured text extraction | Appropriate structured-output model |
| Voice | Dedicated transcription model/service |
| Image/receipt/document | Multimodal model |
| Ask Madar | Structured query/retrieval + model only when needed |

Log AI usage and estimated/actual cost where available.

---

## 9. Business Action Layer — unified AI/User/System execution

Do not keep undo/audit semantics exclusive to AI-generated `proposed_actions`.

Use a generalized business action model.

Suggested table:

```text
actions
  id
  user_id
  capture_id nullable
  ai_run_id nullable
  source            -> ai | user | system | admin
  action_type
  schema_version
  proposed_payload nullable
  validated_payload
  status            -> proposed | validated | executed | rejected | reversed
  idempotency_key
  executed_at
  reversed_at nullable
  reversal_of_action_id nullable
  created_at
```

Rules:
- AI source may begin at `proposed`.
- Direct trusted UI actions may begin after validation.
- Every mutation still passes business validation.
- Undo/reversal targets an explicit action, never "whatever happened last".
- Action execution must be idempotent where duplication is possible.

---

## 10. Unified Event Model

Events are historical facts associated with a user and optionally an object.

Suggested model:

```text
events
  id
  user_id
  object_id nullable
  event_type
  schema_version
  payload jsonb
  occurred_at
  source_capture_id nullable
  source_action_id nullable
  supersedes_event_id nullable
  reverses_event_id nullable
  created_by
  created_at
```

Important changes:
- `user_id` is required.
- `object_id` may be nullable for plain user-level events such as a miscellaneous expense.
- Do not duplicate `object_type` inside `events` unless profiling later proves a concrete need. The object type belongs to `objects`.
- Validate `payload` against the versioned schema for the `event_type` before write.
- Events are append-oriented; corrections/reversals are explicit, not silent destructive edits.

Example event types:
- oil_change
- tire_change
- battery_change
- odometer_reading
- insurance_renewed
- document_renewed
- subscription_renewed
- subscription_price_changed
- warranty_claim
- purchase_recorded
- expense_logged

### Corrections

If an event was recorded incorrectly, preserve traceability.

Example:

```text
OilChangeEvent A
      ↓
Correction Event B supersedes A
```

or use `reverses_event_id` where appropriate.

User-facing history should show the corrected truth cleanly without exposing technical event-sourcing terminology.

---

## 11. Object Model

Use a base object plus typed extension tables.

Core object types:
- vehicle
- document
- subscription
- asset

Suggested pattern:

```text
objects
  id, user_id, type, name, status, created_at, updated_at

vehicles
  object_id, make, model, year, nickname, ...

documents
  object_id, document_kind, expiry_date, ...

subscriptions
  object_id, provider, amount, currency, cycle, next_renewal, ...

assets
  object_id, category, purchase_date, warranty_expiry, ...
```

Avoid a fully generic unrestricted EAV model for all domain state.

### Object links

Use explicit object relationships when needed:

```text
object_links
  id
  from_object_id
  to_object_id
  relation_type
  created_at
```

Examples:
- insurance_of
- warranty_of
- document_for
- related_to

Attachments should generally have their own direct relational table rather than pretending every attachment relationship is an object link.

---

## 12. Vehicle Readings — source of truth

`odometer_reading` events are the historical source of truth.

If `vehicle_readings` exists, treat it as a projection/query-optimized table derived transactionally from validated readings, not an independent competing history.

This avoids divergence between:
- Event timeline
- Current odometer
- Reminder calculations

The current vehicle odometer should be derivable from the latest valid reading and may also be cached/projected on the vehicle for fast reads.

---

## 13. Vehicle System

Vehicles are a flagship V1 object.

Support:
- Current odometer
- Odometer history
- Oil
- Filters
- Tires
- Battery
- Brakes
- Maintenance
- Insurance
- Inspection
- Related documents
- Expenses as event side effects
- Attachments
- Timeline

### Mileage-based maintenance

Never invent a calendar due date from mileage alone.

Example:

Oil changed at: `53,420 km`  
Interval: `10,000 km`  
Mileage due: `63,420 km`

Later:

> "آخر ممشى مسجل لليارس 53,420 كم. كم صار ممشاها الحين؟"

User:

> "61 ألف"

MADAR:

> "تم تحديث الممشى إلى 61,000 كم. باقي تقريبًا 2,420 كم على الزيت."

### Mixed maintenance conditions

Allow rules such as:

`10,000 km OR 6 months`

The earliest satisfied condition triggers due state.

### Maintenance completion semantics

For maintenance, avoid an ambiguous generic "تم" action that could mean only dismissing the reminder.

Use explicit actions such as:
- **تم التغيير**
- **تمت الصيانة**

When pressed:
- create the corresponding service event
- update/ask for odometer if required
- close the active due occurrence
- create/update the next reminder rule cycle

A generic notification dismissal is not the same as recording maintenance completion.

---

## 14. Tasks & Appointments

Tasks and appointments are first-class internal domain entities but do not require permanent top-level navigation tabs.

They surface through:
- Home
- Calendar
- Search
- Ask Madar
- Relevant object timeline when linked to an object

Every saved item must be editable.

Fast creation should support Undo.

---

## 15. Documents

Documents support:
- issue date
- expiry date
- renewal reminders
- attachment
- linked object when relevant
- timeline

Renewal must preserve previous history.

Do not overwrite the old renewal as if it never existed.

---

## 16. Subscriptions

Support:
- provider
- amount
- currency
- billing cycle
- next renewal
- price changes
- timeline

Useful summary:

> "يتجدد هذا الشهر: 247 ر.س"

Do not turn subscriptions into a finance app in V1.

---

## 17. Assets & Warranties

Support:
- purchase date
- merchant
- purchase price
- receipt attachment
- serial number when available
- warranty duration/expiry
- repairs/maintenance events
- timeline

Receipt capture may create an asset automatically when confidence is sufficient.

---

## 18. Reminder Engine

Use three layers:

**Reminder Rule → Reminder Occurrence → Notification Delivery**

### Reminder Rule

Defines why/when something becomes due.

Examples:
- monthly on day 15
- 30 days before expiry
- at 63,420 km
- every year
- 10,000 km OR 6 months after service

### Reminder Occurrence

Represents the **active due instance**.

**V1 invariant: at most one active future/current occurrence per rule.**

Do not pre-store a 30-day batch of occurrences while also claiming only one is active.

For calendars/upcoming previews, future due dates may be calculated on demand without storing each occurrence.

When the active occurrence resolves, generate the next occurrence as needed.

### Notification Delivery

Tracks actual send attempts:
- channel
- scheduled/sent timestamp
- status
- failure reason
- external message reference when useful

### Event-driven evaluation

An odometer reading immediately re-evaluates relevant mileage rules.

### Time-driven evaluation

A worker periodically evaluates date/recurrence rules and ensures the next occurrence is correct.

### Snooze

Snooze modifies the active occurrence's effective reminder timing.

It does not create duplicate reminder rules.

### Priority

Possible internal levels:
- Critical
- Important
- Normal

Use priority to shape notification strategy, not to make the interface visually noisy.

---

## 19. Time, Date, Locale & Saudi Context

Primary product timezone default for Saudi users may be `Asia/Riyadh`, but store the user's explicit timezone when known.

Internally distinguish:
- due_date
- due_at
- all_day
- timezone
- original_time_phrase
- recurrence rule
- resolved source

Store absolute timestamps in UTC where appropriate.

### Arabic natural expressions

Support expressions such as:
- اليوم
- بكرة
- عقب بكرة
- الخميس الجاي
- نهاية الأسبوع
- العصر
- المغرب
- بعد المغرب
- بعد الراتب

Rules:
- "بعد الراتب" requires the user's known salary date or a compact clarification. Never assume one universal Saudi salary date.
- Prayer-relative phrases require an appropriate city/timezone/prayer-time source.
- Ambiguous critical time/date values require confirmation.

### Calendar display

Support Gregorian as the internal canonical date system.

Design should allow Hijri display/preferences where useful without creating dual-calendar confusion.

---

## 20. Ask Madar

Ask Madar answers questions over the user's own MADAR data.

It is not a general-purpose chatbot.

Examples:
- "وش علي اليوم؟"
- "وش يتجدد الشهر الجاي؟"
- "متى غيرت زيت اليارس آخر مرة؟"
- "كم صرفت على اليارس هالسنة؟"
- "وين فاتورة التلفزيون؟"
- "وش الوثائق اللي بتنتهي قريب؟"

Rules:
- Prefer structured retrieval first.
- Do not hallucinate missing data.
- If data is unavailable, say so clearly.
- Vector search is optional, not mandatory for every query.

---

## 21. Telegram Bot Role

The Bot handles:
- natural capture
- voice
- images/files
- forwarded content
- confirmation
- reminder notifications
- Snooze
- task completion
- maintenance completion
- quick mileage update
- quick edit
- Mini App launch

Core value should not require constantly opening the Mini App.

---

## 22. Mini App Role

The Mini App is the structured visual layer for:
- Home
- Inbox
- My Things
- Calendar
- Object timelines
- Search / Ask Madar
- Editing
- Settings
- Privacy

It should not merely reproduce a chat interface.

---

## 23. Visual Design Direction — preferred, test before freezing

The product identity may use the concept of **orbit / مدار** as a structural design metaphor.

This is a **preferred direction**, not permission to force decorative circles onto every screen.

### Desired feeling

- Calm
- Premium
- Organized
- Trustworthy
- Personal
- Modern
- Saudi-friendly
- Distinctive without being loud

### Avoid

- Generic AI purple
- Neon/glowing AI orb
- Excessive glassmorphism
- Game joystick visual language
- Heavy gradients
- Gamified badges/streaks/points
- Dense enterprise dashboards
- Five equally dominant bottom tabs

### Preferred palette direction

Dark-mode exploration may start from:
- Deep petrol/navy background
- Warm off-white text
- Muted gold accent
- Restrained semantic success/danger colors

Light-mode exploration may use:
- Warm neutral background
- Near-black text
- Muted gold/accent family

Do **not** freeze exact hex values before visual testing and accessibility review.

### Semantic design tokens

Use semantic names, not inverted/confusing token names.

Example:

```text
--background
--surface
--surface-raised
--text-primary
--text-secondary
--accent
--success
--warning
--danger
--border
```

Dark/light themes should map these semantics to appropriate values.

### Typography

Arabic-first. Choose a high-quality Arabic headline/brand font and a highly readable UI/body font.

Noto Kufi Arabic and IBM Plex Sans Arabic are valid starting references, not mandatory until tested in the actual UI.

---

## 24. File & Attachment Security

Attachment pipeline:

```text
Upload
↓
Size validation
↓
MIME/content validation
↓
Security / malware check where appropriate
↓
Private object storage
↓
Processing
```

Rules:
- Do not trust filename extensions.
- Use private storage.
- Avoid permanent public URLs.
- Use short-lived signed access when needed.
- Set file-size/type limits.
- Allow attachment deletion independently when business semantics allow it.
- Define retention of raw originals.

---

## 25. Privacy & Data Safety

MADAR is private by default.

Do not request/store in V1 unless explicitly required by a future feature:
- banking passwords
- OTP codes
- government portal passwords
- Nafath credentials
- payment card details
- continuous precise location history
- unnecessary National ID data

Users must have flows for:
- Export my data
- Delete an attachment
- Delete an object
- Delete my account

AI processing should minimize unnecessary personal context.

### Admin privacy

Admin Console does not casually browse private user attachments.

Any support-access workflow that exposes private user data must be:
- explicit
- least-privilege
- audited
- time-bounded where feasible

---

## 26. Security & Authentication

### Telegram

Authenticate every resource server-side.

### Mini App

Validate Telegram Mini App `initData` on the backend.

Never trust a frontend-supplied Telegram user ID as authorization proof.

### Authorization

Every object, attachment, event, task, reminder, and action enforces per-user ownership/authorization.

### Secrets

Store secrets in environment/secret management, never source code.

---

## 27. Idempotency

Prevent duplicate writes caused by:
- duplicate Telegram updates
- retried webhooks
- worker retries
- repeated AI execution
- repeated notification delivery jobs

Use appropriate keys such as:
- Telegram update ID
- capture fingerprint where useful
- action idempotency key
- reminder delivery key

Financially meaningful or externally visible writes must be especially strict.

---

## 28. Admin Console

Admin manages the system, not the user's life.

Core areas:

### Overview
- active users
- captures
- processing success/failure
- AI usage/cost
- notification health

### Processing
- queue health
- failed jobs
- safe retry

### AI
- model routing
- cost
- failure patterns
- schema validation failures

### Notifications
- sent
- failed
- retries

### Users
- account state
- plan
- non-sensitive activity summary

### Feature Flags
- experiments
- rollout control

### System
- workers
- database
- Redis
- storage
- health checks

---

## 29. Architecture & Stack

Build a **Modular Monolith** for V1.

Do not start with microservices.

Suggested structure:

```text
madar/
├── backend/
│   └── app/
│       ├── users/
│       ├── auth/
│       ├── telegram/
│       ├── inbox/
│       ├── ai/
│       ├── actions/
│       ├── objects/
│       ├── vehicles/
│       ├── documents/
│       ├── subscriptions/
│       ├── assets/
│       ├── events/
│       ├── tasks/
│       ├── appointments/
│       ├── reminders/
│       ├── notifications/
│       ├── attachments/
│       ├── search/
│       ├── billing/
│       ├── admin/
│       ├── localization/
│       └── system/
├── worker/
├── apps/
│   ├── mini-app/
│   └── admin-web/
├── migrations/
├── tests/
├── infra/
└── docs/
```

### Stack

Backend:
- Python 3.12+
- FastAPI
- aiogram
- SQLAlchemy
- Alembic

Data:
- PostgreSQL
- Redis

Storage:
- S3-compatible private object storage

Frontend:
- Next.js
- TypeScript
- Tailwind CSS
- RTL-first

Deployment:
- Docker Compose
- HTTPS
- Telegram webhook
- health checks
- structured logs

---

## 30. Core Tables

Expected starting entities:

```text
users
user_preferences

captures
capture_processing_jobs

actions

objects
object_links

vehicles
vehicle_readings        # projection/query support, not competing history

documents
subscriptions
assets

events

tasks
appointments

reminder_rules
reminder_occurrences
notification_deliveries

attachments

activity_log

ai_runs
ai_usage

billing_subscriptions   # commercial plan/account billing, not life plans
```

If future personal planning is added, use a clearly separate concept such as:

`life_plans`

Do not reuse ambiguous `user_plans` for both billing and personal goals.

---

## 31. Build Order

### Phase 1 — Foundation
- repository
- Docker
- PostgreSQL
- Redis
- migrations
- users/auth
- Telegram identity
- health checks
- structured logging

### Phase 2 — Capture Core
- Telegram ingestion
- captures
- text input
- idempotency
- activity/action infrastructure

### Phase 3 — Task Core
- tasks
- appointments
- Arabic date/time parsing
- reminder engine
- notifications
- Done
- Snooze
- Edit
- Undo/reversal

Build and test this first with deterministic/manual input paths.

### Phase 4 — Intelligence
- voice/transcription
- images
- PDFs
- AI Gateway
- structured outputs
- confidence × risk
- confirmations
- AI-proposed actions

### Phase 5 — Objects
- vehicles
- documents
- subscriptions
- assets
- unified events/timelines
- invoice routing

### Phase 6 — Mini App
- Mini App auth
- Home
- central control interaction
- Inbox
- My Things
- object timelines
- Calendar
- editing

### Phase 7 — Search & Ask Madar
- structured search
- natural-language retrieval
- Ask Madar

### Phase 8 — Admin
- monitoring
- failures
- AI cost
- feature flags

### Phase 9 — Beta Hardening
- security review
- backup/restore
- observability
- rate limits
- performance
- recovery paths
- automated test expansion

### Phase 10 — Phase 2 Intelligence
Only after V1 reliability:
- "مدار يلاحظ"
- richer trends
- optional weekly narrative digest improvements

---

## 32. Minimum Test Coverage

At minimum test:
- relative Arabic dates
- user timezone
- ambiguous date confirmation
- Hijri/Gregorian display conversion where enabled
- vehicle matching
- odometer source-of-truth behavior
- mileage reminder math
- mixed mileage/date maintenance rules
- one-active-occurrence invariant
- Snooze
- task Done
- maintenance "تم التغيير" semantics
- Telegram update idempotency
- action idempotency
- worker retries
- per-user authorization
- attachment access control
- document renewal history
- subscription renewal history
- event correction/reversal
- AI schema validation
- invoice routing branches
- money precision/currency
- failed job retry
- account deletion
- data export

---

## 33. Reference Scenarios

### A — Vehicle voice capture

User:

> "غيرت زيت اليارس اليوم على 53420 والزيت يمشي عشرة آلاف."

Expected:

```text
Voice Capture
→ Transcription
→ Structured Extraction
→ Match Vehicle
→ Validate
→ Execute Action
→ oil_change Event
→ odometer_reading Event
→ Update vehicle reading projection/current state
→ Mileage Reminder Rule at 63,420 km
→ Reply
→ Timeline visible immediately
```

If no Yaris exists, propose creating/matching the vehicle rather than silently inventing one.

If prior comparable history exists, contextual comparison is optional and concise.

### B — Invoice photo

Photo of TV receipt:

```text
Image Capture
→ Extract merchant/date/product/amount/warranty
→ High confidence: propose Asset
OR
→ Ambiguous: three-button classification
→ Create/Link Asset as appropriate
→ Attach receipt privately
→ Purchase/expense Event
→ Warranty rule if supported
→ Asset timeline
```

No dedicated invoices section.

### C — Natural task

> "ذكرني بكرة الساعة 8 أروح الصيدلية."

Expected:

```text
Text Capture
→ Resolve user-local tomorrow 08:00
→ Create Task
→ Create Reminder Rule / next Occurrence
→ Reply with absolute-enough confirmation
→ Edit / Undo available
```

### D — Document image

User sends insurance/document image:

```text
Image Capture
→ Detect document
→ Extract expiry
→ Confidence × Risk
→ Confirm only when needed
→ Create/Link Document
→ Reminder Rule
→ Attachment
→ Timeline
```

### E — Subscription

> "شاهد يتجدد يوم 15 كل شهر بـ65 ريال."

Expected:

```text
Capture
→ Subscription object
→ 65 SAR stored precisely
→ Monthly renewal rule
→ Next occurrence
→ Monthly upcoming total updated
```

---

## 34. UX Design Work Order

**Do not generate production code yet.**

First deliver:

1. Final Information Architecture
2. Navigation recommendation
3. Central-circle interaction model
4. Directional drag/swipe discovery strategy
5. Core user flows
6. Design System direction
7. First primary screen architecture
8. UX risks and fixes

### First screen group

Design first:
1. Welcome
2. Onboarding
3. Home
4. Central MADAR control
5. Voice capture
6. Quick text/photo capture
7. Processing
8. AI confirmation/classification
9. Saved success/Undo
10. Inbox

Do not immediately design every remaining screen before this interaction model is coherent.

### Second screen group

After approval:
- Calendar
- My Things
- Vehicle
- Vehicle timeline
- Mileage update
- Document
- Subscription
- Asset/warranty
- Reminder detail

### Third screen group

Then:
- Search
- Ask Madar
- Global history/activity where useful
- Notification preferences
- Profile
- Privacy
- Export
- Billing/Plus
- Delete account
- Recovery/error states

Admin UX comes after the consumer experience is stable.

---

## 35. Product Acceptance Questions

Before approving a design or feature, ask:

- Can a new Saudi user understand the product without a tutorial?
- Can they add something naturally within seconds?
- Is voice capture obvious?
- Is the central control useful rather than decorative?
- Are directional gestures discoverable?
- Does MADAR ask fewer questions than a normal productivity app?
- Are AI mistakes easy to correct?
- Does the user know why they received a reminder?
- Does vehicle maintenance behave correctly for mileage?
- Is history preserved rather than overwritten?
- Is the interface calm and one-handed?
- Does the product still feel like "بس أرسلها لمدار"?

If not, simplify.

---

## 36. Governance

Maintain one authoritative product specification.

Every major decision must be classified as:
- **DECIDED**
- **PROPOSED**
- **DEFERRED**
- **OUT OF SCOPE**

Do not silently expand V1.

When a new idea appears, ask whether it strengthens the core promise or merely adds another section.

---

# 37. Decision Register

## DECIDED — Product

- MADAR is a personal life companion, not a generic AI chatbot.
- Primary promise: **"بس أرسلها لمدار."**
- Telegram Bot + Mini App are the initial platform.
- Natural capture is preferred over category-first forms.
- Capture is the first-class ingestion object.
- Core V1 objects: Vehicles, Documents, Subscriptions, Assets.
- Tasks and Appointments exist internally but do not require standalone top-level navigation.
- Inbox is a first-class product area.
- Ask Madar queries the user's own MADAR data.
- History/timelines are core product value.
- Contextual comparisons are optional, not mandatory on every confirmation.
- "مدار يلاحظ" is not required for V1.
- Expenses are a side effect, not a budgeting module.
- No standalone Invoices navigation.

## DECIDED — UX

- Central circular MADAR control is the primary interaction identity.
- Tap defaults to voice capture.
- Directional drag/swipe will be designed and tested, especially for RTL.
- Essential features cannot exist only as hidden gestures.
- Central control may shrink/dock on detail-heavy screens.
- Visual design should be calm, premium, Arabic-first, and non-gimmicky.
- Exact palette/font choices remain subject to visual/accessibility testing.

## DECIDED — Architecture

- Modular monolith for V1.
- PostgreSQL + Redis + private object storage.
- AI never writes directly to domain tables.
- Unified business `actions` layer supports AI, user, system, and admin sources.
- Unified append-oriented `events` history with explicit corrections/reversals.
- `user_id` is required on events; `object_id` can be nullable.
- Do not duplicate `object_type` into events by default.
- Version schemas for events/actions/AI structured outputs.
- Odometer events are historical truth; `vehicle_readings` may be a projection.
- Reminder engine uses Rule → Occurrence → Delivery.
- V1 keeps at most one active future/current occurrence per reminder rule.
- Money uses precise numeric representation + currency, never float.
- Telegram Mini App `initData` is validated server-side.
- Idempotency is mandatory for externally repeated/retried operations.

## DEFERRED

- Family shared workspace
- Business mode
- Native iOS/Android apps
- Advanced personal plans/project planning
- "مدار يلاحظ" analytics layer
- Rich weekly intelligence
- Advanced financial analysis
- Government integrations
- Banking integrations
- Semantic/vector retrieval where structured search is sufficient

## OUT OF SCOPE V1

- Generic AI chat
- Accounting
- Budgeting
- CRM
- Social features
- Habit gamification
- Marketplace
- Team project management
- Continuous precise location tracking
- Government login/Nafath automation
- Banking credentials/OTP storage
- Native mobile apps

---

# 38. Final Instruction for Work

Start with **product and UX architecture only**.

Do not produce production code until the interaction model and first design direction are reviewed.

The first output must include:

1. Information Architecture
2. Recommended navigation
3. Central-circle behavior
4. Directional gesture model and RTL reasoning
5. Five primary end-to-end user flows
6. Design-system direction
7. First-screen wireframe/visual direction
8. Identified usability risks
9. Any recommended change only if it materially simplifies or improves MADAR

The test for every proposal is simple:

**Can a Saudi user send something naturally, see that MADAR understood it, trust that it was saved correctly, and rely on MADAR to bring it back when needed?**

If yes, the direction is correct.
