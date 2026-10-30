# MADAR UX Decision Log

Date: 2026-10-12
Status: Documentation checkpoint. Proposals are not approved behavior.

| ID | Status | Decision or question | Source / next action |
|---|---|---|---|
| UX-001 | BASELINE | The central circle is the dominant Home control; tap starts voice. | Product v2.1 §6; UX v1 §5 |
| UX-002 | BASELINE / TEST REQUIRED | Directions: up Calendar, right My Things, left Inbox, down Ask MADAR. Visible tap alternatives are required. | UX v1 §4; validate RTL semantics in a prototype |
| UX-003 | PROPOSED | Replace the internal compact floating circle with a bottom capture composer: microphone at inline-start (right in RTL), text in the center, attachment at inline-end. | Owner raised placement concern; review recommendation. Validate against keyboard, safe areas, and screen actions. |
| UX-004 | CONFLICT RESOLUTION / BASELINE | At most one active future/current stored occurrence per reminder rule in V1. Compute future calendar previews on demand. | Product v2.1 §18 overrides UX v1 §12.2 multiple-future-occurrences text. Record an approved amendment before replacing the original UX document. |
| UX-005 | BASELINE | Clarify only uncertain or high-risk fields. Clear, low-risk captures may save after deterministic validation and offer Undo. | Product v2.1 §4/§7; UX v1 §10.3. Do not impose confirmation on every capture. |
| UX-006 | BASELINE | Maintenance completion uses explicit wording such as «تم التغيير» or «تمت الصيانة». Generic notification dismissal does not record maintenance. | Product v2.1 §13; qualify generic UX v1 notification copy by context. |
| UX-007 | OPEN | Exact circle diameter, tap destination placement, and right/left drag behavior. | Measure at 320/360/390/430px and test with first-time Arabic users. |
| UX-008 | OPEN | Live transcription availability and privacy/retention choices. | Use simulated text in design; provider/runtime capability remains unqualified. |
| ENG-001 | PENDING | Adopt central engineering governance at a selected approved version. | Repository creation and public visibility do not qualify adoption. |

## Change control

Every accepted change records the owner decision, affected document section, and resulting behavior. Do not rename proposals as DECIDED merely because a new conversation begins or the owner asks to continue unrelated work.

## 2026-10-28 — v0.2 visual review

- UX-009 — PROPOSED: semantic dark/light palette and embedded Noto Kufi/Noto Sans Arabic, specified in [Design System v0.2](DESIGN_SYSTEM-v0.2.md). The font substitution and exact values await visual approval.
- UX-010 — PROPOSED: persistent labeled direction buttons on Home and one header destination menu internally; remove repeated internal bottom navigation. No new product area is introduced.
- UX-003 — STILL PROPOSED: default bottom composer implemented for comparison. The owner's current instruction authorizes improvement/prototyping, not automatic final design approval.
- UX-007 — TESTED PARTIALLY: 136px circle candidate; 40 browser layout cases passed after calendar target repair. Physical first-time user direction testing remains open.
- Preserve UX-004 one-active-occurrence invariant, UX-005 confidence-based clarification, and UX-006 explicit maintenance completion wording. No backend implementation or central governance adoption is implied.
- Reference attribution: latest retrievable conversation description plus UX v1 §17; original selected raster unavailable. See [dated review](../../ENGINEERING/REPORTS/DESIGN-REVIEW-2026-10-28.md).

## 2026-10-29 — v0.3 visual refinement

UX-011 — PROPOSED: quieter broken orbit arcs, 144px inset-ring Home circle with MADAR wordmark, start-aligned greeting, outlined summary cards, capture pills, segmented filters and inset composer. Requested as a refinement of the current design, not approval of final dimensions or prior proposals. Four directions, tap alternatives, synthetic fixtures, original product/UX references and palette values are preserved. Both Node suites and 40 Chromium shell layout/target cases PASS; physical device and user validation remain pending. Review in the same unmerged PR #3.

## 2026-10-30 — UX-012 DECIDED by owner: hold to record

The owner explicitly replaces Home tap-to-start/tap-to-stop with press-and-hold recording and release-to-submit. Prototype candidate threshold: 350ms. Movement >24px before activation cancels the hold timer and permits the existing four physical directions. After recording starts, upward drag ≥90px arms cancellation; release cancels. Return to the circle before release resumes the send intention. OS pointer cancellation, lost capture, tab hiding, blur and navigation cancel without submission. Short taps show guidance. Space/Enter hold/release is supported; explicit start/stop/send controls remain an accessible alternative. This supersedes tap-default on Home in UX-001 and original reference §§6/5.2; original reference bytes stay unchanged. Internal capture controls remain explicit in this round.

Release means end capture and submit for processing, not a claim of successful domain save. The selected synthetic fixture proceeds through the existing confidence/clarification pipeline. No microphone, actual audio storage, AI or notification service is introduced. Real phone touch and first-user validation remain pending.

## 2026-10-30 — UX-013: configurable circle shortcuts

Owner requests the circle as a useful central hub: each physical direction may open the user's chosen menu, while hold/release captures speech for tasks, reminders and appointments. DECIDED: expose four configurable destinations with visible matching tap labels; keep UX-012 hold/release and original direction defaults. Candidate destinations in the prototype are Calendar, My Things, Inbox, Ask, Text, Attachment, Vehicle Timeline and Settings. Exact placement/options remain proposed; changing shortcuts must not repurpose recording after hold begins. Preferences are session-only in the prototype, with Reset Defaults.

Added bounded Task and Appointment speech fixtures alongside Reminder. A task without a date creates no invented timed reminder; a dated appointment displays its explicit date/time. Processing and saving remain synthetic, with a manual “show simulated result” control and explicit no-real-AI copy. Browser tests: changing Up to Text changed both label and actual physical swipe destination; mouse hold→Task→result passed. Node tests cover customization/reset, task/appointment View+Undo and hold/direction regressions. Real audio interpretation and device testing remain pending.

## 2026-10-30 — UX-014 DECIDED: owner accepts current design baseline

Owner instruction: "تمام ادمج و اعتمد", following the current prototype review and confirmation of the roadmap and root AGENTS.md. Accept the present prototype as the design baseline: UX-003 internal composer; UX-009 semantic dark/light system and embedded Arabic font substitution; UX-010 visible direction alternatives and internal navigation; UX-011 current visual refinement; UX-012 hold/release; UX-013 configurable four-direction shortcuts and their current Settings placement. UX-007 current dimensions/navigation are accepted for the baseline, with device and first-time usability qualification still pending. Earlier PROPOSED statements describe historical checkpoints and are superseded for these current candidates only.

The instruction authorizes merging stacked PR #3 into PR #2 and then main, and accepts the existing project AGENTS.md/reference organization. It does not authorize an unspecified central-governance adoption (ENG-001 remains PENDING), production deployment, new backend work or a claim of real audio/AI/reminder delivery. Original Product Master v2.1 and UX Architecture bytes remain preserved; use this dated amendment for current behavior. Test results and NOT RUN cases remain unchanged by approval.
