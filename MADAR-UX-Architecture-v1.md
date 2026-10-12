# MADAR (مدار) — UX Architecture v1

**Status:** Proposed for Approval  
**Product baseline:** MADAR Product & UX Master Specification v2.1  
**Phase:** UX architecture only — no production code  
**Primary language:** Arabic, RTL, Saudi-friendly  
**Primary surfaces:** Telegram Bot + Telegram Mini App

---

## 1. Purpose

This document defines how MADAR behaves before visual UI production and engineering begin. It turns the approved product direction into a testable experience model: navigation, the central MADAR control, screen states, capture behavior, confirmation, recovery, object timelines, reminders, and Ask MADAR.

The product promise remains:

> **بس أرسلها لمدار.**

The user should not need to understand MADAR's internal categories before sending something. MADAR receives the item, understands it, asks only when necessary, organizes it, and returns it at the right time.

---

## 2. Experience Principles

1. **Capture before classification.** Never ask the user to choose a type before sending.
2. **One dominant action.** The central MADAR circle is the visual and functional center of Home.
3. **Voice is one tap away.** A single tap starts voice capture immediately.
4. **Recognition over memory.** Direction labels appear as soon as dragging begins; users do not need to memorize gestures.
5. **Confirmation is exceptional.** Confirm only uncertain, risky, destructive, or identity-sensitive actions.
6. **Ask only about the uncertain field.** Confidence and clarification operate at field level.
7. **Never lose a capture.** Failed or incomplete processing always remains recoverable in Inbox.
8. **Show evidence.** Ask MADAR answers can open the original source or event.
9. **Speak within recorded knowledge.** Use wording such as «المسجل عندي» and never imply complete knowledge of the user's life.
10. **Calm, not empty.** The interface is sparse but always explains current state and the next useful action.
11. **Gestures are enhancements, not barriers.** Every swipe action has an accessible tap alternative.
12. **Bot captures; Mini App organizes.** Both surfaces share one data model and consistent outcomes.

---

## 3. Product Surfaces and Responsibility

| Surface | Primary responsibility | Best used for |
|---|---|---|
| Telegram Bot | Universal capture and immediate follow-up | Text, voice, photo, screenshot, PDF/file, forwarded message, notifications, quick confirmation |
| Telegram Mini App | Browse, organize, inspect, edit, and retrieve | Home, Inbox, My Things, Calendar, Ask MADAR, timelines, settings |
| Telegram notification | Bring the right item back at the right time | Reminder, renewal, clarification, processing failure |

The same capture must never appear as two separate records because the user interacted with it in both Bot and Mini App.

---

## 4. Information Architecture

### 4.1 Primary destinations

- **الرئيسية** — today, attention, upcoming, and the central control.
- **الوارد** — items needing confirmation, processing, or recovery.
- **أشيائي** — vehicles, documents, subscriptions, and assets.
- **التقويم** — future-first day, week, and month views, with past navigation available.
- **اسأل مدار** — retrieval over the user's own recorded data.
- **الإعدادات** — preferences, reminders, privacy, accessibility, and account.

There are no standalone Tasks, Appointments, Invoices, Expenses, or History tabs.

### 4.2 Primary navigation model

MADAR uses a **hybrid navigation model**:

1. On Home, the large central control supports four directional destinations.
2. A compact destination row or menu provides the same four destinations by tap.
3. On internal pages, a compact MADAR control remains reachable for capture.
4. Settings is reached from the profile/control area, not from the four-direction gesture.
5. Standard Back returns to the previous state without discarding drafts.

### 4.3 Direction map

| Direction from the center | Destination | Rationale |
|---|---|---|
| Up `↑` | **التقويم** | Future and upcoming items live spatially above the present moment. |
| Right `→` | **أشيائي** | In RTL reading, this feels like moving toward the user's owned context. |
| Left `←` | **الوارد** | A queue of received items waiting to be handled. |
| Down `↓` | **اسأل مدار** | Pull up retrieval and questions from the current context. |

The mapping is the baseline for prototype testing. Direction labels must always appear during drag. If testing shows repeated direction errors, change the mapping before visual freeze rather than teaching the user harder.

