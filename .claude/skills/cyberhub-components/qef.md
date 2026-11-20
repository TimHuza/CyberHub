# QEF — Quiz Exam Forge

Generates quizzes for exam preparation and records results.

## Requirements
- Sources (selecting a source is **optional**):
  - One or more individual NTT notes.
  - Entire NTT folders.
  - Other supported educational files (when appropriate).
  - No source — quiz generated from a topic/prompt alone.
- Flow: open QEF → optionally select NTT folder(s)/note(s) → QEF analyzes material → generates quiz → user takes it → results stored.
- Question types (initial ideas): multiple choice, true/false; difficulty levels.
- Review incorrect answers after a quiz.

## Implementation notes
- Generation uses the local Ollama model (shared AI helper, see `aim.md` for LLM rules). Ask the model for **structured output (JSON)** and validate it before saving; handle malformed responses gracefully.
- Long folders may exceed the model's context — plan for chunking/summarizing.
- Store generated questions with the quiz so results stay meaningful even if source notes change later.
- Track a quiz's state: created vs. completed.

## Interfaces
- **Consumes**: NTT read-only services.
- **Reports to PTM**: quiz created, quiz completed (questions answered, correct, incorrect, score, topic/source).
