from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import ProfileForm, ProfilePasswordForm, SignUpForm


def signup(request):
    """Create an account, log the new user in and open the dashboard."""
    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        form = SignUpForm()

    return render(request, "registration/signup.html", {"form": form})


@login_required
def settings_page(request):
    """Show the Settings page. Its controls are visual only until themes are built."""
    return render(request, "accounts/settings.html")


@login_required
def profile(request):
    """Let the logged-in user edit their own details."""
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile saved.")
            return redirect("accounts:profile")
    else:
        form = ProfileForm(instance=request.user)

    return render(request, "accounts/profile.html", {"form": form})


@login_required
def profile_password(request):
    """Let the logged-in user change their own password."""
    if request.method == "POST":
        form = ProfilePasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Changing the password ends the session unless we refresh it.
            update_session_auth_hash(request, user)
            messages.success(request, "Password changed.")
            return redirect("accounts:profile_password")
    else:
        form = ProfilePasswordForm(request.user)

    return render(request, "accounts/password.html", {"form": form})
