"""Back/Forward history for the Notes pages, kept in the user's session.

Each entry is a folder id, or None for the main Notes page.
"""

from .models import Folder

SESSION_KEY = "notes_history"
MAX_ENTRIES = 50


def _clean(user, entries: list, index: int) -> tuple[list, int]:
    """Drop folders that no longer exist and merge neighbours that became identical."""
    folder_ids = [entry for entry in entries if entry is not None]
    existing = set(Folder.objects.filter(user=user, pk__in=folder_ids).values_list("pk", flat=True))

    cleaned = []
    new_index = 0
    for position, entry in enumerate(entries):
        is_valid = entry is None or entry in existing
        if is_valid and (not cleaned or cleaned[-1] != entry):
            cleaned.append(entry)
        if position == index:
            # If the current page was removed, the nearest earlier page becomes current.
            new_index = max(len(cleaned) - 1, 0)
    return cleaned, new_index


def _load(request) -> tuple[list, int]:
    saved = request.session.get(SESSION_KEY, {"entries": [], "index": 0})
    return _clean(request.user, saved["entries"], saved["index"])


def _save(request, entries: list, index: int) -> None:
    state = {"entries": entries, "index": index}
    # Assigning marks the session as changed, so skip it when nothing moved to avoid a database write.
    if request.session.get(SESSION_KEY) != state:
        request.session[SESSION_KEY] = state


def record_visit(request, folder_id: int | None = None) -> dict:
    """Record the page being shown and return which history buttons are available."""
    entries, index = _load(request)

    # Same page as the current entry: a refresh, or the redirect after Back/Forward.
    if not entries or entries[index] != folder_id:
        entries = entries[: index + 1] + [folder_id]  # A new visit clears Forward history.
        entries = entries[-MAX_ENTRIES:]
        index = len(entries) - 1

    _save(request, entries, index)
    return {"can_go_back": index > 0, "can_go_forward": index < len(entries) - 1}


def move(request, step: int) -> int | None:
    """Move one step (-1 back, +1 forward) and return the folder id to show."""
    entries, index = _load(request)
    if not entries:
        return None

    if 0 <= index + step < len(entries):
        index += step
    _save(request, entries, index)
    return entries[index]
