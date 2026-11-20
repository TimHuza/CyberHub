# NTT — Note Taker

Markdown-only note management. Main educational source for QEF and AIM.

## Requirements
- Notes live in **folders**; user can create, rename and manage folders. (Nested folders: undecided — ask.)
- Opening a note shows **Preview** (rendered Markdown) by default.
- **Edit** button opens the editor with two tabs, like GitHub PRs/issues:
  - **Code** — write raw Markdown.
  - **Preview** — rendered result.
- Note list shows each note's **creation date under its name**.
- Supports standard Markdown: headings, code blocks (with syntax highlighting), tables, images, lists, links.

## Implementation notes
- Store raw Markdown in the DB; render to HTML on display. Rendered HTML **must be sanitized** (see `security` skill) — notes can contain arbitrary HTML.
- Preview tab: either a small server endpoint that renders + sanitizes, or a client-side renderer with sanitization. Same renderer for both views so they match.
- Images: decide with the owner between uploaded files (validated) and external links.

## Interfaces
- **Provides (read-only)** to QEF/AIM: list folders, get notes by folder or by IDs, returning title + raw Markdown + metadata.
- **Reports to PTM**: note created (and later edited/deleted if useful).
