---
name: security
description: CyberHub security checklist — Markdown/XSS sanitization, file uploads, Django auth/CSRF, secrets, and prompt injection for the local LLM. Use when code handles user input, rendered Markdown, uploads, authentication, AI prompts, or settings; and when reviewing code.
---

# Security checklist

## Markdown & XSS (NTT, CLV, AIM output)
- Render Markdown server-side, then **sanitize** the HTML with an allowlist (e.g. `nh3` or `bleach`) before marking it safe. Never `|safe` raw user content or raw LLM output.
- Strip `javascript:` URLs, event handlers (`onerror=`…), `<script>`, `<iframe>`, `<style>`.
- If rendering client-side for Preview, sanitize there too (e.g. DOMPurify) — and keep server-side rendering authoritative.

## File uploads (AIM files, NTT images)
- Validate extension **and** content type; enforce a max size.
- Store outside templates/static, under `MEDIA_ROOT`, with generated filenames (never trust the uploaded name — path traversal).
- Serve only to the owning user. Never execute or `eval` uploaded content.
- Parse PDFs with a maintained library; handle parse failures gracefully.

## Django basics
- CSRF token on every POST form; don't use `@csrf_exempt`.
- `@login_required` + filter by `request.user` on every object lookup (prevents IDOR — seeing others' data by changing an ID).
- Use the ORM; never build SQL with string formatting. If raw SQL is unavoidable, use parameters.
- `SECRET_KEY`, DB credentials etc. only in `.env` (gitignored). `DEBUG=False` and proper `ALLOWED_HOSTS` outside development.
- Run `python manage.py check --deploy` before any deployment.

## LLM / prompt injection (AIM, QEF)
- Note text, PDFs and transcripts are **untrusted data**: put them in clearly delimited context blocks, separate from system instructions.
- The LLM must never trigger actions (DB writes, file access, PTM queries) by itself — only code paths chosen by the user's command (e.g. `/ptm`) do that.
- Validate structured LLM output (QEF JSON) before saving; treat it as user input.
- Keep Ollama bound to localhost; no cloud AI APIs without owner approval.
- Don't log full prompts containing personal school data at INFO level.

## Dependencies
- Install only approved packages; pin versions; prefer well-maintained libraries.
