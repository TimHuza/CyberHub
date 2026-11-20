---
name: cyberhub-components
description: CyberHub component responsibilities, data ownership, and integration rules between NTT, QEF, CLV, AIM and PTM. Use when designing or implementing any component feature or any interaction between components. Per-component requirements are in separate files — read only the one you need.
---

# CyberHub components

## Responsibilities and data ownership
| Component | Django app (proposed) | Owns | Details |
|---|---|---|---|
| NTT | `notes` | Folders, Markdown notes | [ntt.md](ntt.md) |
| QEF | `quizzes` | Quizzes, questions, attempts/results | [qef.md](qef.md) |
| CLV | `commands` | Tabs, categories, commands | [clv.md](clv.md) |
| AIM | `mentor` | Conversations, uploaded educational files, secret commands | [aim.md](aim.md) |
| PTM | `progress` | Activity events, derived statistics | [ptm.md](ptm.md) |

App names and interface designs below are proposals until the owner approves them.

## Integrations
| Source → Destination | Purpose | Interface |
|---|---|---|
| NTT → QEF | Generate quizzes from notes/folders | NTT read-only service functions |
| NTT → AIM | Answer questions from notes | NTT read-only service functions |
| Educational files → AIM | Answer from school material | Owned by AIM |
| QEF → PTM | Quiz results and stats | PTM event recording |
| NTT → PTM | Note activity | PTM event recording |
| PTM → AIM | Progress info | PTM query functions — **only on `/ptm`** |

## Rules
1. **Talk through services, not models.** Each app exposes a `services.py` with plain functions (e.g. `notes.services.get_notes(folder_id=None, note_ids=None)`). Other apps call these; they never import another app's models to query or write.
2. **Single owner, no copies.** Consumers reference data by ID or read it at use time; they don't duplicate note contents or statistics into their own tables. (Storing a snapshot is acceptable only where history must be preserved, e.g. quiz questions as generated.)
3. **One way into PTM.** Components report activity through a single PTM entry point (e.g. `progress.services.record_event(kind, **data)` — or Django signals; decide with the owner). PTM must not need to know other components' internals.
4. **AIM ↔ PTM restriction.** AIM never fetches progress data automatically — only inside the `/ptm` command handler.
5. **Read-only by default.** Consumers (QEF, AIM) only read NTT data; they never modify notes.
6. **Extensible.** New components/integrations add a new app + its `services.py`, a row in the tables above, and a new `<component>.md` file here.
7. Data is per-user (`request.user`) even if there is one user today — keeps access control correct.
