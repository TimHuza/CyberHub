from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = "accounts"

# Django's built-in views handle password checking, sessions and CSRF for us.
urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("login/", auth_views.LoginView.as_view(redirect_authenticated_user=True), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("settings/", views.settings_page, name="settings"),
    path("profile/", views.profile, name="profile"),
    path("profile/password/", views.profile_password, name="profile_password"),
]
