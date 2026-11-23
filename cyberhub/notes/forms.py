from django import forms
from django.core.exceptions import ValidationError

from .models import Folder


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
        siblings = Folder.objects.filter(user=self.user, parent=self.parent, name__iexact=name)
        if siblings.exclude(pk=self.instance.pk).exists():
            raise ValidationError("A folder with this name already exists here.")
        return name
