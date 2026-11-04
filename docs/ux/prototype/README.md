# MADAR interactive design prototype v0.2

Open `index.html` in a modern browser, or use the owner-only [interactive preview](https://madar-design-review-oct28.n923760.chatgpt.site). On mobile, scroll below the app for review tools; appearance is also reachable in the app's destination menu → Settings. All examples are synthetic and memory-only. Reload resets them. No microphone, AI, upload, persistence or notifications are active.

Home uses hold-to-record/release-to-submit and four configurable physical drag directions, with defaults: up Calendar, right My Things, left Inbox, down Ask. Each destination has a visible tap alternative. The header brand returns Home; the menu opens destinations/settings. RTL Back and browser Back return to the previous route.

The review panel controls shell width, dark/light mode, six capture fixtures, screen selection and dock/Compact comparison. My Things has search/type filters. Calendar supports day/week/month, month traversal and day selection against a fixed 28 October 2026 review date. Unknown Ask queries return a no-result state. Text drafts survive in-session navigation.

## Review paths

1. Reminder fixture → Home circle hold/release → Processing → show simulated result → Saved → Undo (explicit Voice controls remain an alternative).
2. Oil fixture → voice → processing → valid mileage → saved → vehicle timeline.
3. Document fixture → PDF → send → complete → reminder timing → saved.
4. Invoice fixture → photo → send → complete → appliance → saved.
5. Ask → oil question → source → correct → save → Undo.
6. Inbox → failed item → offline simulation → retry blocked → restore connection → retry.
7. Home circle → each physical direction; short/diagonal/cancelled drag must not start voice. Repeat by visible buttons and keyboard.

## Checks

```sh
node docs/ux/prototype/checks/flows.cjs
node docs/ux/prototype/checks/design.cjs
```

These are Node logic checks, not device qualification. See the [dated report](../../../ENGINEERING/REPORTS/DESIGN-REVIEW-2026-10-28.md) for actual browser results and NOT RUN cases. [Design System](../DESIGN_SYSTEM-v0.2.md) documents tokens/components/interactions. Font subsets and license text are embedded to keep the preview self-contained.

The owner accepted this current design baseline on 2026-10-30 (UX-014), including the internal composer, palette, font substitution, circle and shortcuts. Earlier proposed/review-pending statements below are historical checkpoints. Product/UX reference bytes are unchanged. Device qualification remains pending; this design acceptance does not implement production audio, AI, storage or reminders.

## Visual refinement v0.3 — 2026-10-29

The owner requested a more beautiful version of the current design. This pass keeps product behavior and palette values while refining the Home orbit into quiet broken arcs, a 144px inset-ring circle, asymmetric Arabic greeting, outlined summary cards, softer capture pills, segmented filters, and an inset internal composer. No idle decorative animation is added. Prototype fixture dates remain fixed at 28 October for regression consistency.

Executed: both Node suites PASS; Chromium shell matrix 5 views × 4 widths × 2 appearances PASS with no horizontal overflow or buttons below 44×44px, including the footer. Real mobile, screen readers, 200% text, keyboard and user study remain NOT RUN. The visual result remains proposed for owner review.

## Home hold-to-record — 2026-10-30

Hold Home's circle for 350ms to begin the simulated voice capture. Release submits directly to Processing, without Stop/Send taps. Before activation, a quick directional swipe still navigates. During recording, slide up 90px and release to cancel; move back before release to submit. A short tap explains the gesture. Keyboard users may hold/release Space or Enter; screen-reader activation and the disclosed alternative open explicit recording controls. Interruptions cancel safely. All audio remains simulated. Owner approval of this behavior is UX-012; real device qualification remains pending.

Validation: both Node suites PASS; Chromium mouse hold/release and Space hold/release reached Processing without a second action. Short pointer click stayed Home with guidance. Node checks cover release-once, all four fast directions, slide cancellation/return, short tap, cancellation and actual bound Home handler. Mobile touch, screen reader and real audio remain NOT RUN.

## Central hub refinement — 2026-10-30

Destination menu → Settings → Circle Shortcuts lets the reviewer assign each direction to a real prototype view, then return Home. Labels and physical swipes use the same mapping. Reset restores Up Calendar, Right Things, Left Inbox, Down Ask. The circle follows the finger slightly as directional feedback before recording starts.

The scenario selector now includes Task (no assumed deadline) and Appointment (explicit date/time), in addition to Reminder. Hold/release submits the fixture to Processing; “show simulated analysis result” completes the design demonstration. It does not analyze actual speech or arbitrary text. Result cards expose kind, details, View and Undo. Both Node suites PASS; browser custom-upward-swipe and held Task fixture PASS. Real phone touch and AI interpretation NOT RUN.

## Interruption qualification — 2026-10-31

The candidate fix cancels pending or active capture when pointer capture or keyboard focus is lost, isolates the primary pointer, and consumes Escape during a hold before global Back. Small pre-hold drift recenters when listening starts. The approved 350ms hold, four directions, release-to-process and explicit capture alternative are preserved.

Both Node suites and 40 Chromium shell layouts PASS; native mouse/Space release, Space+Tab cancellation and Space+Escape local cancellation PASS. Lost capture, focus loss during recording and secondary-pointer cases are additionally covered by the Node binding tests. Physical mobile, screen readers, 200% text and real audio remain NOT RUN. See [qualification report](../../../ENGINEERING/REPORTS/INTERACTION-QUALIFICATION-2026-10-31.md) for the device script and exact limits.

## Capture state journeys — 2026-11-01

Two additional **synthetic** scenarios are selectable in the review panel below/beside the phone:

1. **تذكير — سؤال عن الوقت**: Try flow → Stop/Send (or hold/release on Home) → Show simulated analysis → choose a time for 5 November 2026 in Riyadh → confirm time → Simulate storage response. The time starts empty; there is no inferred default. The original source and clarification stay separate. Nothing appears as a saved record before the simulated receipt.
2. **حفظ — انقطع الرد**: select this scenario, then choose the review-only response mode. After simulated analysis, use Simulate storage response. The default loses the reply **after** the mock action: status stays unknown until Check result reconciles the same operation. The alternatives lose it **before** the action or leave it unsent offline. Unknown outcomes cannot be blindly retried. After reconciliation finds no action, retry reuses the capture; acknowledgement does not create a second action.

Pending captures reopen through Inbox/Home attention. A confirmed record appears in Calendar's explicitly unfiltered recent-capture section and as a source-backed entry point in Ask. Tasks do not create My Things objects. Undo references the selected action and preserves original/clarification sources plus a reversal trace; it leaves later captures alone. No permanent navigation area is added. Existing fixture journeys and approved circle interactions are preserved.

The response selector and manual completion buttons are **review controls**, not a required confirmation workflow for the product. The in-page ledger is separate from the Python experiment in PRs #6/#7; there is no live adapter between them. All data disappears on reload. Arbitrary text is not classified; no network request, provider, microphone, durable storage or actual notification exists.

Run the added suite:

```sh
node --test docs/ux/prototype/checks/capture.cjs
node docs/ux/prototype/checks/flows.cjs
node docs/ux/prototype/checks/design.cjs
```

Validation checkpoint: 12 added Node tests PASS, existing flow/design suites PASS, semantic palette text/control contrast and original reference hashes PASS, `git diff --check` PASS. Chromium interaction checks PASS: missing-time question, empty-time inline error, explicit 18:30 answer, separate source/answer, lost response after mock commit, offline reconciliation refusal and successful same-operation reconciliation. 56 phone-shell cases PASS (Home, Inbox, My Things, Calendar, Ask, new saved status and new source × 320/360/390/430 × dark/light), no horizontal overflow or visible controls below 44px within the measurement tolerance (43px). These are desktop Chromium shell sizes, not real device viewports. Model accuracy, real networking/storage/auth, mobile touch/Telegram WebView, screen readers, 200% text and notification delivery remain NOT RUN. Semantic palette checks do not qualify every rendered state or focus announcement.

### Draft and navigation repair — 2026-11-01

The time input now keeps an unsubmitted draft per capture while navigating within the page; it does not append evidence, increment the source revision or create a receipt until explicitly confirmed. A second capture starts empty. Enter confirms a valid explicit time; errors mark the input with `aria-invalid` and reference its help/error text.

History entries now bind route and selected capture, including two captures opened on the same route. Back/Forward restore that context; a new branch of navigation discards forward entries. This repairs source/detail mixing caused by a single global selection. Browser history contains only local route/index/capture references, never source text.

Current checks: 16 capture tests PASS (12 existing + 4 regressions); existing flow/design suites and reference/palette checks PASS; `git diff --check` PASS. Chromium interaction checks PASS: retained 18:45 draft after Inbox, second capture empty, native Back to capture-2, Forward to capture-1 with its draft, and Enter to Committing. Physical phone/Telegram, actual virtual keyboard, screen reader announcements and 200% text remain NOT RUN. The 56-case layout checkpoint above is historical and was not repeated for this logic-only repair. No real persistence, authentication or backend integration is introduced.

### Automated checks

`.github/workflows/prototype-checks.yml` runs the three Node suites on pull requests, pushes to main/the current design branch, and manual dispatch. It uses Node 24, commit-pinned official checkout/setup actions, read-only repository permission, no retained checkout credentials, a five-minute timeout and cancellation of superseded runs. It installs no project packages and has no deployment or provider step. It uses `pull_request`, never `pull_request_target`.

A green run means synthetic behavior, palette assertions and original-reference hashes passed; it does not qualify browser layout, assistive technology, physical mobile, AI, authentication, durable storage or delivery. Check the actual GitHub run before reporting CI as PASS. Local execution and workflow YAML parsing alone do not prove hosted execution. Required-check branch protection is not configured by this file.

### Optional invoice association — 2026-11-02

Choose the Invoice scenario, process the synthetic attachment, then choose **حفظ الفاتورة فقط** or **ربط بالغسالة الموجودة**. Both use the same committing/receipt/reconciliation/source/reversal ledger as the new capture journeys. Source-only does not create an asset, warranty, expiry or reminder. Explicit association targets the existing washer; its related-invoice entry appears only after the mock receipt and disappears on targeted reversal. Invoices stay outside Calendar, remain reachable in Inbox and through Ask's last-confirmed-capture entry point, and preserve their source. Duplicate-review state cannot bypass into this path. This is not an expense extraction/accounting implementation or a new-device creation flow.

19 capture tests PASS (16 existing + 3 invoice cases), existing flow/design suites and reference checks PASS. Chromium source-only receipt/source, explicit existing-asset link and reversal PASS; 12 shell checks (invoice clarification/status/source × 320/390 × dark/light) PASS without horizontal overflow or undersized buttons at the existing tolerance. These are desktop shell checks, not phone qualification. No real upload/OCR/provider/private-file storage, production backend or notification execution is introduced; all records remain page-memory synthetic data. Device/Telegram/screen-reader checks remain NOT RUN.


## Text scaling and keyboard focus — 2026-11-04

Typography uses rem units at the unchanged 16px reference size. The review panel offers 100/150/200% root text scaling. At large text on a narrow phone container, the circle remains first, followed by four labeled shortcut buttons in reading order; physical swipe mappings do not change. Every destination still has a tap alternative. Calendar cells retain at least 44px width, disclosure summaries have 44px minimum height, and the screen uses a thin scrollbar.

For keyboard review, open Calendar and press Enter on a day: the selected day keeps focus. Repeat with Inbox filters. Changing destination (or selecting a different capture on the same route) focuses the named main region at its start. Same-context refresh retains scroll and the corresponding control if it still exists; a removed control falls back to the main region.

Chromium phone-shell matrix PASS: five primary views × 320/360/390/430px × 100/200% text × dark/light = 80 cases, no horizontal screen/phone overflow, visible controls at least 44×44 CSS px. Native Enter on a day and an Inbox filter retained focus; the destination menu focused the named main region. This is desktop Chromium shell testing, not physical mobile, screen-reader, OS text-size or browser zoom qualification. 150% is available for manual review but is not part of the recorded matrix.

23 capture/state/focus Node tests PASS (19 existing + 4 focus-policy checks); flow/design/reference suites PASS. The new calendar focus regression fails on the unmodified main baseline and passes after repair. Detailed evidence and device follow-up: ENGINEERING/REPORTS/ACCESSIBILITY-REVIEW-2026-11-04.md. No new production behavior is implemented.
