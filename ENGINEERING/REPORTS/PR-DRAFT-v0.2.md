# design: refine MADAR five-screen minimal premium prototype

Proposed base: `design/interactive-prototype-v0.1` (stacked on PR #2).
Proposed head: `design/minimal-premium-v0.2`.
Status: prepared locally; not a created GitHub PR.

MADAR's prototype now exposes the four circle destinations by labeled taps, removes repeated internal navigation, and uses a shared Arabic dark/light visual system. My Things gains search and filters; Calendar gains selectable day/week/month views; Ask gains an explicit no-recorded-result state. RTL Back, browser history, draft retention, gesture cancellation and narrow calendar targets are improved. Arabic font subsets are embedded for consistent offline review.

Private interactive review: https://madar-design-review-oct28.n923760.chatgpt.site

Validation: both Node suites pass; 40 constrained-browser layout cases pass after target-size repair; five simulated fixture journeys exercised in Chromium. The final shared-record display adjustment was checked in Node only. Real-device/Telegram keyboard, screen readers, 200% text, reduced-motion runtime and first-time usability tests are NOT RUN. See ENGINEERING/REPORTS/DESIGN-REVIEW-2026-10-28.md.

Product Master v2.1 and UX source hashes are unchanged. UX-003, exact visual tokens/font choice and final approval remain pending. No backend, microphone, AI, persistence or reminders are implemented. No automatic merge requested.
