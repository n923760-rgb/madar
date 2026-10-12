# MADAR First Ten Screens — Wireframe Brief v0.1

Status: DRAFT DESIGN BRIEF — not a rendered or user-tested prototype.
Scope: UX/UI only. Arabic-first, RTL. No production application.

## Visual direction

Preserve the approved petrol-navy / warm paper / restrained gold identity and desert-day light theme. Keep the central circle at the visual center of Home's usable viewport. Use semantic colors, logical CSS directions, readable Arabic, sparse decoration, and reduced-motion alternatives.

The following specifies screen composition for the next visual design pass. All numeric sizes are prototype candidates, not a frozen standard.

| Screen | Top | Main composition | Primary action | Secondary / recovery |
|---|---|---|---|---|
| 01 Welcome | Small MADAR mark | Promise «بس أرسلها لمدار.» plus one plain explanation | «ابدأ» | «كيف يحفظ مدار معلوماتي؟» |
| 02 Onboarding | Skip / progress | Three short steps: send, understand/organize, remind/retrieve; optional gesture practice | «التالي» / «خلنا نبدأ» | «تخطي»; show only required preferences |
| 03 Home | Greeting and one relevant upcoming/attention item | Central hero circle; two satellites for text and attachment; subtle labeled destination alternative | Tap voice | Calendar, My Things, Inbox, Ask available by visible taps |
| 04 Expanded Control | Existing Home dims | Four labeled targets around the anchored center; directional highlight | Release on a target | Release in dead zone cancels; accessible tap route |
| 05 Voice Capture | Close / duration | Restrained listening state; transcript only when reliable | Stop then «إرسال» | Cancel, playback, re-record; permission-denied state |
| 06 Photo/File | Back / capture title | Camera/Photos/File choices then source preview and optional note | «إرسال لمدار» | Remove file, replace, unsupported/oversized/upload-failure states |
| 07 Processing | Small source preview | Real stage label; «تقدر تطلع، وبنبلغك إذا خلصت.» | «عرض في الوارد» | No fake percentage; failure preserves source |
| 08 Clarification | Source access | Short understanding summary; uncertain field only; choices before text | Confirm selected detail | Edit, not this, keep for later; duplicate/object ambiguity variants |
| 09 Saved | Calm success mark | Exact outcome, resolved time/object, relevant next reminder | «عرض» | «تراجع» tied to this action |
| 10 Inbox | Title and compact filters | Needs confirmation, processing, failed; recent organized items secondary | Resolve the top pending item | Retry, add detail, keep; empty/loading/error variants |

## Proposed internal composer

Apply to Inbox and supporting browsing views as a prototype alternative to Compact Mode:

- Height candidate 56–64px inside the Telegram safe area.
- Microphone at inline-start; at least 44×44px target.
- Text input in the middle; attachment at inline-end.
- Send replaces microphone when text is present. Keep labels accessible.
- Opening the keyboard must not obscure Save, timeline controls, or the focused input.
- Editing and modal flows may omit the composer when it competes with their primary action.
- A microphone request must say whether it records a new capture or asks a question. Ask MADAR has a separate explicit query context.

This change remains UX-003 PROPOSED until the owner accepts the visual result.

## Prototype journeys

1. Home → Voice → Processing → Clarification if needed → Saved → Calendar.
2. Home → File → Processing → Invoice classification → Asset timeline.
3. Inbox failed capture → Add detail / Retry → Saved.
4. My Things → Vehicle → Oil-change capture → Next mileage reminder.
5. Ask MADAR → Recorded answer → Source → Correct / Undo.

Supporting Calendar, My Things, Timeline, Ask, and Settings views are required to finish these journeys, even though they sit outside the first ten primary screen numbers.

## Review matrix and acceptance

- Viewports: 320, 360, 390, 430 CSS px. Test short and long Arabic content, font scaling, portrait/landscape, keyboard, and Telegram safe areas.
- Touch targets at least 44×44px; WCAG AA contrast; labels for icon controls; state never conveyed by color alone.
- Visible tap alternatives for every direction; reduced motion; focus and Back behavior documented.
- Clear distinction between local draft, uploading, processing, and saved.
- A low-risk clear capture must not gain an unnecessary confirmation step.
- Failed captures remain visible and retry does not imply duplicate persistence.
- Run the UX v1 usability tasks and record actual results separately. Current status: NOT RUN.

## Handoff boundary

Next deliverable: rendered wireframes and clickable design prototype. Do not claim UI approval, runtime microphone support, actual AI processing, persisted actions, or reminder delivery from this brief.
