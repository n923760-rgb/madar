# MADAR Master Roadmap

Checkpoint: 2026-10-31. Current phase: **Approved design baseline; production engineering not started**.
Status: OWNER APPROVED the current prototype and project instructions on 2026-10-30 ("تمام ادمج و اعتمد"). Integration is tracked through stacked PR #3 → PR #2 → main; GitHub merge metadata is authoritative. The private static preview remains a simulation.

## Verified source checkpoint

Repository: https://github.com/n923760-rgb/madar — public.
Official main verified on 2026-10-31 after approved PR #2/#3 integration: `8b3b5daef3a53f4578082c3531899c00c27c9c9b`.
Original documentation import: `21ad88e0e2432307d455b8ad80c9254284d507d4` on `docs/product-design-foundation`.
Organization was merged through PR #1 on 2026-10-14; design PR #3 merged into PR #2, then PR #2 merged into main on 2026-10-30. UX-014 records owner design approval. The new interruption qualification fixes are isolated on `design/interaction-qualification-v0.4`, pending PR review.

## Phase status

| Phase | Verified progress | Remaining gate |
|---|---|---|
| Product specification | Product Master v2.1 imported unchanged | Preserve approved baseline; record amendments |
| UX architecture | UX v1 imported unchanged; conflicts recorded | Resolve open details and document decision attribution |
| First ten screen brief | Interactive source retained; five primary views approved | Device qualification |
| Wireframes/prototype | Approved baseline; interruption fixes and 40 layout cases rechecked 2026-10-31 | Review new PR and physical device QA |
| UI approval | Current prototype baseline APPROVED by owner, 2026-10-30 | Runtime/device qualification remains separate |
| Usability/accessibility | Token contrast, browser targets/layout PASS | User study, real devices, screen readers NOT RUN |
| AI evaluation set | v2.2 synthetic contract set prepared: 46 expected-output cases and 17 invalid-proposal checks | Real provider/extraction evaluation NOT RUN |
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
- [PR #3](https://github.com/n923760-rgb/madar/pull/3) merged into PR #2's branch on 2026-10-30 at `1047cd97ad2852ec723cde3d67e04151e734c1e1`. [PR #2](https://github.com/n923760-rgb/madar/pull/2) carries the complete approved baseline into main; its GitHub merged state/merge commit is the integration evidence. Browser publication was authorized after connector 403; source/test files matched local Git blob hashes.
- `flows.cjs` and `design.cjs` PASS. Product/UX hashes unchanged. Browser matrix: 40 cases, no horizontal overflow or primary-screen buttons below 44px after repair. Five simulated fixture journeys exercised; final record-sharing adjustment checked in Node only.

## Exact next round

The current circle, configurable shortcuts, hold/release behavior, internal composer and dark/light visual system are the approved design baseline (UX-014). Qualify real mobile/Telegram keyboard, safe areas, foldable/short/landscape layouts, 200% text, reduced motion, screen readers and first-time Arabic user tasks. Original selected raster reference is not recovered; no pixel fidelity is claimed. Production implementation requires a bounded engineering task; no backend, live AI, microphone or production services are started by this merge.

## Open decisions

- v2.2 capture understanding: [owner direction, classification/storage rules, prompt and contract candidates](../docs/product/capture-v2.2/MASTER-ADDENDUM.md); review before provider integration.
- UX-003: current internal composer accepted as baseline under UX-014; physical keyboard/safe-area qualification remains open.
- UX-007: current circle and visible navigation accepted as baseline under UX-014; physical device/first-user direction testing remains open.
- UX-008: live transcription capability and privacy/retention choices.
- ENG-001: selected central governance adoption version.

Preserve the v2.1 one-active-occurrence invariant and confidence/risk policy pending explicit owner amendments.

## Update rules

This is the only roadmap. Update phase status from actual artifacts or owner decisions. Detailed reports retain their dated checkpoint; link them here. Never promote planned tests or source inspection into runtime qualification.

## 2026-10-30 interaction update

Owner-approved UX-012 replaces Home tap recording with hold/release submission. The prototype retains fast directional swipes and adds slide-up cancellation, interruption cancellation, keyboard hold/release and explicit-button accessibility fallback. Both Node suites PASS; Chromium held-pointer release and held-Space release reached Processing, and a short pointer tap remained Home with guidance. Cancellation/direction races are covered in Node controller tests. Actual mobile touch, audio permissions and production recording remain NOT RUN/outside this design simulation. Historical validation checkpoint before merge; details in Decision Log and prototype guide.

## 2026-10-30 central hub refinement

Owner-directed configurable directions (UX-013) are available under Settings → Circle Shortcuts, with matching visible labels and Reset Defaults. Added Task and Appointment voice fixtures alongside Reminder; undated tasks do not invent a timed reminder. Node checks PASS; Chromium customized upward swipe opened Text and held Task capture produced the expected synthetic result. No real transcription/AI or persistence is claimed. See prototype README and Decision Log; approval and integration are recorded below and in GitHub merge metadata.

## 2026-10-30 owner approval and merge authorization

The owner explicitly instructed "تمام ادمج و اعتمد" after reviewing the prototype and the repository reference/AGENTS status. This approves the current design baseline and project instructions and authorizes the dependency-ordered merge; it does not qualify unexecuted tests, activate real audio/AI/reminders, or select a central-governance version. Earlier dated review statements above are historical checkpoints. Both Node suites were rerun PASS against files matching remote PR #3 head `d8029c1d7f41311b9b91d85c1ba2e79f3793ead7`; reference integrity PASS. See UX-014 for the approval scope. GitHub PR merge metadata is authoritative for final integration status.

## 2026-10-31 capture understanding v2.2

Owner asks MADAR to receive natural requests (tasks, appointments, reminders, invoices and similar personal records), classify and store them correctly, and develop the existing prompt. [v2.2 addendum](../docs/product/capture-v2.2/MASTER-ADDENDUM.md) refines v2.1 without changing original bytes. It defines input-versus-intent separation, evidence/field confidence, invoice expense/asset/document routing, undated tasks, time ambiguity, multi-intent atomic proposals, source preservation, duplicate handling and action-specific Undo. Broad capture is accepted scope; schema/prompt details remain implementation candidates. `AGENTS.md` points agents to this reference chain.

`node docs/product/capture-v2.2/check.cjs` PASS: 46 synthetic expected-output fixtures, 17 invalid proposals rejected, original reference hashes unchanged. No actual AI, voice/OCR, parsing, database, authorization enforcement or reminder delivery was exercised. The fixture verifier is not a production validator. Proposed next slice: authenticated deterministic text → task/appointment + source + one active occurrence + Edit/Undo, before real providers. Attachment limits/retention and provider selection remain open. This round creates no backend or production services.

Official main verified at `8b3b5daef3a53f4578082c3531899c00c27c9c9b`; separate [PR #4](https://github.com/n923760-rgb/madar/pull/4) remains open for circle interruption fixes. This product/prompt branch is independently based on main, with no automatic merge or governance adoption.

## 2026-10-31 local action-core experiment

Continuation builds a bounded local experiment in [experiments/capture_core](../experiments/capture_core/README.md), stacked on the v2.2 contract branch/PR #5. It consumes reviewed structured proposals and actually validates/saves task, appointment and reminder records in session memory, with preserved sources, owner-scoped access policy, exact retry idempotency, one active occurrence, clarification round-trip and action-specific reversal. Unsupported domain families defer the whole group. It does not perform natural-language understanding or execute invoice routing.

30 Python behavior tests PASS; five-proposal demo PASS; v2.2 fixture verifier PASS (46 expected outputs / 17 invalid proposals); reference integrity and `git diff --check` PASS. No authentication integration, durable storage, provider, audio/OCR, file ingestion, concurrency, edit/recurrence/delivery or UI/mobile integration is qualified. This is a local synthetic experiment, not production backend implementation. Current production status remains NOT STARTED.

Next bounded task: review the experiment and contract together, then design the authenticated adapter, persistence transactions and UI integration before any real personal data or production services are enabled. PR #4 circle fixes remain separate. No automatic merge or central-governance adoption is implied.

## 2026-10-31 capture integration boundary review

[Integration design](../docs/product/capture-v2.2/INTEGRATION-DESIGN.md) reviews the experiment's gaps and proposes authenticated identity, source/context revision binding, durable ingest versus domain commit, transaction/uniqueness policy, timeout reconciliation, targeted reversal with dependency checks, and truthful states across the five approved views. It preserves clear low-risk automatic capture, existing navigation and the one-active-occurrence invariant. Session policy, private-file limits and durable migrations remain candidates, not implemented integrations.

Optional local `ProposalGate` freezes proposed payloads and rejects late results after clarification changes source context. All 38 Python behavior tests PASS (30 existing + 8 new); five-proposal demo PASS; v2.2 specification verifier PASS (46 expected outputs / 17 invalid proposals), original reference hashes unchanged; `git diff --check` PASS. This is a synthetic in-memory ordering experiment, not authentication, a concurrent transaction, production persistence or a live UI connection. Auth/session, PostgreSQL/restart/concurrency, real provider/files/audio, delivery and UI/device tests remain NOT RUN. Production engineering remains NOT STARTED; no new services or deployment.

Next bounded task: prototype clarification, timeout/reconciliation and committed-receipt states with synthetic responses in the approved interface, then qualify mobile/accessibility before implementing the authenticated durable text slice. PRs #4–#6 remain separate review dependencies; no automatic merge or central-governance adoption.
## 2026-10-31 interruption qualification

An added regression failed against main: losing pointer capture before the hold threshold could start recording later. Fixed pending/active pointer cancellation, keyboard focus-loss cancellation, Escape event containment, secondary pointer isolation and recording recentering. Both Node suites and `git diff --check` PASS. Chromium native held mouse and Space submission PASS; Space+Tab cancellation and Space+Escape local cancellation PASS. Rechecked 40 shell layout cases (five primary views × four widths × two themes): no horizontal overflow or primary-view buttons below 44×44px. This is desktop Chromium, not mobile touch qualification.

[Qualification report and physical-device task script](REPORTS/INTERACTION-QUALIFICATION-2026-10-31.md). Next: review the isolated fixes; execute the script on Mate X6 folded/unfolded and Telegram, then scope the first implementation slice. No production backend/provider or unspecified governance adoption starts in this round.

## 2026-11-01 interactive capture state prototype

The [prototype guide](../docs/ux/prototype/README.md#capture-state-journeys--2026-11-01) documents two new synthetic journeys: reminder-time clarification and lost storage response (before/after the mock action), plus unsent/offline retry, same-operation reconciliation, source/clarification preservation and explicit-action reversal. Inbox reopens pending captures; Calendar/Ask expose only confirmed mock receipts. The time starts empty. Existing circle/navigation and old fixtures are preserved. The local JavaScript ledger is independent of the Python experiment in PRs #6/#7; no real integration is claimed.

12 added Node behavior tests PASS; existing flow/design suites PASS; original reference integrity and palette contrast PASS; Chromium clarification/reconciliation checks and 56 phone-shell layout/target cases PASS; `git diff --check` PASS. Exact coverage/limits and reproduction steps are in the prototype guide. Physical mobile/Telegram, screen readers/200% text, actual provider/auth/storage/network/delivery remain NOT RUN. This design branch is based on PR #4's interruption fixes; PRs #5–#7 remain separate unmerged product/experiment dependencies. Production status remains NOT STARTED, central-governance adoption PENDING; no automatic merge.

Next bounded task: review these recovery states on Huawei Mate X6 folded/unfolded and Telegram, then qualify first-user usability and accessibility before the authenticated durable text slice. Private design preview published successfully at https://madar-design-review-oct28.n923760.chatgpt.site from Site source commit `dc7fdf98785b8d28a7aede669ccc260ecb8a7f79`. This is separate from enabling any MADAR production service.

## 2026-11-01 capture draft and navigation repair

Follow-up within the PR #8 design branch fixes unsubmitted time loss and cross-capture Back/Forward context. Drafts are scoped to a capture in page memory; explicit confirmation alone appends the clarification. History binds route/capture/index, including same-route capture switches. Enter and associated help/error semantics improve keyboard interaction.

16 capture tests PASS (12 existing + 4 regression cases), existing flow/design suites and original-reference/palette checks PASS; Chromium draft retention, second-capture isolation, native Back/Forward context and Enter confirmation PASS; `git diff --check` PASS. See the prototype guide for exact evidence. The earlier 56-case shell matrix remains a dated checkpoint, not a rerun. Physical Mate X6/Telegram/virtual keyboard, screen readers and 200% text remain NOT RUN. No production service, governance adoption or automatic merge. Next: execute the physical-device script, review accessibility and prepare the bounded durable-text implementation only after that review.

Private preview republished successfully from Site source `df4ac89633798e77055e9a7fdc3b521ccb070bae` at https://madar-design-review-oct28.n923760.chatgpt.site. Owner-only audience preserved.

## 2026-11-01 automated prototype validation

Added a read-only GitHub Actions workflow for the three prototype Node suites, using Node 24 and commit-pinned official actions. It covers capture/recovery, circle/navigation and design/reference assertions without deployment, secrets or provider calls. Workflow YAML parsing and all three local commands PASS (16 capture tests plus existing flow/design checks); `git diff --check` PASS. Hosted CI status must be read from its run; it is not inferred from local PASS. Branch protection, real device/accessibility and production integration remain unchanged/unqualified. No automatic merge or central-governance adoption.

Hosted execution subsequently verified PASS: https://github.com/n923760-rgb/madar/actions/runs/41334387631 — the capture, flow/navigation and design/reference steps all succeeded. This establishes the first hosted workflow result, not branch protection or device/provider qualification.

## 2026-11-02 optional invoice association prototype

Invoice review now offers source-only retention or explicit association with the existing washer, without inventing an asset/warranty/expiry/reminder or adding a tab. The synthetic action ledger provides committing/receipt/reconciliation/source/targeted reversal; confirmed association appears on the existing asset and invoices stay outside Calendar. Duplicate review cannot bypass into source-only execution. No arbitrary file extraction, expense accounting or durable ingestion is claimed.

19 capture tests and existing flow/design/reference checks PASS locally; Chromium invoice source-only/association/reversal and 12 narrow-shell/theme cases PASS. Guide contains reproduction steps and limits. Real files/OCR/private storage, mobile/Telegram, screen readers and production services remain NOT RUN/not implemented. Work stays on PR #8 with no automatic merge or central-governance adoption. Next: review optional invoice association alongside the physical-device script and qualify accessibility before bounded production engineering.

## 2026-11-02 cross-branch integration review

[Integration review](REPORTS/INTEGRATION-REVIEW-2026-11-02.md) pins published heads and reruns both workstreams: PR #8's 19 capture tests plus flow/design checks PASS; PR #7's 38 Python tests, five-proposal demo and 46-output/17-rejection specification verifier PASS. A local read-only merge-tree probe found a roadmap conflict between the two chain tips. No remote merge or combined runtime qualification was performed. UI invoice behavior remains independent from the Python adapter, which defers invoices. Existing CI covers UI only; physical-device/accessibility, real identity/storage/provider/delivery and central-governance adoption remain unqualified.

Next: review the pinned integration procedure, resolve the roadmap in an authorized isolated integration branch retaining both dated histories, then rerun combined checks and extend CI. No automatic merge, production service or preview change in this review.
