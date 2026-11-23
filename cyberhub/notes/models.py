from django.conf import settings
from django.db import models
from django.db.models import Q


class Folder(models.Model):
    """A user's folder. No parent means it is a top-level folder."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="folders")
    parent = models.ForeignKey("self", on_delete=models.RESTRICT, null=True, blank=True, related_name="children")
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(fields=["user", "parent", "name"], name="unique_subfolder_name"),
            models.UniqueConstraint(fields=["user", "name"], condition=Q(parent__isnull=True), name="unique_top_level_folder_name"),
        ]

    def __str__(self) -> str:
        return self.name


class Note(models.Model):
    """A Markdown note. Raw Markdown is stored and rendered only when displayed."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notes")
    folder = models.ForeignKey(Folder, on_delete=models.RESTRICT, related_name="notes")
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(fields=["folder", "title"], name="unique_note_title_in_folder"),
        ]

    def __str__(self) -> str:
        return self.title
