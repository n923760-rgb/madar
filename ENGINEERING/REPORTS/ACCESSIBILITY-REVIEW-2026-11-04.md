# MADAR text scaling and keyboard review — 2026-11-04

## Source and scope

Official main: f6620a7e03173a5b3d166f002830276071b2b9e3. Repository identity and no open PRs verified before work. Branch: design/mobile-accessibility-v0.5. UI prototype only; original Product v2.1 / UX v1 and production code are unchanged. PRs #4–#8 were merged on 2026-11-03; main CI run 41597470602 succeeded.

## Findings and changes

Fixed-pixel font sizes did not follow the browser root text setting. Use rem units, with the same default sizes, and expose 100/150/200% review scaling. At narrow large-text widths, the circle stays dominant and shortcut buttons reflow below it. Physical gestures, accessible capture fallback and shortcut destinations are preserved.

Unconditional render focused the screen and reset its scroll after every calendar/filter action. Retain control focus and reading position only for the same route and capture; announce a named main region for destination/capture changes or removed controls. Four focused tests cover these cases. The calendar regression failed on main (22/23 passing) and passes after the fix (23/23).

The initial matrix found undersized Inbox disclosure and narrow Calendar cells. Give summaries minimum 44px height, let Calendar use available inline padding, and reserve a thin scrollbar so seven 44px columns fit at 320px. Recheck after repair passed.

## Executed evidence

| Check | Result | Limit |
|---|---|---|
| Node capture/state/focus suite | PASS, 23 tests | DOM stub; not screen-reader execution |
| Flow/navigation/circle suite | PASS | Synthetic controller / DOM stub |
| Design/palette/reference suite | PASS | Token-level contrast and original-file hashes |
| Chromium layout/target matrix | PASS, 80 cases | Five primary routes × four phone-shell widths × two text scales × two themes |
| Native Enter on Calendar day | PASS | Same control retains focus and pressed state |
| Native Enter on Inbox filter | PASS | Same control retains focus and pressed state |
| Destination menu navigation | PASS | Focus on named main region |
| git diff --check | PASS | Whitespace check |

Matrix widths: 320, 360, 390, 430 CSS px. Text scales: 100 and 200% root font size. No horizontal phone/screen overflow; all visible buttons, inputs, selects and summaries measured at least 44×44 CSS px. Measurement includes controls outside the current scroll viewport; collapsed content with no rendered box is excluded. This is not a usability study or a physical viewport/device test.

## Not executed / still open

Physical Huawei Mate X6 folded/unfolded, Telegram WebView, soft keyboard/safe-area behavior, OS font scaling, browser zoom at 200%, screen readers, reduced-motion emulation and first-time user tasks remain NOT RUN. Root text scaling is a bounded browser review aid and does not replace those checks. No claims of real audio, provider classification, OCR, private-file storage, authentication, durable persistence or notifications.

## Device follow-up

Use the existing physical-device task script plus this sequence: increase system text size; open all five views in dark/light; open month view; traverse days and filters with a connected keyboard or screen reader; open the internal composer with the soft keyboard; hold/release the circle, cancel an active hold and use explicit recording buttons. On Mate X6, repeat folded, unfolded and landscape. Record actual observations before changing NOT RUN statuses.

Private preview publication succeeded on 2026-11-04 at https://madar-design-review-oct28.n923760.chatgpt.site, from Site source `25a3adbc2a4a102d733e3b2418ce9beda6dd6055`. Owner-only audience preserved. This publishes the synthetic design preview; it does not enable MADAR production services.
