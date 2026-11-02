# MADAR integration review — 2026-11-02

Read-only review of published branch snapshots. No remote merge, deployment or production implementation was performed. This report is evidence and a proposed integration procedure, not owner approval or a new roadmap.

## Reviewed revisions

Official main: `8b3b5daef3a53f4578082c3531899c00c27c9c9b`.

| PR | Head SHA | Base | Scope |
|---|---|---|---|
| #4 | `9366a6ba82c9a0dca3c0d3605dbbbeff29947125` | main | Circle interruption fixes |
| #8 | `a35e236bc872215bc02d9630769e09bba30205ac` | #4 branch | Capture/invoice UI simulation, navigation, CI |
| #5 | `cff851ce952571ffd399e3d6e4c88aa7d33b2e21` | main | v2.2 product/prompt/schema/fixtures |
| #6 | `827a11c642a9dd7a08c797a271e2fb47dd49f531` | #5 branch | Python memory action experiment |
| #7 | `944784016b584759d849466865ac4c7b8ab7048a` | #6 branch | Context binding and integration design |

All five were open Draft at the checkpoint. Re-check heads and checks before integration. Local archives were extracted directly from fetched remote Git refs; locally authored commit IDs were not substituted for published revisions.

## Results rerun on published source

| Scope | Result | What this proves |
|---|---|---|
| PR #8 capture suite | PASS, 19 tests | Synthetic UI state and recovery logic |
| PR #8 flow suite | PASS | Circle/navigation fixture regressions under DOM stub |
| PR #8 design suite | PASS | Palette assertions, fixture interactions and original reference hashes |
| PR #7 Python tests | PASS, 38 tests | In-memory validation/action/context-binding policy |
| PR #7 demo | PASS, five proposals | Reviewed proposals execute/defer/clarify as documented |
| PR #7 v2.2 verifier | PASS, 46 outputs / 17 invalid proposals | Specification fixture consistency and unchanged original references |
| Automatic merge of #8 and #7 branch tips | FAIL | Content conflict in `ENGINEERING/MASTER_ROADMAP.md` |

Merge probe used `git merge-tree --write-tree` against those two remote tips. It wrote only local Git objects and returned a conflict; it did not alter a working tree, create a commit or merge a GitHub PR. The conflicting stages contain the independently appended UI and product/experiment checkpoints. No conflict was detected in executable files by that probe. This does not constitute an integrated runtime test or a completed conflict resolution.

## Findings requiring attention

1. **Roadmap integration conflict:** selecting “ours” or “theirs” wholesale loses one workstream's evidence. Preserve both sets of dated checkpoints. Mark earlier next-task paragraphs as historical; add one current integration checkpoint with the selected heads and outstanding qualification. Resolve the roadmap in an isolated integration branch, not through a direct main edit.
2. **UI and Python are independent:** browser invoice retention/link/reversal is a JavaScript simulation; the Python adapter defers invoice groups. UI PASS does not mean invoice ingestion/storage works. Preserve this boundary in user-facing copy and future acceptance criteria.
3. **CI coverage is split:** the current workflow exercises prototype JavaScript, not the Python experiment or product verifier. After selecting/combining source, extend CI to run all applicable commands and fail rather than silently skip missing expected files. Do not claim cross-layer protection from the current green UI check.
4. **No authenticated durable vertical slice:** trusted caller identity, session memory, no real provider, no transactional persistent store, no private original-file ingestion and no reminder delivery. Exact quotes and golden outputs do not prove model understanding.
5. **Device/accessibility evidence remains missing:** actual Mate X6 folded/unfolded, Telegram WebView, virtual keyboard, screen-reader announcements and 200% text were not run in this review. Prior desktop shell/layout results remain dated evidence, not new device qualification.
6. **Governance adoption remains pending:** no central-governance source/version was selected. Existing project AGENTS and v2.1/UX amendments govern this review; central adoption and branch-protection settings are not implied.

## Proposed integration procedure

- Review the UI chain in dependency order #4 → #8, and product/experiment chain #5 → #6 → #7. These arrows describe branch dependencies, not permission to merge.
- With owner merge authority, choose one isolated integration branch. Combine the selected chain tips without rewriting their histories. Resolve only the roadmap conflict by retaining dated evidence from both sides and adding a single current checkpoint. Review the complete combined diff, including AGENTS and all specification links.
- Re-run the three Node suites, Python unittest discovery, Python demo and product fixture verifier on the **combined** tree. Verify original reference hashes. Add the missing CI jobs on that branch; read actual hosted results. Verify the final preview uses the selected prototype bytes before any preview update.
- Execute the existing physical-device script and targeted accessibility checks. Record PASS/FAIL/NOT RUN independently. Design acceptance cannot turn an unexecuted test into PASS.
- Review a bounded authenticated durable **text** slice before production engineering; specify receipt/timeout/retry, source ownership, action identity, one-active-occurrence and reversal behavior. Keep real files/providers/delivery behind their own acceptance evidence.

The current review authorizes none of these merges or production changes. The owner’s original “no automatic merge” instruction still applies to these open PRs.