---

## 5. The Central MADAR Control

### 5.1 Two display modes

**Hero Mode — Home**

- Large circle positioned at the actual visual center of the usable viewport.
- Two small satellites: image/file and text.
- Faint orbital arcs establish brand identity without visual noise.
- Sufficient clear space for a deliberate drag gesture.

**Compact Mode — internal pages**

- Smaller persistent control inside a safe, non-obstructive zone.
- Tap starts voice capture.
- Expanding it exposes text and image/file actions.
- It must not cover timeline actions, document controls, keyboard, or system safe areas.

### 5.2 Input behavior

| Input | Result |
|---|---|
| Tap center | Start voice capture |
| Tap image satellite | Open source chooser: Camera / Photos / File |
| Tap text satellite | Open focused text composer |
| Press and drag center | Reveal four directional destinations |
| Release over a destination | Open that destination |
| Release inside dead zone | Cancel navigation and return to idle |
| Long press center | Not assigned in V1, avoiding hidden commands |

### 5.3 Gesture mechanics

- Drag begins only from the central control, not the full screen.
- A short movement threshold prevents accidental activation during a normal tap.
- When the threshold is crossed, the four labels appear around the control.
- The nearest target enlarges slightly and receives one light haptic tick.
- Crossing to another target produces a single new tick, not continuous vibration.
- Releasing outside all targets cancels safely.
- Vertical dragging must not hijack ordinary page scrolling outside the control zone.
- A first-use coach mark demonstrates the gesture once and remains available in Help.

### 5.4 Control state machine

| State | Visual behavior | Primary copy | Available action |
|---|---|---|---|
| Idle | Stable circle, very subtle breathing motion | «وش ودك تحفظ؟» | Tap or choose satellite |
| Listening | Soft expanding ring and live duration | «أسمعك…» | Stop / Cancel |
| Captured | Brief settle animation | «وصلتني» | Cancel before upload finishes if possible |
| Uploading | Thin orbital progress | «جاري الرفع» | Continue in background |
| Processing | Slow orbit, no indefinite spinner | «أرتبها لك…» | Close; processing continues |
| Needs confirmation | Warm accent, restrained | «باقي أتأكد من شيء» | Open clarification |
| Saved | Short success pulse | Contextual confirmation | View / Undo |
| Failed | Calm danger treatment, no disappearance | «ما قدرت أكملها» | Retry / Add detail / Keep |
| Offline | Neutral paused state | «بنرسلها إذا رجع الاتصال» | Keep queued / Cancel |

Reduced Motion replaces pulses and orbital movement with static state changes and text.

---

## 6. Home Architecture

Home is not a dashboard. It answers three questions only:

1. What needs attention now?
2. What can I send to MADAR?
3. What is coming next?

### 6.1 Vertical composition

1. **Quiet header:** greeting/name, date, profile/settings access.
2. **Needs attention:** zero to two cards only. If empty, the section disappears.
3. **Central MADAR control:** Hero Mode at the visual center.
4. **Today:** compact list of immediate reminders/appointments.
5. **Upcoming:** next few meaningful items, not an infinite feed.

The circle retains visual priority. Attention cards may move it slightly but must not push it below the initial viewport under normal content.

### 6.2 Attention ranking

Only items requiring a user decision or carrying meaningful urgency belong here:

1. Overdue or due today.
2. A capture requiring clarification.
3. A failed capture requiring recovery.
4. A renewal approaching its user-defined threshold.

Informational observations such as «مدار يلاحظ» never displace urgent items.

### 6.3 Empty Home

Do not fill empty states with generic productivity prompts. Show the MADAR control, a short invitation, and one concrete example:

> «أرسل موعد، فاتورة، أو شيء ودك ما تنساه.»

---

## 7. First Ten Screens

### Screen 01 — Welcome

**Goal:** Explain the promise in one glance and establish trust.

**Content**

- MADAR mark and orbit motif.
- Headline: «بس أرسلها لمدار.»
- Supporting line: «صوت، صورة، ملف، أو رسالة… ومدار يرتبها ويرجعها لك بوقتها.»
- Primary action: «ابدأ».
- Secondary link: «كيف يحفظ مدار معلوماتي؟»

