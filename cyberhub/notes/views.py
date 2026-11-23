from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import RestrictedError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from core.markdown import render_markdown

from . import history
from .forms import FolderForm, NoteForm
from .models import Folder, Note


def _get_user_folder(user, pk):
    """Return the user's folder, or 404 so other users can't even tell it exists."""
    return get_object_or_404(Folder, pk=pk, user=user)


def _breadcrumbs(folder):
    """Return the folder's path from the top level down to the folder itself."""
    path = []
    while folder is not None:
        path.insert(0, folder)
        folder = folder.parent
    return path


def _redirect_to_folder(folder):
    """Go to the folder, or to the top-level list when there is no folder."""
    if folder is None:
        return redirect("notes:list")
    return redirect("notes:folder_detail", pk=folder.pk)


@login_required
def folder_list(request):
    """Show the user's top-level folders."""
    folders = Folder.objects.filter(user=request.user, parent=None)
    context = {"folders": folders, "history": history.record_visit(request)}
    return render(request, "notes/folder_list.html", context)


@login_required
def folder_detail(request, pk):
    """Show one folder with its subfolders and notes."""
    folder = _get_user_folder(request.user, pk)
    context = {"folder": folder, "folders": folder.children.all(), "notes": folder.notes.all(), "breadcrumbs": _breadcrumbs(folder), "history": history.record_visit(request, folder.pk)}
    return render(request, "notes/folder_list.html", context)


def _redirect_to_history_entry(folder_id):
    """Go to a history entry, where None means the main Notes page."""
    if folder_id is None:
        return redirect("notes:list")
    return redirect("notes:folder_detail", pk=folder_id)


@login_required
@require_POST
def history_back(request):
    """Go to the previous page in the Notes history."""
    return _redirect_to_history_entry(history.move(request, -1))


@login_required
@require_POST
def history_forward(request):
    """Go to the next page in the Notes history."""
    return _redirect_to_history_entry(history.move(request, 1))


@login_required
def folder_create(request, parent_id=None):
    """Create a top-level folder, or a subfolder when parent_id is in the URL."""
    parent = _get_user_folder(request.user, parent_id) if parent_id else None

    if request.method == "POST":
        form = FolderForm(request.POST, user=request.user, parent=parent)
        if form.is_valid():
            folder = form.save(commit=False)
            folder.user = request.user
            folder.parent = parent
            folder.save()
            messages.success(request, "Folder created.")
            return _redirect_to_folder(parent)
    else:
        form = FolderForm(user=request.user, parent=parent)

    context = {"form": form, "heading": "New folder", "button": "Create", "cancel_folder": parent}
    return render(request, "notes/folder_form.html", context)


@login_required
def folder_rename(request, pk):
    """Change a folder's name. Its place in the tree stays the same."""
    folder = _get_user_folder(request.user, pk)

    if request.method == "POST":
        form = FolderForm(request.POST, instance=folder, user=request.user, parent=folder.parent)
        if form.is_valid():
            form.save()
            messages.success(request, "Folder renamed.")
            return _redirect_to_folder(folder)
    else:
        form = FolderForm(instance=folder, user=request.user, parent=folder.parent)

    context = {"form": form, "heading": "Rename folder", "button": "Save", "cancel_folder": folder}
    return render(request, "notes/folder_form.html", context)


@login_required
@require_POST
def folder_delete(request, pk):
    """Delete an empty folder. RESTRICT on the models blocks deleting one with contents."""
    folder = _get_user_folder(request.user, pk)
    parent = folder.parent

    try:
        folder.delete()
    except RestrictedError:
        messages.error(request, "This folder isn't empty. Move or delete its contents first.")
        return _redirect_to_folder(folder)

    messages.success(request, "Folder deleted.")
    return _redirect_to_folder(parent)


@login_required
def note_create(request, folder_id):
    """Create a note inside one of the user's folders."""
    folder = _get_user_folder(request.user, folder_id)

    if request.method == "POST":
        form = NoteForm(request.POST, folder=folder)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.folder = folder
            note.save()
            messages.success(request, "Note created.")
            return redirect("notes:note_detail", pk=note.pk)
    else:
        form = NoteForm(folder=folder)

    context = {"form": form, "folder": folder, "heading": "New note", "button": "Create", "cancel_url": reverse("notes:folder_detail", args=[folder.pk])}
    return render(request, "notes/note_form.html", context)


@login_required
def note_edit(request, pk):
    """Change a note's title or content. It stays in the same folder."""
    note = get_object_or_404(Note, pk=pk, user=request.user)

    if request.method == "POST":
        form = NoteForm(request.POST, instance=note, folder=note.folder)
        if form.is_valid():
            form.save()
            messages.success(request, "Note saved.")
            return redirect("notes:note_detail", pk=note.pk)
    else:
        form = NoteForm(instance=note, folder=note.folder)

    context = {"form": form, "folder": note.folder, "heading": "Edit note", "button": "Save", "cancel_url": reverse("notes:note_detail", args=[note.pk])}
    return render(request, "notes/note_form.html", context)


@login_required
@require_POST
def note_delete(request, pk):
    """Delete one of the user's notes and return to its folder."""
    note = get_object_or_404(Note, pk=pk, user=request.user)
    folder = note.folder
    note.delete()
    messages.success(request, "Note deleted.")
    return _redirect_to_folder(folder)


@login_required
@require_POST
def note_preview(request):
    """Return sanitized HTML for the Preview tab. Nothing is saved."""
    return HttpResponse(render_markdown(request.POST.get("content", "")))


@login_required
def note_detail(request, pk):
    """Show one note. Returns 404 for another user's note."""
    note = get_object_or_404(Note, pk=pk, user=request.user)
    context = {"note": note, "rendered_content": render_markdown(note.content), "breadcrumbs": _breadcrumbs(note.folder)}
    return render(request, "notes/note_detail.html", context)
