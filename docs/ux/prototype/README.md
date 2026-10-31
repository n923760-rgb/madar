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
