from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class UserModelTests(TestCase):
    def test_custom_user_model_is_used(self):
        self.assertEqual(User._meta.label, "accounts.User")


class SignUpTests(TestCase):
    valid_data = {"username": "newuser", "password1": "a-long-test-password", "password2": "a-long-test-password"}

    def test_signup_page_links_to_login(self):
        response = self.client.get(reverse("accounts:signup"))

        self.assertTemplateUsed(response, "registration/signup.html")
        self.assertContains(response, f'<a class="link-primary" href="{reverse("accounts:login")}">account</a>')

    def test_valid_signup_creates_user_and_logs_in(self):
        response = self.client.post(reverse("accounts:signup"), self.valid_data)

        self.assertRedirects(response, reverse("core:home"))
        user = User.objects.get(username="newuser")
        self.assertEqual(self.client.session["_auth_user_id"], str(user.pk))

    def test_password_is_stored_hashed(self):
        self.client.post(reverse("accounts:signup"), self.valid_data)

        user = User.objects.get(username="newuser")
        self.assertNotEqual(user.password, "a-long-test-password")
        self.assertTrue(user.check_password("a-long-test-password"))

    def test_new_user_gets_no_admin_rights(self):
        self.client.post(reverse("accounts:signup"), {**self.valid_data, "is_staff": "on", "is_superuser": "on"})

        user = User.objects.get(username="newuser")
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_duplicate_username_is_rejected(self):
        User.objects.create_user(username="newuser", password="a-long-test-password")

        response = self.client.post(reverse("accounts:signup"), self.valid_data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.filter(username="newuser").count(), 1)

    def test_weak_password_is_rejected(self):
        data = {"username": "newuser", "password1": "12345", "password2": "12345"}

        response = self.client.post(reverse("accounts:signup"), data)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="newuser").exists())

    def test_logged_in_user_is_sent_to_dashboard(self):
        self.client.force_login(User.objects.create_user(username="tim", password="a-long-test-password"))

        response = self.client.get(reverse("accounts:signup"))

        self.assertRedirects(response, reverse("core:home"))


class AuthPageLayoutTests(TestCase):
    def test_auth_pages_hide_sidebar_and_search(self):
        for url_name in ["accounts:signup", "accounts:login"]:
            with self.subTest(url_name=url_name):
                response = self.client.get(reverse(url_name))

                self.assertNotContains(response, 'id="sidebar"')
                self.assertNotContains(response, 'role="search"')
                self.assertNotContains(response, "Ask AIM")
                self.assertNotContains(response, "core/js/search.js")

    def test_login_page_links_to_signup(self):
        response = self.client.get(reverse("accounts:login"))

        self.assertContains(response, f'<a class="link-primary" href="{reverse("accounts:signup")}">account</a>')


class LoginLogoutTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tim", password="a-long-test-password")

    def test_login_page_loads(self):
        response = self.client.get(reverse("accounts:login"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")

    def test_valid_login_redirects_to_dashboard(self):
        response = self.client.post(reverse("accounts:login"), {"username": "tim", "password": "a-long-test-password"})

        self.assertRedirects(response, reverse("core:home"))

    def test_wrong_password_shows_error(self):
        response = self.client.post(reverse("accounts:login"), {"username": "tim", "password": "wrong"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Wrong username or password.")
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_logout_requires_post(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("accounts:logout"))

        self.assertEqual(response.status_code, 405)

    def test_logout_logs_user_out(self):
        self.client.force_login(self.user)

        response = self.client.post(reverse("accounts:logout"))

        self.assertRedirects(response, reverse("accounts:login"))
        self.assertNotIn("_auth_user_id", self.client.session)


class SettingsPageTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tim", password="a-long-test-password")

    def test_anonymous_user_is_redirected(self):
        url = reverse("accounts:settings")

        response = self.client.get(url)

        self.assertRedirects(response, f'{reverse("accounts:signup")}?next={url}')

    def test_page_loads_for_logged_in_user(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("accounts:settings"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/settings.html")

    def test_page_shows_appearance_controls(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("accounts:settings"))

        self.assertContains(response, 'id="color-mode-light"')
        self.assertContains(response, 'id="color-mode-dark"')
        self.assertContains(response, 'id="font-size"')
        self.assertContains(response, 'value="16" min="12" max="24"')

    def test_page_hides_sidebar_and_search(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("accounts:settings"))

        self.assertNotContains(response, 'id="sidebar"')
        self.assertNotContains(response, 'role="search"')
        self.assertNotContains(response, "Ask AIM")
        self.assertNotContains(response, "core/js/search.js")

    def test_account_menu_links_to_settings(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("core:home"))

        self.assertContains(response, f'<a class="dropdown-item" href="{reverse("accounts:settings")}">Settings</a>')

    def test_color_mode_defaults_to_dark(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("accounts:settings"))

        self.assertEqual(self.user.color_mode, User.ColorMode.DARK)
        self.assertContains(response, 'data-bs-theme="dark"')

    def test_logged_out_pages_use_dark(self):
        response = self.client.get(reverse("accounts:login"))

        self.assertContains(response, 'data-bs-theme="dark"')

    def test_saving_light_mode_applies_it(self):
        self.client.force_login(self.user)
        url = reverse("accounts:settings")

        response = self.client.post(url, {"color_mode": "light", "font_size": 16}, follow=True)

        self.assertRedirects(response, url)
        self.user.refresh_from_db()
        self.assertEqual(self.user.color_mode, User.ColorMode.LIGHT)
        self.assertContains(response, 'data-bs-theme="light"')
        self.assertContains(response, 'value="light" autocomplete="off" checked')

    def test_switching_back_to_dark_is_saved(self):
        self.user.color_mode = User.ColorMode.LIGHT
        self.user.save()
        self.client.force_login(self.user)

        self.client.post(reverse("accounts:settings"), {"color_mode": "dark", "font_size": 16})

        self.user.refresh_from_db()
        self.assertEqual(self.user.color_mode, User.ColorMode.DARK)

    def test_invalid_color_mode_is_ignored(self):
        self.client.force_login(self.user)

        self.client.post(reverse("accounts:settings"), {"color_mode": "purple", "font_size": 16})

        self.user.refresh_from_db()
        self.assertEqual(self.user.color_mode, User.ColorMode.DARK)

    def test_anonymous_user_cannot_save_color_mode(self):
        url = reverse("accounts:settings")

        response = self.client.post(url, {"color_mode": "light"})

        self.assertRedirects(response, f'{reverse("accounts:signup")}?next={url}')
        self.user.refresh_from_db()
        self.assertEqual(self.user.color_mode, User.ColorMode.DARK)

    def test_font_size_defaults_to_16(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("core:home"))

        self.assertEqual(self.user.font_size, 16)
        self.assertContains(response, 'style="font-size: 16px;"')

    def test_logged_out_pages_use_default_font_size(self):
        response = self.client.get(reverse("accounts:login"))

        self.assertContains(response, 'style="font-size: 16px;"')

    def test_font_size_limits_can_be_saved(self):
        self.client.force_login(self.user)

        for size in (12, 24):
            with self.subTest(size=size):
                response = self.client.post(reverse("accounts:settings"), {"color_mode": "dark", "font_size": size}, follow=True)

                self.user.refresh_from_db()
                self.assertEqual(self.user.font_size, size)
                self.assertContains(response, f'style="font-size: {size}px;"')

    def test_invalid_font_size_is_ignored(self):
        self.client.force_login(self.user)

        for size in ("11", "25", "abc", "", "16px;color:red"):
            with self.subTest(size=size):
                self.client.post(reverse("accounts:settings"), {"color_mode": "light", "font_size": size})

                self.user.refresh_from_db()
                self.assertEqual(self.user.font_size, 16)
                self.assertEqual(self.user.color_mode, User.ColorMode.DARK)


class ProfilePageTests(TestCase):
    password = "a-long-test-password"

    def setUp(self):
        self.user = User.objects.create_user(username="tim", password=self.password, email="old@example.com")
        self.url = reverse("accounts:profile")
        self.client.force_login(self.user)

    def post(self, **changes):
        data = {"first_name": "", "username": "tim", "email": "old@example.com"}
        return self.client.post(self.url, {**data, **changes})

    def test_anonymous_user_is_redirected(self):
        self.client.logout()

        response = self.client.get(self.url)

        self.assertRedirects(response, f'{reverse("accounts:signup")}?next={self.url}')

    def test_page_hides_sidebar_and_search(self):
        response = self.client.get(self.url)

        self.assertTemplateUsed(response, "accounts/profile.html")
        self.assertNotContains(response, 'id="sidebar"')
        self.assertNotContains(response, 'role="search"')
        self.assertNotContains(response, "Ask AIM")

    def test_page_has_no_password_fields(self):
        response = self.client.get(self.url)

        self.assertNotContains(response, 'type="password"')

    def test_page_links_to_password_tab(self):
        response = self.client.get(self.url)

        self.assertContains(response, f'href="{reverse("accounts:profile_password")}"')
        self.assertContains(response, "CyberHub Password")

    def test_account_menu_links_to_profile(self):
        response = self.client.get(reverse("core:home"))

        self.assertContains(response, f'<a class="dropdown-item" href="{self.url}">Profile</a>')

    def test_saves_name_username_and_email(self):
        response = self.post(first_name="Tim", username="timnew", email="new@example.com")

        self.assertRedirects(response, self.url)
        self.user.refresh_from_db()
        self.assertEqual((self.user.first_name, self.user.username, self.user.email), ("Tim", "timnew", "new@example.com"))

    def test_blank_username_keeps_current(self):
        self.post(username="")

        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "tim")

    def test_blank_email_clears_it(self):
        self.post(email="")

        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "")

    def test_invalid_email_is_rejected(self):
        response = self.post(email="not-an-email")

        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "old@example.com")

    def test_duplicate_username_is_rejected_ignoring_case(self):
        User.objects.create_user(username="other", password=self.password)

        response = self.post(username="OTHER")

        self.assertContains(response, "A user with that username already exists.")
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "tim")

    def test_cannot_grant_admin_rights(self):
        self.post(is_staff="on", is_superuser="on")

        self.user.refresh_from_db()
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)

    def test_only_own_account_changes(self):
        other = User.objects.create_user(username="other", password=self.password, email="other@example.com")

        self.post(first_name="Changed", id=other.pk)

        other.refresh_from_db()
        self.assertEqual(other.first_name, "")

    def test_password_sent_to_profile_is_ignored(self):
        self.post(old_password=self.password, new_password1="another-strong-passphrase-42", new_password2="another-strong-passphrase-42")

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(self.password))


