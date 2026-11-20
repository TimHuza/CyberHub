# CyberHub

Personal Django web app supporting a 1.5-year Cybersecurity + AI education (IT Step Academy). Built gradually — one component at a time — as the owner's skills grow. It must be genuinely useful for studying and a clean GitHub portfolio piece.

## Components
| Code | Name | Purpose |
|---|---|---|
| NTT | Note Taker | Markdown notes in folders (Code/Preview editor) |
| QEF | Quiz Exam Forge | Quiz generation from NTT notes/folders or other material; results |
| CLV | Command Library Vault | Searchable commands in tabs → nested categories |
| AIM | AI Mentor | Local-LLM tutor over notes and school files; secret chat commands |
| PTM | Progress Tracking Manager | Records learning activity and statistics |

Details, data ownership and integration rules: **`cyberhub-components` skill**. Original requirements: `.claude/prompts/` (read-only source docs — never edit).

## Stack (preferences, not commitments)
Python · Django · HTML/CSS/Bootstrap · SQLite (PostgreSQL later) · Ollama `llama3.1:8b` (local only, no cloud AI APIs) · LangChain only if clearly needed · Docker and Git/GitHub later.
Never introduce a technology, package or service the owner has not approved.

## Architecture principles
- One Django app per component, plus a small `core` app for shared pieces.
- Components interact only through each other's service functions — never import another app's models to query/write them directly.
- Each piece of data has one owner component; others reference it, never copy it.
- AIM reads PTM data **only** when the user uses `/ptm`.
- Prefer simple, readable solutions over clever or "enterprise" patterns. No premature abstraction.

## Code quality & security
- Follow the **`django-dev` skill** when writing Django/Python code; **`security` skill** when handling user input, uploads, Markdown rendering, auth, or AI prompts.
- Small, focused changes. Tests for new logic. No secrets in code — use `.env` (never read or print it).

## Working with the owner
- The owner is learning. Explain important decisions in plain, beginner-friendly language and say *why*.
- Act as a technical partner: propose, explain trade-offs, recommend one option, let the owner decide.
- Help them understand the code rather than just dumping finished implementations.
- Ask focused questions; don't assume architecture decisions that haven't been made.

## Permission rules (CRITICAL)
Reading/listing/inspecting is allowed. **Any modification requires explicit approval first**: creating, writing, editing, renaming, moving, overwriting or deleting files; changing config; installing packages; running commands that change the project or environment (migrations, git commits, etc.).
Before each change: state what will change, which files, and why — then **stop and wait** for an explicit "yes".
- Approval covers only the exact action approved. Approval to create ≠ edit others; edit ≠ delete; a directory ≠ all files in it.
- Silence or earlier approvals are not permission. Never silently overwrite content.
- **Deletion** always needs its own separate approval, after explaining what and why.
- If unsure whether something modifies anything, ask.

## Token efficiency
- Read only files relevant to the task; don't re-read or re-summarize what is already in context.
- Load skills only when relevant; read only the needed component file inside `cyberhub-components`.
- Agents: `architect` for new-component or cross-component design; `reviewer` after a finished feature. Don't use agents for simple tasks or run several on one task.
- Be direct and concise. Correctness, security and the permission rules always outrank token savings.
