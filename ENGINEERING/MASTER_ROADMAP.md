# MADAR Master Roadmap

Checkpoint: 2026-10-28. Current phase: **UX/UI design only**.
Status: v0.2 PUBLISHED FOR REVIEW in [draft PR #3](https://github.com/n923760-rgb/madar/pull/3); private static preview published; owner design approval pending.

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
| UI approval | NOT VERIFIED | Owner review and open decisions resolved |
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

Review draft PR #3 without merging. Owner reviews Home directions, dock versus Compact, palette and font substitution. Then qualify real mobile/Telegram keyboard, safe areas, foldable/short/landscape layouts, 200% text, reduced motion, screen readers and first-time Arabic user tasks. Original selected raster reference is not recovered; do not claim pixel fidelity. Production engineering remains blocked until explicit design approval.

## Open decisions

- UX-003: internal voice composer location and appearance.
- UX-007: circle diameter, visible navigation, RTL direction testing.
- UX-008: live transcription capability and privacy/retention choices.
- ENG-001: selected central governance adoption version.

Preserve the v2.1 one-active-occurrence invariant and confidence/risk policy pending explicit owner amendments.

## Update rules

This is the only roadmap. Update phase status from actual artifacts or owner decisions. Detailed reports retain their dated checkpoint; link them here. Never promote planned tests or source inspection into runtime qualification.

## 2026-10-30 interaction update

Owner-approved UX-012 replaces Home tap recording with hold/release submission. The prototype retains fast directional swipes and adds slide-up cancellation, interruption cancellation, keyboard hold/release and explicit-button accessibility fallback. Both Node suites PASS; Chromium held-pointer release and held-Space release reached Processing, and a short pointer tap remained Home with guidance. Cancellation/direction races are covered in Node controller tests. Actual mobile touch, audio permissions and production recording remain NOT RUN/outside this design simulation. Review in unmerged PR #3; details in Decision Log and prototype guide.
