# MADAR Master Roadmap

Checkpoint: 2026-10-14. Current phase: **UX/UI design only**.
Status: DOCUMENTATION FOUNDATION — PR #1 open; not merged to main.

## Verified source checkpoint

Repository: https://github.com/n923760-rgb/madar — public.
Official main before this task: `13b68ea2a065821a0d767de6f3c3a52d39175af9`.
Original documentation import: `21ad88e0e2432307d455b8ad80c9254284d507d4` on `docs/product-design-foundation`.
Organization changes are tracked by [PR #1](https://github.com/n923760-rgb/madar/pull/1); use its live head for the latest task source. The SHAs above are historical checkpoints, not a claim that main contains this packet.

## Phase status

| Phase | Verified progress | Remaining gate |
|---|---|---|
| Product specification | Product Master v2.1 imported unchanged | Preserve approved baseline; record amendments |
| UX architecture | UX v1 imported unchanged; conflicts recorded | Resolve open details and document decision attribution |
| First ten screen brief | Draft composition and journeys written | Render and connect screens |
| Wireframes/prototype | NOT VERIFIED | Ten primary screens + supporting views + five journeys |
| UI approval | NOT VERIFIED | Owner review and open decisions resolved |
| Usability/accessibility | NOT RUN | Recorded Arabic/RTL task results and device checks |
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

## Exact next round

Render the first ten wireframes and Calendar/My Things/Timeline/Ask/Settings supporting views needed for the five journeys. Use synthetic data. Compare the proposed internal bottom composer with Compact Mode, while preserving the central circle on Home. Record visual decisions in the Decision Log.

Then build a clickable design prototype, inspect 320/360/390/430px, keyboard/safe-area and reduced-motion cases, and run a first-time Arabic usability round. A design brief alone is not a rendered or tested prototype.

## Open decisions

- UX-003: internal voice composer location and appearance.
- UX-007: circle diameter, visible navigation, RTL direction testing.
- UX-008: live transcription capability and privacy/retention choices.
- ENG-001: selected central governance adoption version.

Preserve the v2.1 one-active-occurrence invariant and confidence/risk policy pending explicit owner amendments.

## Update rules

This is the only roadmap. Update phase status from actual artifacts or owner decisions. Detailed reports retain their dated checkpoint; link them here. Never promote planned tests or source inspection into runtime qualification.