class ProfilePasswordTests(TestCase):
    password = "a-long-test-password"
    new_password = "another-strong-passphrase-42"

    def setUp(self):
        self.user = User.objects.create_user(username="tim", password=self.password)
        self.url = reverse("accounts:profile_password")
        self.client.force_login(self.user)

    def post(self, **changes):
        data = {"new_password1": self.new_password, "new_password2": self.new_password}
        return self.client.post(self.url, {**data, **changes})

    def assertPasswordUnchanged(self):
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(self.password))

    def test_anonymous_user_is_redirected(self):
        self.client.logout()

        response = self.client.get(self.url)

        self.assertRedirects(response, f'{reverse("accounts:signup")}?next={self.url}')

    def test_page_hides_sidebar_and_search(self):
        response = self.client.get(self.url)

        self.assertTemplateUsed(response, "accounts/password.html")
        self.assertNotContains(response, 'id="sidebar"')
        self.assertNotContains(response, 'role="search"')
        self.assertNotContains(response, "Ask AIM")

    def test_page_never_shows_password_hash(self):
        response = self.client.get(self.url)

        self.assertNotContains(response, self.user.password)

    def test_current_password_is_readonly_dots(self):
        response = self.client.get(self.url)

        self.assertContains(response, 'id="password-set" value="••••••••••" autocomplete="off" readonly')
        self.assertNotContains(response, 'name="old_password"')

    def test_only_new_password_has_eye_button(self):
        response = self.client.get(self.url)

        self.assertContains(response, "data-password-toggle=", count=1)
        self.assertContains(response, 'data-password-toggle="id_new_password1"')

    def test_password_change_keeps_user_logged_in(self):
        response = self.post()

        self.assertRedirects(response, self.url)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(self.new_password))
        self.assertEqual(self.client.get(reverse("core:home")).status_code, 200)

    def test_mismatched_confirmation_shows_error(self):
        response = self.post(new_password2="a-different-passphrase-99")

        self.assertContains(response, "Passwords do not match.")
        self.assertPasswordUnchanged()

    def test_weak_new_password_is_rejected(self):
        response = self.post(new_password1="12345", new_password2="12345")

        self.assertEqual(response.status_code, 200)
        self.assertPasswordUnchanged()

    def test_passwords_are_not_echoed_after_error(self):
        response = self.post(new_password2="a-different-passphrase-99")

        self.assertNotContains(response, "a-different-passphrase-99")
        self.assertNotContains(response, self.new_password)
