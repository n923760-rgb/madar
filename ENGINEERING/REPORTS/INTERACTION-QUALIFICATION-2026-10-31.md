# MADAR interaction qualification — 2026-10-31

Base: official main `8b3b5daef3a53f4578082c3531899c00c27c9c9b`. Owner-approved design: UX-014. Branch: `design/interaction-qualification-v0.4`. Design prototype only; all sources, captures and saves are synthetic, session-only. Original Product v2.1 and UX v1 references are unchanged. Central governance adoption remains PENDING.

## Findings and repair

| Trigger | Previous behavior | Candidate behavior |
|---|---|---|
| Pointer capture lost before 350ms | Pending timer could activate recording after input loss; reproduced by a failing regression | Cancel pending and active gestures, clear input ownership |
| Tab/focus loss during keyboard hold | Only window blur was handled; a late keyup could submit | Cancel at orb blur; late keyup does not submit |
| Escape during a hold | Local cancellation bubbled to the global Back handler | Cancel locally and stop propagation; idle Escape retains Back |
| Secondary pointer move/up | Could control a gesture despite its down event being ignored | Only the initiating pointer can move, finish or cancel it |
| Small movement before hold activates | Circle could remain slightly displaced | Listening starts centered |

The fixes preserve 350ms activation, four customizable directions and visible button alternatives, release submission, slide-to-cancel and the explicit voice-control alternative. No new visual system or product area is introduced.

## Executed evidence

- `node docs/ux/prototype/checks/flows.cjs`: PASS; existing fixture journeys and actual Home bindings, plus new input-loss regressions. Added lost-capture assertion failed on the baseline before the repair (`true !== false`). Node VM/DOM stubs do not qualify browser event ordering or real devices.
- `node docs/ux/prototype/checks/design.cjs`: PASS; filters/calendar/drafts, semantic text contrast (dark minimum 7.17:1, light 5.34:1), and exact original Product/UX SHA-256 integrity.
- `git diff --check`: PASS.
- Chromium native held mouse 650ms/release: Processing. Held Space 650ms/release: Processing. Space+Tab chord: Home idle with focus on Text. Space+Escape chord: Home with cancellation message, despite a previous route in history. These chords exercise interruption before activation; active-recording focus loss is covered in Node only.
- Chromium shell matrix: Home, Inbox, My Things, Calendar and Ask × 320/360/390/430px × dark/light = 40 cases. Screen `scrollWidth <= clientWidth + 1`; visible screen/footer buttons >=44×44 CSS px. PASS. This is constrained shell sizing in a desktop viewport, not device emulation or system text scaling.

## NOT RUN

Actual Huawei/iOS touch and multi-touch; OS lost-pointer event sequencing; Telegram keyboard/safe areas; folded/unfolded and landscape runtime; 200% text; screen reader and Reduced Motion runtime; first-time-user study. No real recording, microphone permissions, upload, transcription, AI, durable storage or reminder delivery is implemented or tested.

## Physical device script — ready to execute, no results claimed

Use the private preview on Mate X6 folded, unfolded, and within Telegram when a test Mini App exists. Repeat key tasks in both appearances. Record device/browser/Telegram versions, orientation, system text size, result, accidental route/submission count and a screenshot only with synthetic data.

| Task | Expected result |
|---|---|
| Brief tap the circle | Guidance only; no Processing |
| Hold, speak the example, release | One Processing transition; no second Stop/Send action |
| Four quick direction swipes | One configured destination; corresponding visible button opens the same view |
| Hold, slide upward to cancellation, release | Home idle; no submission |
| Hold then background the app or interrupt touch | Idle on return; no delayed start or submission |
| Keyboard/Switch Access: hold then move focus, or Escape | Cancel; no late submission or unintended Back |
| Text input with keyboard, Back and large text | Input remains reachable; Back and composer remain usable; no overlap/clipping |

Use real first-time Arabic users for discoverability. UX v1 targets remain 80% direction understanding, 90% category-free capture, and 90% failed-item recovery; these are targets, not measured scores. Screen reader users must be able to complete capture with explicit controls.

## Proposed next implementation slice

After device findings, scope a local capture-to-save vertical slice: a versioned capture/action contract, deterministic validation, explicit idempotency and action-specific Undo, synthetic provider adapter, and read-only source retrieval. Test duplicate receipt, uncertain date/time and wrong-object prevention before adding a real provider. Authentication, durable personal data, microphone retention and production deployment require their explicit bounded design/engineering decisions. This report does not select a stack/provider or authorize production operations.