**Rule:** No feature carousel and no account form if Telegram identity is already available.

### Screen 02 — Onboarding

**Goal:** Teach the mental model with minimum setup.

Use three short steps:

1. «أرسل بطريقتك» — voice, text, image, screenshot, PDF/file, forwarded message.
2. «مدار يفهم ويرتب» — clarification only when needed.
3. «يرجعها لك بوقتها» — reminders, retrieval, and history.

Then request only necessary preferences:

- Notification permission/context.
- Default locale and timezone confirmation.
- Optional preferred reminder timing.

Show the central-control gesture once as an interactive practice, with a visible «تخطي» action.

### Screen 03 — Home

**Goal:** Provide the daily overview and immediate capture.

Contains the structure in §6, with Hero Mode as the dominant element. The tap-based destination alternative appears as a subtle labeled row or expandable menu, not a competing bottom bar.

### Screen 04 — Central Control Expanded

**Goal:** Make directional navigation self-explanatory.

When drag begins:

- Background content dims slightly.
- Four labels appear: التقويم / أشيائي / الوارد / اسأل مدار.
- Current target scales up.
- Center remains tethered visually to its resting position.
- Releasing in the dead zone cancels.

This is an interaction state, not a permanent page.

### Screen 05 — Voice Capture

**Goal:** Capture a natural statement with one tap.

**Content**

- Live duration and restrained listening state.
- Stop and Cancel.
- Optional live transcription only if quality is dependable; otherwise show it after stopping.
- After stop: allow quick playback and «إرسال» / «إعادة التسجيل».

**Rule:** If the user leaves after sending, processing continues and the result appears in Inbox/Home.

### Screen 06 — Photo / File Capture

**Goal:** Send visual or document evidence without pre-classification.

Source chooser:

- «الكاميرا»
- «الصور»
- «ملف»

After selection, show preview, optional note, and «إرسال لمدار». Screenshots and forwarded Telegram messages enter the same capture pipeline without forcing a separate type.

### Screen 07 — Processing

**Goal:** Communicate progress without trapping the user.

**Content**

- Small source preview.
- Plain-language stage such as «أقرأ الفاتورة» or «أحوّل الصوت لنص».
- Message: «تقدر تطلع، وبنبلغك إذا خلصت.»
- Action: «عرض في الوارد».

There is no fake percentage when the system cannot measure actual progress.

### Screen 08 — Clarification / Confirmation

**Goal:** Resolve only the missing or risky detail.

**Structure**

- What MADAR understood.
- Highlight only uncertain fields.
- Tap targets before free text.
- Original source accessible from the card.
- Actions: Confirm / Edit / Not this / Keep for later.

Example:

> «واضح عندي المبلغ والتاريخ. مدة الضمان مو واضحة — تعرف كم؟»

For invoice ambiguity:

- «مصروف عادي»
- «جهاز فيه ضمان»
- «وثيقة تخص شيء عندي»
- Optional «تفاصيل إضافية»

### Screen 09 — Saved Success

**Goal:** Confirm the exact outcome and preserve user control.

**Content**

- Contextual confirmation, e.g. «تم، سجلت تغيير زيت اليارس على ٥٣٬٤٢٠ كم.»
- Secondary context only when supported: «هذا ثالث تغيير زيت مسجل عندي لليارس هالسنة.»
- Created reminder, if any: «التذكير القادم عند ٦٣٬٤٢٠ كم أو بعد ٦ أشهر، أيهما أول.»
- Actions: «عرض» and «تراجع».

Undo adds a reversal; it never silently deletes the historical event.

### Screen 10 — Inbox

**Goal:** Act as a work queue, not a permanent archive.

Default sections:

1. **يحتاج تأكيد**
2. **جاري المعالجة**
3. **تعذر فهمه**

Recently organized items may remain briefly under «تم تنظيمه مؤخرًا» and then leave the default Inbox while staying searchable and visible in history.

Each failed item offers:

