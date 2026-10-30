# MADAR Master Roadmap

Checkpoint: 2026-10-30. Current phase: **Approved design baseline; production engineering not started**.
Status: OWNER APPROVED the current prototype and project instructions on 2026-10-30 ("تمام ادمج و اعتمد"). Merge authorized through stacked PR #3 → PR #2 → main. The private static preview remains a simulation.

## Verified source checkpoint

Repository: https://github.com/n923760-rgb/madar — public.
Official main after authorized PR #1 merge: `efb9e91a7f0fe858d60ad1394c1dfd9c1b487e19`.
Original documentation import: `21ad88e0e2432307d455b8ad80c9254284d507d4` on `docs/product-design-foundation`.
Organization was merged through [PR #1](https://github.com/n923760-rgb/madar/pull/1) on 2026-10-14. Prototype changes are on `design/interactive-prototype-v0.1`; use the live branch/PR head for exact source. This checkpoint does not imply prototype merge or design approval.

## Phase status

| Phase | Verified progress | Remaining gate |
|---|---|---|
| Product specification | Product Master v2.1 imported unchanged | Preserve approved baseline; record amendments |
| UX architecture | UX v1 imported unchanged; conflicts recorded | Resolve open details and document decision attribution |
| First ten screen brief | Interactive source retained; five primary views refined | Owner review |
| Wireframes/prototype | 40 browser layout cases and five simulated journeys checked | Physical device QA and visual approval |
| UI approval | Current prototype baseline APPROVED by owner, 2026-10-30 | Runtime/device qualification remains separate |
| Usability/accessibility | Token contrast, browser targets/layout PASS | User study, real devices, screen readers NOT RUN |
| AI evaluation set | NOT VERIFIED | Synthetic cases, expected outcomes, metrics and review |
| Central governance adoption | PENDING | Approved source/version and adoption evidence |
| Production engineering | NOT STARTED | Explicit design approval and bounded engineering task |

## Document ownership

- Product requirements: [Product Master](../docs/product/madar-complete-master-prompt-v2.1.md).
- Experience model: [UX Architecture](../docs/ux/MADAR-UX-Architecture-v1.md).
- Decisions/proposals: [Decision Log](../docs/ux/DECISION_LOG.md).
- Current design work: [First Ten Screens](../docs/ux/DESIGN_BRIEF-v0.1.md).
- Detailed dated findings: [Baseline report](REPORTS/BASELINE-2026-10-12.md).
- Reference integrity: [Manifest](../docs/references/SOURCE-MANIFEST.json).

## Current design artifact and checks

- [Private interactive prototype](https://madar-design-review-oct28.n923760.chatgpt.site), owner-only; synthetic data; no production MADAR services.
- [Prototype guide](../docs/ux/prototype/README.md), [Design System v0.2](../docs/ux/DESIGN_SYSTEM-v0.2.md), [dated review and exact test limits](REPORTS/DESIGN-REVIEW-2026-10-28.md).
- Remote `design/minimal-premium-v0.2` starts at PR #2 head `dcc37b80069797ffe90a216dad11c30160b702aa`. [Draft PR #3](https://github.com/n923760-rgb/madar/pull/3) targets PR #2's branch. Browser publication was authorized after connector 403; all 11 changed files matched local blob hashes. Neither PR is merged.
- `flows.cjs` and `design.cjs` PASS. Product/UX hashes unchanged. Browser matrix: 40 cases, no horizontal overflow or primary-screen buttons below 44px after repair. Five simulated fixture journeys exercised; final record-sharing adjustment checked in Node only.

## Exact next round

Complete the owner-authorized stacked merge of PR #3 into PR #2's branch, then PR #2 into main; use GitHub's merged state and merge commit for evidence. The current circle, configurable shortcuts, hold/release behavior, internal composer and dark/light visual system are the approved design baseline (UX-014). Qualify real mobile/Telegram keyboard, safe areas, foldable/short/landscape layouts, 200% text, reduced motion, screen readers and first-time Arabic user tasks. Original selected raster reference is not recovered; no pixel fidelity is claimed. Production implementation requires a bounded engineering task; no backend, live AI, microphone or production services are started by this merge.

## Open decisions

- UX-003: current internal composer accepted as baseline under UX-014; physical keyboard/safe-area qualification remains open.
- UX-007: current circle and visible navigation accepted as baseline under UX-014; physical device/first-user direction testing remains open.
- UX-008: live transcription capability and privacy/retention choices.
- ENG-001: selected central governance adoption version.

Preserve the v2.1 one-active-occurrence invariant and confidence/risk policy pending explicit owner amendments.

## Update rules

This is the only roadmap. Update phase status from actual artifacts or owner decisions. Detailed reports retain their dated checkpoint; link them here. Never promote planned tests or source inspection into runtime qualification.

## 2026-10-30 interaction update

Owner-approved UX-012 replaces Home tap recording with hold/release submission. The prototype retains fast directional swipes and adds slide-up cancellation, interruption cancellation, keyboard hold/release and explicit-button accessibility fallback. Both Node suites PASS; Chromium held-pointer release and held-Space release reached Processing, and a short pointer tap remained Home with guidance. Cancellation/direction races are covered in Node controller tests. Actual mobile touch, audio permissions and production recording remain NOT RUN/outside this design simulation. Review in unmerged PR #3; details in Decision Log and prototype guide.

## 2026-10-30 central hub refinement

Owner-directed configurable directions (UX-013) are available under Settings → Circle Shortcuts, with matching visible labels and Reset Defaults. Added Task and Appointment voice fixtures alongside Reminder; undated tasks do not invent a timed reminder. Node checks PASS; Chromium customized upward swipe opened Text and held Task capture produced the expected synthetic result. No real transcription/AI or persistence is claimed. See prototype README and Decision Log; review remains in unmerged PR #3.

## 2026-10-30 owner approval and merge authorization

The owner explicitly instructed "تمام ادمج و اعتمد" after reviewing the prototype and the repository reference/AGENTS status. This approves the current design baseline and project instructions and authorizes the dependency-ordered merge; it does not qualify unexecuted tests, activate real audio/AI/reminders, or select a central-governance version. Earlier dated review statements above are historical checkpoints. Both Node suites were rerun PASS against files matching remote PR #3 head `d8029c1d7f41311b9b91d85c1ba2e79f3793ead7`; reference integrity PASS. See UX-014 for the approval scope. GitHub PR merge metadata is authoritative for final integration status.
