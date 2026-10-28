# MADAR interactive design prototype v0.2

Open `index.html` in a modern browser, or use the owner-only [interactive preview](https://madar-design-review-oct28.n923760.chatgpt.site). On mobile, scroll below the app for review tools; appearance is also reachable in the app's destination menu → Settings. All examples are synthetic and memory-only. Reload resets them. No microphone, AI, upload, persistence or notifications are active.

Home preserves tap-to-voice and four physical drag directions: up Calendar, right My Things, left Inbox, down Ask. Each destination has a visible tap alternative. The header brand returns Home; the menu opens destinations/settings. RTL Back and browser Back return to the previous route.

The review panel controls shell width, dark/light mode, four capture fixtures, screen selection and dock/Compact comparison. My Things has search/type filters. Calendar supports day/week/month, month traversal and day selection against a fixed 28 October 2026 review date. Unknown Ask queries return a no-result state. Text drafts survive in-session navigation.

## Review paths

1. Reminder fixture → Try flow → Stop → Send → complete → saved → Undo.
2. Oil fixture → voice → processing → valid mileage → saved → vehicle timeline.
3. Document fixture → PDF → send → complete → reminder timing → saved.
4. Invoice fixture → photo → send → complete → appliance → saved.
5. Ask → oil question → source → correct → save → Undo.
6. Inbox → failed item → offline simulation → retry blocked → restore connection → retry.
7. Home circle → each physical direction; short/diagonal/cancelled drag must not start voice. Repeat by visible buttons and keyboard.

## Checks

```sh
node docs/ux/prototype/checks/flows.cjs
node docs/ux/prototype/checks/design.cjs
```

These are Node logic checks, not device qualification. See the [dated report](../../../ENGINEERING/REPORTS/DESIGN-REVIEW-2026-10-28.md) for actual browser results and NOT RUN cases. [Design System](../DESIGN_SYSTEM-v0.2.md) documents tokens/components/interactions. Font subsets and license text are embedded to keep the preview self-contained.

UX-003 and final visual approval remain pending. Product/UX reference bytes are unchanged. Do not start production engineering from this prototype alone.