- «إعادة المحاولة»
- «أضف توضيح»
- «احتفظ به»
- Delete only through an explicit secondary action

---

## 8. Supporting Screens Required for a Complete Prototype

The first ten screens define the initial design package, but the five primary flows also require these supporting screens:

### 8.1 My Things

- One unified collection with filters for vehicles, documents, subscriptions, and assets.
- Search and recently used objects.
- Each card uses human identity first: name, relevant status, next event.
- No separate data silo per object type in primary navigation.

### 8.2 Object Detail and Timeline

- Object identity and current status at top.
- Most important upcoming reminder.
- Chronological event timeline as the main body.
- Related documents and linked objects.
- Add event, edit object, aliases, and archive controls.
- Source evidence accessible for every event created from a capture.

### 8.3 Calendar

- Opens to today and future items.
- Day, week, and month modes.
- Past navigation remains available.
- Items may include tasks, appointments, renewals, and reminder occurrences without forcing type-specific tabs.

### 8.4 Ask MADAR

- Suggested personal queries based on available data, not generic AI prompts.
- Text and voice question input.
- Answer card with source links.
- Clear zero-result response: «ما عندي شيء مسجل عن هذا.»
- Ask MADAR never guesses from general knowledge when answering about user data.

### 8.5 Settings

- Notification preferences.
- Weekly digest, off by default or trivially disabled.
- Language, date system, timezone, and reminder defaults.
- Accessibility: reduced motion and gesture alternatives.
- Privacy, export, account deletion, and support.

---

## 9. Five Primary User Flows

### Flow A — Text or Voice → Task, Appointment, or Reminder

1. User taps the central control or text satellite.
2. User says or writes: «ذكرني الخميس الجاي بعد المغرب أكلم أبو خالد.»
3. MADAR normalizes locale, timezone, relative date, and intent.
4. If the date resolves safely, MADAR saves directly.
5. If «بعد المغرب» needs a user-specific interpretation, MADAR asks only for the intended time or offers clear choices.
6. Success shows the resolved date/time and Undo.
7. Item appears on Home and Calendar; the original capture remains accessible.

**Critical cases:** ambiguous relative dates, past time, duplicate reminder, timezone change, notification permission missing.

### Flow B — Vehicle Maintenance + Odometer + Mileage Reminder

1. User sends: «غيرت زيت اليارس اليوم على ٥٣٤٢٠ والزيت يمشي عشرة آلاف.»
2. MADAR extracts maintenance type, object reference, date, odometer, and interval.
3. Object Resolution compares «اليارس» against aliases and existing vehicles.
4. Clear match links automatically; multiple plausible matches trigger a one-question chooser.
5. Validated actions create oil-change and odometer events plus the reminder rule.
6. Success states: next threshold ٦٣٬٤٢٠ km and any time condition.
7. Events appear immediately in the Yaris timeline.

**Critical cases:** odometer lower than latest reading, two Yaris vehicles, missing interval, mixed distance/time reminder, duplicate capture.

### Flow C — Document or Subscription → Expiry and Renewal

1. User sends a PDF, image, or forwarded renewal message.
2. MADAR extracts issuer/service, identifier where appropriate, expiry/renewal date, and amount.
3. It resolves an existing document/subscription before creating a new object.
4. High-confidence, low-risk fields save automatically.
5. Missing expiry asks only for expiry, without repeating known fields.
6. A reminder rule is created using the user's default lead time.
7. Renewal later adds an event and updates current state; it does not erase prior history.

**Critical cases:** Hijri/Gregorian ambiguity, auto-renewing subscription, no expiry printed, sensitive identifiers, duplicate object.

### Flow D — Invoice or Image → Expense, Asset, or Linked Document

1. User sends the image without selecting a category.
2. MADAR extracts merchant, date, amount, product, and explicit warranty data.
3. It never infers a warranty period merely from brand or market convention.
4. Confident classification saves directly where safe.
5. Ambiguous classification asks:
   - «مصروف عادي»
   - «جهاز فيه ضمان»
   - «وثيقة تخص شيء عندي»
