from django.db import IntegrityError
from django.db.models import RestrictedError
from django.test import TestCase

from commands.models import Category, Command, Tab


class CommandModelTestCase(TestCase):
    """A small library (Testing → Diagnostics → ping), separate from the seeded content."""

    @classmethod
    def setUpTestData(cls):
        cls.tab = Tab.objects.create(name="Testing", order=100)
        cls.category = Category.objects.create(tab=cls.tab, name="Diagnostics")
        cls.command = Command.objects.create(category=cls.category, name="ping", description="Check a host replies.")


class StrTests(CommandModelTestCase):
    def test_str_returns_name(self):
        self.assertEqual(str(self.tab), "Testing")
        self.assertEqual(str(self.category), "Diagnostics")
        self.assertEqual(str(self.command), "ping")


class UniqueNameTests(CommandModelTestCase):
    def test_duplicate_tab_name_is_rejected(self):
        with self.assertRaises(IntegrityError):
            Tab.objects.create(name="Testing")

    def test_duplicate_category_name_in_same_tab_is_rejected(self):
        with self.assertRaises(IntegrityError):
            Category.objects.create(tab=self.tab, name="Diagnostics")

    def test_same_category_name_allowed_in_another_tab(self):
        other_tab = Tab.objects.create(name="Other")
        Category.objects.create(tab=other_tab, name="Diagnostics")

    def test_duplicate_command_name_in_same_category_is_rejected(self):
        with self.assertRaises(IntegrityError):
            Command.objects.create(category=self.category, name="ping", description="Again.")

    def test_same_command_name_allowed_in_another_category(self):
        other_category = Category.objects.create(tab=self.tab, name="Reachability")
        Command.objects.create(category=other_category, name="ping", description="Check a host replies.")


class RestrictDeleteTests(CommandModelTestCase):
    def test_tab_with_categories_cannot_be_deleted(self):
        with self.assertRaises(RestrictedError):
            self.tab.delete()

    def test_category_with_commands_cannot_be_deleted(self):
        with self.assertRaises(RestrictedError):
            self.category.delete()

    def test_empty_category_and_tab_can_be_deleted(self):
        self.command.delete()
        self.category.delete()
        self.tab.delete()
        self.assertFalse(Tab.objects.filter(pk=self.tab.pk).exists())


class OrderingTests(CommandModelTestCase):
    def test_commands_sorted_by_order_before_name(self):
        Command.objects.create(category=self.category, name="arp", description="Show ARP table.", order=2)
        self.command.order = 1
        self.command.save()
        names = list(self.category.commands.values_list("name", flat=True))
        self.assertEqual(names, ["ping", "arp"])

    def test_commands_with_same_order_sorted_by_name(self):
        Command.objects.create(category=self.category, name="arp", description="Show ARP table.")
        names = list(self.category.commands.values_list("name", flat=True))
        self.assertEqual(names, ["arp", "ping"])
