from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class HomeViewTests(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(username="tim", password="a-long-test-password")
        self.client.force_login(user)

    def test_home_page_loads(self):
        response = self.client.get(reverse("core:home"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/home.html")
        self.assertTemplateUsed(response, "core/base.html")

    def test_home_page_shows_all_components(self):
        response = self.client.get(reverse("core:home"))

        for code in ["NTT", "QEF", "CLV", "AIM", "PTM"]:
            self.assertContains(response, code)

    def test_component_data_is_embedded_for_search(self):
        response = self.client.get(reverse("core:home"))

        self.assertContains(response, 'id="ch-components"')
        self.assertContains(response, "Note Taker")

    def test_home_shows_account_menu(self):
        response = self.client.get(reverse("core:home"))

        self.assertContains(response, 'data-bs-toggle="dropdown"')
        self.assertContains(response, "tim")
        for option in ["Profile", "Settings", "Sign Out"]:
            self.assertContains(response, option)
        self.assertContains(response, f'action="{reverse("accounts:logout")}"')


class HomeViewAnonymousTests(TestCase):
    def test_anonymous_user_is_redirected_to_signup(self):
        response = self.client.get(reverse("core:home"))

        expected = f"{reverse('accounts:signup')}?next={reverse('core:home')}"
        self.assertRedirects(response, expected)
