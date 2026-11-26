from django.test import TestCase

from commands.models import Category, Command, Tab

# The test database runs every migration, so the seeded library is present here too.


class SeedLibraryTests(TestCase):
    def test_six_tabs_in_agreed_order(self):
        names = list(Tab.objects.values_list("name", flat=True))
        self.assertEqual(names, ["Python", "Networking", "Linux", "PowerShell", "Bash", "Git"])

    def test_every_tab_has_a_description_and_categories(self):
        for tab in Tab.objects.all():
            with self.subTest(tab=tab.name):
                self.assertTrue(tab.description)
                self.assertTrue(tab.categories.exists())

    def test_every_category_has_a_description_and_commands(self):
        for category in Category.objects.all():
            with self.subTest(category=category.name):
                self.assertTrue(category.description)
                self.assertTrue(category.commands.exists())

    def test_every_command_has_a_description(self):
        self.assertFalse(Command.objects.filter(description="").exists())

    def test_git_categories_in_agreed_order(self):
        git = Tab.objects.get(name="Git")
        names = list(git.categories.values_list("name", flat=True))
        self.assertEqual(names, ["Setup & Configuration", "Staging & Snapshots", "Branching", "Remote (GitHub)"])