6. Plain expense creates an unlinked expense event.
7. Asset creates an object, attaches the image, and creates warranty reminders only from explicit data.
8. Linked document proposes likely objects and confirms when necessary.
9. Success explains exactly what was created and offers Undo.

**Critical cases:** multiple totals, return receipt, no readable date, same invoice uploaded twice, uncertain object link.

### Flow E — Ask MADAR → Answer → Source → Edit or Undo

1. User asks: «متى غيرت زيت اليارس؟»
2. MADAR performs structured retrieval over the user's authorized data.
3. Answer gives the latest matching recorded event with careful wording.
4. User can open the source event, voice note, image, or document.
5. From the source, user may edit a current-state field or reverse an action.
6. Edits preserve history; Undo references the exact proposed action/effect.
7. If nothing matches, MADAR says so without guessing.

**Critical cases:** multiple vehicles, conflicting events, deleted/archived object, missing source attachment, answer based on several sources.

---

## 10. Shared Interaction Patterns

### 10.1 Field-level confidence

Each extracted field can be:

- **Confirmed by source** — shown normally.
- **High confidence** — eligible for automatic save if risk is low.
- **Uncertain** — highlighted and clarified individually.
- **Missing** — requested only if necessary for the intended action.
- **Derived deterministically** — labeled when useful, such as calculated mileage threshold.

The UI must never make the user reconfirm all fields because one field is uncertain.

### 10.2 Object Resolution

Resolution order:

1. Exact object ID from current context.
2. Exact alias match.
3. Normalized name/type match.
4. Recent and frequently referenced candidate weighting.
5. Ask the user when two or more plausible candidates remain.

Examples such as «سيارتي»، «اليارس»، and «يارس 2023» may refer to one object. Aliases are user-visible and editable in object settings.

Never create a duplicate silently when a plausible existing object is found.

### 10.3 Confirmation policy

Always confirm before:

- Linking to one of multiple plausible objects.
- A destructive action.
- A high-impact change derived from uncertain data.
- Saving sensitive data not clearly intended for storage.

Do not confirm again when:

- The user has already made the same choice in the current flow.
- Every required field is clear and the action is low risk.
- A deterministic rule can resolve the result safely.

### 10.4 Undo and correction

- Success surfaces Undo for a short convenient period.
- Later correction remains available from the event/source detail.
- Undo references the exact action and produces a reversal event/effect.
- If reversal affects a reminder, linked attachment, or current object state, preview those effects before confirmation when material.
- The system never guesses which recent action the user meant.

### 10.5 Duplicate handling

When a probable duplicate capture or event is detected:

> «يبدو أن هذي مسجلة قبل. تبغى أفتحها أو أحفظها كحدث جديد؟»

Actions: «افتح المسجل» / «احفظ كجديد» / «إلغاء».

### 10.6 Failure and recovery

No capture disappears. Failure states retain:

- Original source.
- Last completed processing stage.
- Safe retry option.
- Add-detail option.
- Keep-without-processing option.

Retries must not create duplicates.

### 10.7 Offline behavior

- Text drafts remain local until successfully submitted.
- Uploadable captures show queued state.
- Users see whether an item is local, uploading, processing, or saved.
- Closing the Mini App must not imply successful submission if the upload never completed.

---

## 11. Inbox Lifecycle

| State | Appears in default Inbox | Exit condition |
|---|---|---|
| Received | Briefly, if not immediately processing | Processing starts |
| Processing | Yes | Organized, needs confirmation, or failed |
| Needs confirmation | Yes, highest priority | User confirms, edits, rejects, or keeps for later |
| Failed | Yes | Retry succeeds, user keeps it, or explicitly deletes it |
| Organized | Brief recent section only | Auto-archives from default view |
| Kept unprocessed | Searchable/archive view | User reopens or deletes |

Inbox badges represent actionable items, not the total historical capture count.

---

## 12. Reminder Experience

### 12.1 Reminder types

- Date/time reminder.
- Recurring time reminder.
- Mileage/threshold reminder.
- Mixed reminder: date OR threshold, whichever occurs first.
- Renewal/expiry reminder with lead time.

### 12.2 Occurrence behavior

