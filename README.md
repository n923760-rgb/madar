# MADAR — مدار

> بس أرسلها لمدار.

Arabic-first personal organizer for the Saudi market, delivered through a Telegram Bot and Telegram Mini App.

**Current phase: Product UX/UI design.** Engineering begins after design approval.

## Product

Capture → Understand → Validate → Organize → Save → Remind → History → Ask.

Users send text, voice, images, screenshots, PDFs, files, and forwarded messages naturally. MADAR proposes versioned structured actions; deterministic validation and risk rules control saving. Clear low-risk inputs may save directly with Undo. Uncertain or sensitive details receive targeted clarification.

## Project documents

| Document | Status / use |
|---|---|
| [Product Master v2.1](madar-complete-master-prompt-v2.1.md) | Approved product baseline, original bytes preserved |
| [UX Architecture v1](MADAR-UX-Architecture-v1.md) | Approved UX reference; conflicts listed in the decision log |
| [Decision Log](UX-DECISION-LOG.md) | Baseline rules, conflicts, proposals, and open questions |
| [First Ten Screens Brief](UX-DESIGN-BRIEF-v0.1.md) | Draft layout and prototype requirements; not user-tested |
| [Documentation Baseline](PROJECT-BASELINE-2026-10-12.md) | Verified pre-import repository state and next work |
| [Source Manifest](SOURCE-MANIFEST.json) | Original reference sizes and SHA-256 hashes |
| [Project Instructions](AGENTS.md) | Scope, authority, and development boundaries |

## Planned engineering direction

Python/FastAPI, aiogram, PostgreSQL, SQLAlchemy/Alembic, Redis, private object storage, Next.js, TypeScript, and Tailwind. This documentation repository does not yet contain a production implementation.

## Governance

General reference: https://github.com/n923760-rgb/engineering-governance

Adoption is pending selection of an approved version and a separate project baseline/adoption task. Creating or publishing this repository does not qualify governance, an AI executor, or the product runtime.

## Next milestone

Render the first ten wireframes and supporting views, connect the five primary journeys, and validate Home gestures and the proposed internal capture composer before freezing the UI.

All prototype data must be synthetic. No credentials or real personal captures belong in this public repository.
