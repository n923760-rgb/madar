# MADAR Design System v0.2

Status: PROPOSED visual implementation, 2026-10-28. Product Master v2.1 remains authoritative. This is a reviewable prototype, not a production UI or visual sign-off.

## Visual reference and hierarchy

Reconstructed from the user's latest retrievable choice: calm petrol navy/teal, warm gold, large Home circle, warm sand light mode, simple internal input dock. The original selected raster image was not recovered; no pixel-match claim is made. UX Architecture v1 §17 independently supports this direction. Older conflicting gesture concepts are superseded by the four destinations in UX v1 §4.3.

Home contains a quiet greeting, one attention row, the central circle, two capture alternatives, and two compact Today/Upcoming cards. No permanent Tasks, Invoices, Expenses, or Documents navigation is added. Internal pages use one compact header destination menu and a capture composer, without the previous repeated bottom tabs.

## Color tokens

| Semantic token | Dark | Light | Role |
|---|---|---|---|
| background | #0D242C | #F6F2E9 | Page |
| surface | #163139 | #FFFCF5 | Cards |
| surface-raised | #1D3B43 | #EEE7DA | Selected chip |
| text-primary | #F3EFE5 | #18323A | Main text |
| text-secondary | #BAC8C9 | #52646A | Supporting copy |
| accent | #D8B77C | #7B591D | Primary action and focus |
| on-accent | #17252A | #FFFAF0 | Primary action text |
| border | #36545C | #D5CBBB | Decorative separators |
| control-border | #71878A | #8A8172 | Input boundaries |
| success | #9CD5BE | #28704E | Success text, with words/icon |
| danger | #FFB7A5 | #A33D29 | Failure text, with words/icon |

`design.cjs` checks text token pairs against background/surface (minimum dark 7.17:1; light 5.34:1), primary action contrast ≥4.5:1 and input boundary contrast ≥3:1. Decorative separators are not control boundaries. This is not a full WCAG audit.

## Typography, spacing and icons

- Embedded Arabic subsets: Noto Kufi Arabic headings/brand; Noto Sans Arabic body. Noto Sans is a deliberate available prototype substitute for the earlier IBM Plex Sans Arabic reference, pending owner review. Font copyright and SIL OFL notices ship in `prototype/FONT-NOTICES.txt` and inside the HTML.
- Body 16px / 1.8; H1 25px / 1.65; H2 19px; supporting text 13px; compact metadata 11–12px. Font size enlargement and real screen-reader testing remain required before freeze.
- Spacing scale: 4, 8, 12, 16, 20, 24, 32px. Page inset 24px, 20px at mobile breakpoint. Cards 20px radius; compact controls 12–14px.
- One consistent 24px outline SVG icon family, stroke 1.6. Icons have accessible names on their buttons. RTL Back points right. Calendar previous points right, next left. Physical gesture directions intentionally do not auto-mirror.

## Component contracts

| Component | Contract |
|---|---|
| Home circle | 136px candidate diameter. Tap simulates voice; drag starts only on circle. No idle glow or looping motion. |
| Direction buttons | Always visible labeled alternatives: ↑ Calendar, → My Things, ← Inbox, ↓ Ask. |
| Capture alternatives | Text and photo/file directly below the circle; one action each. |
| Internal composer | Mic on RTL inline-start/right, text center, attachment left. Send replaces mic when typed. No floating overlap. |
| Edit/capture pages | Omit global composer to keep Save/Cancel dominant. Text draft survives in-app Back. |
| Ask | Explicit question field and voice-question action; no unrelated capture composer. Answers expose source; unknown questions show no-result state. |
| Object list | Human name first, one relevant next detail. Search, type chips, and empty state; subscription sample list intentionally empty. |
| Calendar | Day/week/month, previous/next month, selected day, Today. Fixed review date 28 October 2026, Riyadh; no OS date inference or live reminders. |
| Feedback | Inline state text and status region. Undo is a simulation of the displayed action. |

## Interaction and accessibility

- All measured primary-screen buttons ≥44×44px at 320/360/390/430px shell widths. Narrow calendar uses the page's inline gutters to retain 44px targets.
- Drag threshold 24px; commit distance >70px; diagonal ambiguity within 20px cancels. Short/OS cancellation suppresses follow-on voice click; keyboard activation remains available. Real touch/haptic behavior is unqualified.
- Standard browser Back and on-page Back traverse the same history; Escape requests Back. Header brand returns Home. Menu is a route, so Back closes it first.
- Focus ring 3px accent; main content receives focus on navigation. Native controls, semantic headings, labels and `aria-pressed` on filter/date choices. Live status for feedback/search results.
- Motion limited to 160ms control feedback and simulated recording waveform. `prefers-reduced-motion` disables transitions/animations.
- Content scrolls inside available height; safe-area padding protects header/composer. Real mobile keyboard, Telegram chrome, 200% text and screen readers remain pending.

## States to retain

Idle → simulated listening → captured → processing → targeted clarification when uncertain → saved with View/Undo. Also duplicate, failed, retry, offline, no-result and empty states. No actual AI, microphone, camera, persistence or notification capability is claimed. Reload resets all data.