- Recurring time rules may have multiple future occurrences inside a bounded look-ahead window.
- Each generated occurrence has a uniqueness key to prevent duplicates.
- Mileage rules keep only one active threshold occurrence at a time.
- Snooze affects the occurrence, not the underlying recurrence rule unless the user explicitly edits the rule.
- Completion, snooze, dismissal, and delivery attempts remain auditable.

### 12.3 Reminder notification actions

Prefer a small, consistent set:

- «تم»
- «غفوة»
- «فتح»

Editing is available after opening the item rather than crowding every notification.

---

## 13. Ask MADAR Boundaries

Ask MADAR is **personal retrieval**, not an open-ended general chatbot.

Supported question families:

- «متى غيرت الزيت؟»
- «وين فاتورة التلفزيون؟»
- «كم صرفت هالشهر؟»
- «إيش ينتهي الشهر الجاي؟»
- «وش عندي اليوم؟»

Answer rules:

1. Use only authorized user data.
2. Link every material claim to one or more source records.
3. Distinguish recorded fact from deterministic calculation.
4. State when information is incomplete or conflicting.
5. Say «ما عندي شيء مسجل عن هذا» when no evidence exists.
6. Never silently answer with general web knowledge in V1.

---

## 14. Content and Voice

### 14.1 Voice character

- Saudi-friendly and natural, without forced slang.
- Calm, concise, and respectful.
- Helpful without sounding overly certain.
- Varies within a curated phrase bank, not random generation.

### 14.2 Trust language

Preferred:

- «هذا ثالث تغيير زيت مسجل عندي لليارس هالسنة.»
- «حسب الأشياء اللي سجلتها عندي…»
- «ما عندي تاريخ انتهاء واضح.»

Avoid:

- «أنت دائمًا…»
- «أكيد ضمانه سنتين» when the source does not say so.
- Claims implying MADAR knows events the user never recorded.

### 14.3 Key empty/error copy

| Situation | Recommended Arabic copy |
|---|---|
| No Ask result | «ما عندي شيء مسجل عن هذا.» |
| Processing continues | «تقدر تطلع، وبنبلغك إذا خلصت.» |
| Partial extraction | «فهمت أغلبها، وباقي أتأكد من شيء.» |
| Failed processing | «وصلتني، لكن ما قدرت أرتبها. تقدر تعيد المحاولة أو تضيف توضيح.» |
| Possible duplicate | «يبدو أن هذي مسجلة قبل.» |
| Empty Home | «أرسل موعد، فاتورة، أو شيء ودك ما تنساه.» |

---

## 15. Accessibility and Platform Rules

- Every gesture has a labeled tap alternative.
- Touch targets are at least 44×44 CSS pixels.
- State is never communicated by color alone.
- Text remains usable at increased system text size.
- Reduced Motion removes nonessential orbiting, pulsing, and scale transitions.
- Focus order follows RTL reading and logical task order.
- Screen reader labels describe state and action, not icon shape alone.
- Compact control respects Telegram safe areas, keyboard, and Back behavior.
- System Back closes the current overlay before leaving the current destination.
- Destructive actions require a clear label and confirmation.

---

## 16. Privacy and Trust UX

- Attachments are private by default and are not exposed through public links.
- Processing screens explain what is happening in plain language without exposing internal model details.
- Admin access to user content is not assumed; any exceptional support access must be controlled and audited.
- Sensitive identifiers are minimized in list views and notifications.
- Users can inspect the source behind an extracted fact.
- Export and account deletion are reachable from Settings.
- Operational logs should not include personal content unless strictly necessary.

---

## 17. Visual Direction for UI Phase

The UX architecture expects the approved visual language:

- Dark petrol-navy primary theme with warm paper text and restrained gold accent.
- Warm desert-day light theme using the same identity.
- Noto Kufi Arabic for brand/headings; IBM Plex Sans Arabic for body/UI.
- Central circle and sparse satellite controls as product chrome.
- Subtle orbit arcs, not glassmorphism or neon AI effects.
- No generic purple, gamification, streaks, badges, or equal-weight five-tab navigation.

Motion should communicate state and spatial direction; it should not decorate idle screens continuously.

