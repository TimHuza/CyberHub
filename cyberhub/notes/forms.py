from django import forms
from django.core.exceptions import ValidationError

from .models import Folder, Note


class FolderForm(forms.ModelForm):
    """Create or rename a folder. Owner and parent come from the view, never the browser."""

    class Meta:
        model = Folder
        fields = ("name",)

    def __init__(self, *args, user, parent=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.parent = parent

    def clean_name(self):
        """Django skips the model's unique rules here because user and parent aren't form fields."""
        name = self.cleaned_data["name"]
        siblings = Folder.objects.filter(user=self.user, parent=self.parent, name=name)
        if siblings.exclude(pk=self.instance.pk).exists():
            raise ValidationError("A folder with this name already exists here.")
        return name


class NoteForm(forms.ModelForm):
    """Create a note. Owner and folder come from the view, never the browser."""

    # strip=False keeps leading spaces, because indentation has meaning in Markdown.
    content = forms.CharField(required=False, strip=False, widget=forms.Textarea)

    class Meta:
        model = Note
        fields = ("title", "content")

    def __init__(self, *args, folder, **kwargs):
        super().__init__(*args, **kwargs)
        self.folder = folder

    def clean_title(self):
        """Django skips the model's unique rule here because folder isn't a form field."""
        title = self.cleaned_data["title"]
        siblings = Note.objects.filter(folder=self.folder, title=title)
        if siblings.exclude(pk=self.instance.pk).exists():
            raise ValidationError("A note with this title already exists in this folder.")
        return title
