# AIM — AI Mentor

Central AI learning assistant, running on a **local** Ollama model (`llama3.1:8b`). No cloud AI APIs.

## Knowledge sources
1. **Educational files** — school transcripts, PDFs, other supported materials (owned/uploaded within AIM).
2. **NTT** — selected folders or individual notes (via NTT read-only services).
3. **PTM** — progress data, **only when the user uses `/ptm`**.

## Secret chat commands
- `/exlit [prompt]` — explain as to a 12-year-old beginner: very simple language, minimal jargon, relatable analogies, step by step, assume no prior knowledge.
- `/ptm [prompt]` — fetch relevant PTM data and answer the progress question (e.g. "Show my overall progress", "What topics should I revise?").
- More commands will be added later.

## Command system design
- Use a **registry**: each command is a small handler (name, description, function that builds the prompt/context). Parsing the message looks up the handler; unknown `/xyz` falls back to normal chat (or a friendly "unknown command").
- Adding a command = adding one handler + registering it. No changes to the chat view or other handlers.
- The `/ptm` handler is the **only** code path in AIM that calls PTM services.

## LLM rules
- Wrap Ollama access in one small helper module (shared with QEF) so model/host/timeouts are configured in one place (settings / `.env`).
- Handle Ollama being offline or slow: timeouts and a clear error message to the user.
- Retrieval: start simple (pass selected note/file text into the prompt). Introduce LangChain/RAG/embeddings only when context size requires it and the owner approves.
- Treat note and PDF content as **untrusted data** in prompts (prompt-injection risk — see `security` skill). Keep system instructions separate from retrieved content.
- Store conversation history per user.