---

## 18. Prototype and Usability Test Plan

### 18.1 Prototype scope

The first interactive prototype must include:

- All first ten screens.
- Supporting My Things, Object Timeline, Calendar, Ask MADAR, and Settings views.
- Hero and Compact control modes.
- Tap alternatives for the four directions.
- Success, clarification, duplicate, failure, offline, and Undo states.
- All five primary flows using realistic Arabic content.

### 18.2 Core test tasks

1. Record a voice reminder for next Thursday after Maghrib.
2. Find Inbox without being taught the direction.
3. Add a Yaris oil change and verify the next mileage reminder.
4. Upload a receipt and classify it as an asset with warranty.
5. Find when the Yaris oil was last changed and open the source.
6. Recover a failed PDF capture.
7. Complete the same tasks using tap alternatives without dragging.

### 18.3 Success criteria

- At least 80% of first-time users discover or understand directional navigation after the one-time coach mark.
- At least 90% complete primary capture without choosing a category first.
- At least 90% can find a failed capture and retry it.
- No participant believes closing Processing cancels the work.
- No participant mistakes Ask MADAR for a general-purpose chatbot after onboarding.
- Gesture error rate is low enough that direction remapping or a stronger tap alternative is not required.

---

## 19. MADAR Evaluation Set

Create a Saudi Arabic evaluation set before production AI use, containing at minimum:

- «ذكرني الخميس الجاي بعد المغرب».
- «غيرت زيت الموتر اليوم على ٥٣ ألف».
- Arabic and English receipts.
- Appointment screenshot.
- Insurance PDF.
- Forwarded Telegram message.
- Hijri and Gregorian dates.
- Object aliases such as «اليارس»، «يارس 2023»، and «سيارتي».
- Images with unclear warranty duration.
- Duplicate uploads and conflicting odometer values.

Measure:

- First-pass successful saves.
- Unnecessary clarification rate.
- Wrong-object link rate.
- Duplicate-object and duplicate-event rate.
- Reminder duplication rate.
- Field extraction accuracy by field, not only by capture.
- Source-link correctness in Ask MADAR answers.
- Recovery success after failed processing.

---

## 20. Product Decisions Frozen by This Architecture

The following become baseline decisions once this document is approved:

1. The central MADAR circle is the primary Home interaction and directional navigation control.
2. Tap starts voice; two satellites handle image/file and text.
3. Directions map to Calendar, My Things, Inbox, and Ask MADAR, with visible labels and tap alternatives.
4. Bot is the universal capture surface; Mini App is the organization and retrieval surface.
5. Inbox is an actionable queue, not a permanent archive.
6. Calendar is future-first, not future-only.
7. Ask MADAR retrieves the user's own data and cites sources; it is not a general chatbot.
8. Confirmation and confidence operate at field level.
9. Object Resolution prevents aliases from becoming duplicate objects.
10. Undo creates an explicit reversal tied to the exact action.
11. Failed captures are retained and recoverable.
12. Gesture accessibility, privacy, recovery, and Reduced Motion are V1 requirements.

---

## 21. Open Items Before Visual UI Freeze

Only these items remain deliberately open for prototype evidence:

1. Final physical placement of the tap-based destination alternative.
2. Whether the right/left mapping feels natural enough in RTL after testing.
3. Exact Hero control diameter across small phones and larger screens.
4. Whether live transcription during voice capture is reliable enough to show.
5. Default reminder lead times by document/subscription type.

These do not block wireframing. They must be resolved before high-fidelity UI is declared final.

---

## 22. Exit Criteria for UX Architecture Phase

Move to visual UI design only when:

- The information architecture is approved.
- The central control model and direction mapping are approved.
- The first ten screens and supporting screens are wireframed.
- The five primary flows are clickable end to end.
- Failure, ambiguity, duplicate, offline, accessibility, and Undo states are represented.
- At least one usability round validates the central gesture with first-time users.
- Open items in §21 have an owner and decision deadline.

After visual UI approval, engineering may begin from the approved Product/UX baseline. Production backend or frontend implementation must not begin from this document alone.

