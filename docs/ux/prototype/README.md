# MADAR interactive design prototype v0.1

Design study only. UX-003 remains **PROPOSED**. No production frontend/backend, AI, media capture, persistence or notifications are implemented.

## Open and review

Download [index.html](index.html) and open it in a modern browser. It is self-contained, works offline, and has no dependencies or external assets. Reloading resets the synthetic session. Font names reference the approved Arabic families but fall back to installed fonts; font assets and typography must be qualified before sign-off.

The review panel selects 320/360/390/430px, night/day appearance, a capture scenario, individual screens and the internal composer versus Compact Mode. The hero circle stays on Home. Internal browse pages use a microphone at the right in RTL, text in the middle and an attachment at the left. Typing changes the microphone to Send. Forms and editing screens omit the capture composer. Ask uses an explicit question form.

The ten numbered screens are Welcome, Onboarding, Home, Expanded directions, Voice, File, Processing, Clarification, Saved and Inbox. Supporting views include Calendar, My Things, Vehicle timeline, Appliance, Ask, Source, Correction and Settings. Tap alternatives expose all direction destinations; dragging is candidate behavior requiring browser/device verification.

## Review journeys

| Journey | Click sequence / expected design behavior |
|---|---|
| Clear reminder | Reminder scenario → Try flow → Stop → Send → Complete simulation → Saved → View Calendar. No clarification step; Undo affects this simulated save. |
| Oil change | Oil scenario → Voice → Send → Complete → Confirm valid mileage → Saved → Vehicle timeline. Invalid mileage stays unresolved. |
| Document renewal | Document scenario → PDF example → Send → Complete → Choose reminder timing → Saved → Calendar. One next active reminder in the design. |
| Invoice to asset | Invoice scenario → Photo example → Send → Complete → Choose appliance → Saved → Appliance. Appliance → duplicate example → Existing must not simulate another save. |
| Ask / correction | My Things → Ask → Last oil change → Source → Correct → Save correction → Undo. Keep the original source visible. |

Inbox includes processing, uncertain and failed examples; Retry preserves the synthetic source. Offline retry reports unavailability. Attachments and recording are explicitly simulated; playback only explains that no audio exists. Free text is shown safely in the source preview, while interpretation uses the selected fixture. This is not a general parser or working organizer. Fixed fixtures in Calendar/timelines remain demonstration content; a simulated save is separately identified. The appliance/new-asset examples are illustrative, not persistent domain objects.

## Verification at this checkpoint

Run from repository root:

```sh
node docs/ux/prototype/checks/flows.cjs
```

Passed: 20 template renders; clear direct save; uncertain mileage validation; correction undo; duplicate handling; offline retry; answer/source; HTML escaping; Back; absence of network/storage/media APIs. The test intentionally labels its DOM stub limitation.

**NOT RUN:** browser visual inspection, gesture tests, keyboard/Telegram safe-area behavior, 200% scaling, actual font loading, measured contrast, screen-reader checks and first-time usability. Review controls and CSS are candidates, not evidence of these checks. No approval or central-governance adoption is implied.

After browser QA, record results in a dated report and update the [single roadmap](../../../ENGINEERING/MASTER_ROADMAP.md). Record accepted design changes in the [decision log](../DECISION_LOG.md).
