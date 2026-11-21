from django import forms
from django.contrib.auth.forms import SetPasswordForm, UserCreationForm, UsernameField
from django.core.exceptions import ValidationError

from .models import User


class SignUpForm(UserCreationForm):
    """Django's sign-up form, pointed at our custom User.

    The parent class already checks that the passwords match, runs the
    password validators from settings, and stores the password hashed.
    """

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username",)


class ProfileForm(forms.ModelForm):
    """Edit your own details.

    Only the fields listed in Meta can be changed, so a crafted request
    can't set things like is_staff.
    """

    class Meta:
        model = User
        fields = ("first_name", "username", "email")
        field_classes = {"username": UsernameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].required = False

    def clean_username(self):
        """Blank keeps the current username, because every account needs one to log in."""
        username = self.cleaned_data["username"] or self.instance.username
        # Same case-insensitive rule as sign-up, so "Tim" and "tim" can't both exist.
        taken = User.objects.filter(username__iexact=username).exclude(pk=self.instance.pk)
        if taken.exists():
            raise ValidationError("A user with that username already exists.")
        return username


class ProfilePasswordForm(SetPasswordForm):
    """Django's set-password form with our wording for a mismatch.

    The owner chose not to ask for the current password here. The parent
    class runs the password validators and stores the new password hashed.
    """

    error_messages = {**SetPasswordForm.error_messages, "password_mismatch": "Passwords do not match."}
