---
name: gt-msg
description: Analyze Git changes, propose a commit message, and after the owner's explicit approval commit and push to the current branch.
disable-model-invocation: true
---

# /gt-msg — safe commit & push

## 1. Inspect
Run the `git-commit` agent once. Don't repeat its inspection in the main conversation.

## 2. Stop early when needed
Explain the situation plainly and wait for instructions (do not commit) if the report shows:
- Nothing to commit → say so. Never create an empty commit.
- Merge/rebase in progress, conflicts, detached HEAD, or branch behind its upstream.
- No upstream → explain that the branch doesn't exist on GitHub yet and ask how to proceed (e.g. `git push -u origin <branch>`). Do not choose for the owner.

## 3. Present & ask
Show the agent's report: repo, branch, remote, latest tag, files to include, files excluded and why, the summary, and the proposed message. Then ask exactly:

> **Do you approve creating this commit and pushing it to GitHub?**

The owner may edit the message or the file list. Any edit means presenting again and asking again.
Rejection or no clear "yes" → do nothing and wait.

## 4. After approval
1. Re-check `git rev-parse --short HEAD` and `git status --porcelain=v1`. If they differ from the fingerprint, stop, show what changed, and ask again.
2. Stage only the approved files by explicit path (`git add -- <path> ...`). Never `git add .`, `-A`, or `-u`. If files were already staged but not approved, ask before unstaging them.
3. Check `git diff --cached --name-only` matches the approved list exactly.
4. `git commit` with the approved message only (no attribution lines). Use a heredoc or `-F` for multi-line messages.
5. `git push origin <current-branch>`, the branch from the report, never another one.
6. Verify with `git status -sb` (not ahead) and `git log -1 --oneline`. Report the commit hash, `origin/<branch>`, and the repo URL.
7. If a hook, commit or push fails, show the error, explain it, and stop. Don't retry with workarounds.

## Never
`--amend`, `--force`/`--force-with-lease`, `--no-verify`, `reset`, `rebase`, creating/deleting/moving tags or branches, switching branches, or committing secrets (`.env*`, keys, credentials, `db.sqlite3`). Version tags are only ever *suggested*, as a separate step the owner decides on.
