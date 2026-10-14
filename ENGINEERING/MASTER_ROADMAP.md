# MADAR Master Roadmap

Checkpoint: 2026-10-14. Current phase: **UX/UI design only**.
Status: DOCUMENTATION FOUNDATION MERGED; prototype source prepared on a separate design branch.

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
| First ten screen brief | Draft composition + interactive HTML source | Visual inspection and owner review |
| Wireframes/prototype | Interactive source and logic checks complete; browser rendering NOT VERIFIED | Browser/device QA, gestures and five-journey usability review |
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

## Current design artifact and checks

[Prototype guide](../docs/ux/prototype/README.md) explains how to open [the self-contained HTML](../docs/ux/prototype/index.html) and review the proposed internal composer versus Compact Mode. Source includes ten primary screens and Calendar/My Things/Timeline/Ask/Settings supporting views, four capture scenarios, and sourced-answer/edit/undo interactions. All data is synthetic and browser-memory-only.

`node docs/ux/prototype/checks/flows.cjs` passed 20 screen-template renders and checks for low-risk direct save, uncertain mileage validation, correction undo, duplicate handling, offline retry, sourced answers, text escaping and Back. This is logic-only with a DOM stub. It does not qualify browser rendering, pointer gestures, accessibility, real devices, keyboards, AI or persistence.

## Exact next round

Open the prototype in a supported browser QA environment. Inspect 320/360/390/430px, short/tall viewports, keyboard and Telegram safe areas, 200% text, contrast, focus/Back, reduced motion and direction cancellation. Load the approved Arabic fonts before visual sign-off; this offline draft uses installed font fallbacks. Run all five journeys with first-time Arabic users and record actual results. Review UX-003 and UX-007 without silently approving proposals. Production work remains gated by explicit design approval.

## Open decisions

- UX-003: internal voice composer location and appearance.
- UX-007: circle diameter, visible navigation, RTL direction testing.
- UX-008: live transcription capability and privacy/retention choices.
- ENG-001: selected central governance adoption version.

Preserve the v2.1 one-active-occurrence invariant and confidence/risk policy pending explicit owner amendments.

## Update rules

This is the only roadmap. Update phase status from actual artifacts or owner decisions. Detailed reports retain their dated checkpoint; link them here. Never promote planned tests or source inspection into runtime qualification.
