# MADAR design review — 2026-10-28

## Result

A v0.2 interactive, Arabic/RTL design prototype now refines the five primary screens with shared dark/light tokens, embedded Arabic fonts, discoverable circle navigation, a quieter internal composer, searchable/filterable objects and selectable calendar dates/views. Design approval remains pending. No backend, database, AI integration or production MADAR service was created.

Private interactive review: https://madar-design-review-oct28.n923760.chatgpt.site

Access is owner-only using the owner's ChatGPT account. Static prototype publication succeeded through Sites. Cloud Browser reached the sign-in gate; authenticated access on the owner's real phone has not been verified. Source in this branch remains the authority; Sites serves a copy of `docs/ux/prototype/index.html`.

## Reviewed baseline

- Repository identity and official main: `n923760-rgb/madar`, `efb9e91a7f0fe858d60ad1394c1dfd9c1b487e19`.
- PR #2: open, draft, head `dcc37b80069797ffe90a216dad11c30160b702aa`, branch `design/interactive-prototype-v0.1`; no discussion comments returned.
- Reviewed all tracked source/documentation: README/index, AGENTS, roadmap, baseline report, reference manifest, Product Master v2.1, UX Architecture v1, decision log, design brief, prototype guide/HTML/logic tests. No production app or CI configuration is present in that tree.
- The two original approved reference files retain exact manifest hashes. Their original headers are preserved.
- Prior unpublished local gesture/cancellation repair from 27 October was inspected and carried forward. No prior unpublished report was treated as live GitHub truth.
- Local branch: `design/minimal-premium-v0.2`, based directly on live PR #2 head. It can be submitted as a stacked PR against PR #2's branch, or later retargeted after PR #2 merges. Neither PR is authorized for automatic merge.

## Findings and changes

| Area | Finding in PR #2 | v0.2 response |
|---|---|---|
| Home | Directions behind another action; greeting can compete with orbit | Labeled directions visible around central circle; one attention row; compact Today/Upcoming cards |
| Internal navigation | Composer plus repeated bottom navigation | One header destination menu; brand returns Home; composer remains the sole bottom strip |
| Voice | Unclear competing placement options | Default dock with mic right in RTL, text center, attachment left; Compact comparison retained in review tools |
| RTL/Back | Left-pointing Back; app-only history | Right-pointing Back and browser history integration |
| My Things | Three unfiltered buttons | Search, type filters, clear empty states, identity and next detail |
| Calendar | Static cards only | Day/week/month, month traversal, date selection, Today and empty days |
| Ask | Unsupported input only produced a generic toast | Explicit no-recorded-result state and sourced oil answer reflecting the displayed oil data |
| Typography/theme | Device font fallback; inherited light-mode text issue identified during QA | Embedded Arabic subsets; semantic text inheritance corrected on theme container |
| Accessibility | Small calendar targets at narrow widths in first pass | Narrow calendar gutter adjustment; follow-up matrix found no targets below 44px |
| Gesture cancellation | Short swipe could become a voice click | Preserve prior suppression repair; ambiguous diagonal cancels; visible tap alternatives remain |

The latest selected raster reference was not recovered. The visual direction is reconstructed from the retrievable conversation description and UX §17; it is not a claimed exact reproduction of an unseen image.

## Executed validation

| Check | Result | Scope/limits |
|---|---|---|
| `node docs/ux/prototype/checks/flows.cjs` | PASS | 20 templates; low-risk save; clarification/mileage; correction undo; duplicate/offline retry; escaping; Back; four pointer handler directions; cancellation/click suppression. Node DOM stub, not real touch. |
| `node docs/ux/prototype/checks/design.cjs` | PASS | Search/filter/empty, calendar, Ask no-result, draft retention, palette contrast, immutable reference hashes |
| Browser layout matrix | PASS after correction | 5 screens × 4 shell widths × 2 themes = 40 cases. Actual content shell widths 318/358/388/428 due to 1px border. No horizontal overflow; no primary-screen button below 44×44px. Desktop Chromium with constrained shell, not device emulation. |
| Browser journey A | PASS | Simulated voice reminder → Stop → Send → processing → direct save → Undo |
| Browser journey B | PASS | Simulated oil capture → clarify 86,000 → next threshold 91,000 |
| Browser journey C | PASS | PDF example → clarification → renewal save |
| Browser journey D | PASS | Photo example → link to appliance → save |
| Browser journey E | PASS | Ask example → source → edit → save correction → Undo |
| Visual inspection | PASS with remaining review | Home dark and light; narrow Inbox. Light text inheritance defect corrected and verified by computed style/screenshot. Arabic embedded font rendered. |
| Token contrast | PASS | Minimum body semantic pairs: dark 7.17:1, light 5.34:1; primary action ≥4.5; input border ≥3. Does not certify whole-page accessibility. |
| Private preview publication | PASS | Exact static source copy published owner-only; sign-in gate observed |

Browser journey checks were followed by a source-level improvement sharing the oil display record across source/timeline/Ask; final Node regressions passed. That final synchronization change did not receive a repeat browser journey run because the shared local preview was reassigned to another project. Do not overstate browser coverage of the final file.

## Not run / remaining approval

- Actual Huawei/iPhone/Android touch, mobile keyboard, safe areas inside Telegram, landscape/foldable layouts, short-height devices, 200% system text, VoiceOver/TalkBack and reduced-motion runtime checks.
- First-time Arabic user study and UX v1 success metrics; no usability percentages claimed.
- Pixel comparison with the original chosen image, which remains unavailable.
- Full WCAG/axe audit, screen-reader announcements and focus restoration across all filters.
- Actual microphone/AI/media upload/persistence/reminders/security: intentionally outside this phase.
- Full production-quality action audit/history and reminder semantics. This prototype retains bounded fixtures and one-session simulations; it is not the implementation of those systems.
- Owner approval of UX-003 dock, UX-007 diameter/placement, font substitution and final palette. Central governance adoption ENG-001 remains PENDING; no governance lock is asserted.

## GitHub publication history

The GitHub connector could read the repository and PR but rejected `create_branch` with HTTP 403, `Resource not accessible by integration`. The local branch, changes and review text are prepared. No remote branch or new PR was created; no merge occurred. Browser fallback requires the user's approval under the browser connector-failure rule. This is a connector permission failure, not an automatic safety-review rejection.

### Authorized browser publication follow-up

The owner authorized browser fallback on 28 October 2026. The remote branch `design/minimal-premium-v0.2` was created from PR #2 and the prototype upload was verified through GitHub reads. Documentation and checks are being published in the same branch. The earlier 403 remains a connector limitation; browser writes are available. A review PR is the final step; no merge is authorized.
