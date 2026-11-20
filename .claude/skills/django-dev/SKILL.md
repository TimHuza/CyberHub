---
name: django-dev
description: Django and Python conventions for CyberHub — project layout, models, migrations, views, templates/Bootstrap, forms, code style, and testing. Use when writing, changing, or testing Django/Python code.
---

# Django development conventions

## Layout
- One app per component (`notes`, `quizzes`, `commands`, `mentor`, `progress`) + `core` for shared things (base template, Markdown renderer, Ollama helper). Names are proposals until approved.
- Per app: `models.py`, `views.py`, `urls.py` (with `app_name`), `forms.py`, `services.py` (public API for other apps), `admin.py`, `tests/`, `templates/<app>/`.
- Settings read secrets and environment values from `.env` (e.g. `django-environ` or `python-dotenv` — confirm choice with owner). `DEBUG` off in production config.
- Dependencies pinned in `requirements.txt`; always inside `venv/`.

## Models & migrations
- Every model: `__str__`, `Meta.ordering` where a natural order exists, `created_at`/`updated_at` where useful.
- Per-user data has `user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)`; always filter by `request.user`.
- Use `ForeignKey`/`ManyToMany` instead of storing IDs in text. Use `on_delete` deliberately.
- Migrations: small, named, committed. Never edit an applied migration. Running `migrate` needs owner approval.

## Views & templates
- Start with function-based views (easier to learn); class-based generic views when they clearly simplify.
- Keep views thin: validation in forms, business logic in `services.py`.
- `@login_required` on all user views; use `get_object_or_404(Model, pk=..., user=request.user)`.
- Templates extend `core/base.html`; Bootstrap 5 via static files or CDN (decide once). No inline `|safe` except on sanitized output.
- POST for anything that changes data; redirect after successful POST.

## Python style
- PEP 8, 4-space indent, descriptive names, type hints on service functions, short docstrings for non-obvious functions.
- Small functions; avoid premature abstraction. Comments explain *why*, not *what*.

## Testing
- Django `TestCase`; tests in `<app>/tests/`. Run with `python manage.py test [app]`.
- Test: model logic, services (especially cross-component interfaces), views (status, permissions — another user can't see my data), forms.
- Mock Ollama in tests — never call the real model in the test suite.
- Run `python manage.py check` and the relevant tests before calling a feature done.
