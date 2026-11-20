# PTM — Progress Tracking Manager

Records and summarizes learning activity from other components. AIM can query it only via `/ptm`.

## Initial metrics
- **NTT**: number of notes created; other note activity when useful.
- **QEF**: total quizzes, quizzes completed, total questions answered, correct answers, incorrect answers, results and performance history.
- **General**: overall activity, progress over time, learning statistics, areas needing more study (e.g. topics with low quiz scores).

## Implementation notes
- Prefer an **event log** (one row per activity: user, kind, source component, timestamp, small structured payload such as topic/score) and compute statistics from it. New metrics then usually need no new tables — just a new event kind or query.
- If queries become slow later, add cached aggregates — not before.
- PTM must not reach into other apps' models; components push events to PTM.

## Interfaces
- **Receives**: events from NTT, QEF (and future components) through one entry point.
- **Provides**: query functions (overall summary, per-topic stats, weak topics, quiz history) — used by PTM's own dashboard and by AIM's `/ptm` handler.
