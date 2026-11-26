from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from commands.models import Category, Command, Tab

User = get_user_model()


class CommandViewTestCase(TestCase):
    """The seeded library is in the test database, so pages are tested against real content."""

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="owner", password="test-pass-123")
        cls.git = Tab.objects.get(name="Git")

    def setUp(self):
        self.client.force_login(self.user)


class LoginRequiredTests(CommandViewTestCase):
    def test_anonymous_user_is_redirected_from_library(self):
        self.client.logout()
        response = self.client.get(reverse("commands:library"))
        self.assertEqual(response.status_code, 302)

    def test_anonymous_user_is_redirected_from_tab_page(self):
        self.client.logout()
        response = self.client.get(reverse("commands:tab_detail", args=[self.git.pk]))
        self.assertEqual(response.status_code, 302)


class LibraryPageTests(CommandViewTestCase):
    def test_shows_all_tabs_in_order(self):
        response = self.client.get(reverse("commands:library"))
        self.assertEqual(response.status_code, 200)
        names = [tab.name for tab in response.context["tabs"]]
        self.assertEqual(names, ["Python", "Networking", "Linux", "PowerShell", "Bash", "Git"])

    def test_home_link_is_marked_active(self):
        response = self.client.get(reverse("commands:library"))
        self.assertIsNone(response.context["active_tab"])
        self.assertContains(response, 'aria-current="page"', count=1)

    def test_cards_link_to_tab_pages(self):
        response = self.client.get(reverse("commands:library"))
        self.assertContains(response, reverse("commands:tab_detail", args=[self.git.pk]))

    def test_search_data_is_embedded_as_json(self):
        response = self.client.get(reverse("commands:library"))
        self.assertContains(response, 'id="clv-tabs"')
        self.assertEqual(len(response.context["search_data"]), 6)

    def test_command_search_data_has_every_command(self):
        response = self.client.get(reverse("commands:library"))
        self.assertContains(response, 'id="clv-commands"')
        self.assertEqual(len(response.context["command_search_data"]), Command.objects.count())

    def test_command_search_links_to_tab_page_and_row(self):
        command = Command.objects.get(name="git init")
        response = self.client.get(reverse("commands:library"))
        entry = next(item for item in response.context["command_search_data"] if item["name"] == "git init")
        self.assertEqual(entry["url"], reverse("commands:tab_detail", args=[self.git.pk]) + f"#command-{command.pk}")
        self.assertEqual(entry["location"], "Git › Setup & Configuration")

    def test_library_page_query_count_does_not_grow_with_commands(self):
        # Session + user + tabs + commands (with category and tab joined in).
        with self.assertNumQueries(4):
            self.client.get(reverse("commands:library"))


class TabPageTests(CommandViewTestCase):
    def test_shows_categories_and_commands(self):
        response = self.client.get(reverse("commands:tab_detail", args=[self.git.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Setup &amp; Configuration")
        self.assertContains(response, "git init")

    def test_active_tab_is_marked_in_sidebar(self):
        response = self.client.get(reverse("commands:tab_detail", args=[self.git.pk]))
        self.assertEqual(response.context["active_tab"], self.git)
        self.assertContains(response, 'aria-current="page"', count=1)

    def test_unknown_tab_returns_404(self):
        response = self.client.get(reverse("commands:tab_detail", args=[99999]))
        self.assertEqual(response.status_code, 404)

    def test_markdown_in_examples_is_sanitized(self):
        category = Category.objects.create(tab=self.git, name="Unsafe")
        Command.objects.create(category=category, name="evil", description="Test.", examples="<script>alert(1)</script>")
        response = self.client.get(reverse("commands:tab_detail", args=[self.git.pk]))
        self.assertNotContains(response, "<script>alert(1)</script>")

    def test_command_without_details_has_no_expand_button(self):
        category = Category.objects.create(tab=self.git, name="Plain")
        command = Command.objects.create(category=category, name="plain", description="No extras.")
        response = self.client.get(reverse("commands:tab_detail", args=[self.git.pk]))
        self.assertNotContains(response, f'data-bs-target="#command-{command.pk}"')
