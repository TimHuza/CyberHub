from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.history import MAX_ENTRIES, SESSION_KEY
from notes.models import Folder, Note

User = get_user_model()


class HistoryTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="owner", password="test-pass-123")
        cls.other_user = User.objects.create_user(username="other", password="test-pass-123")
        cls.first = Folder.objects.create(user=cls.user, name="First")
        cls.second = Folder.objects.create(user=cls.user, name="Second")

    def setUp(self):
        self.client.force_login(self.user)

    def open_notes(self):
        return self.client.get(reverse("notes:list"))

    def open_folder(self, folder):
        return self.client.get(reverse("notes:folder_detail", args=[folder.pk]))

    def back(self):
        return self.client.post(reverse("notes:history_back"), follow=True)

    def forward(self):
        return self.client.post(reverse("notes:history_forward"), follow=True)

    def assertButtons(self, response, back, forward):
        self.assertEqual(response.context["history"], {"can_go_back": back, "can_go_forward": forward})

    def test_buttons_appear_on_notes_and_folder_pages(self):
        for response in (self.open_notes(), self.open_folder(self.first)):
            self.assertContains(response, reverse("notes:history_back"))
            self.assertContains(response, reverse("notes:history_forward"))

    def test_both_disabled_before_opening_a_folder(self):
        response = self.open_notes()
        self.assertButtons(response, back=False, forward=False)
        self.assertContains(response, 'aria-label="Back" title="Back" disabled')
        self.assertContains(response, 'aria-label="Forward" title="Forward" disabled')

    def test_back_enabled_after_opening_a_folder(self):
        self.open_notes()
        self.assertButtons(self.open_folder(self.first), back=True, forward=False)

    def test_back_then_forward(self):
        self.open_notes()
        self.open_folder(self.first)

        response = self.back()
        self.assertEqual(response.request["PATH_INFO"], reverse("notes:list"))
        self.assertButtons(response, back=False, forward=True)

        response = self.forward()
        self.assertEqual(response.context["folder"], self.first)
        self.assertButtons(response, back=True, forward=False)

    def test_opening_different_folder_clears_forward(self):
        self.open_notes()
        self.open_folder(self.first)
        self.back()
        self.assertButtons(self.open_folder(self.second), back=True, forward=False)
        self.assertEqual(self.client.session[SESSION_KEY]["entries"], [None, self.second.pk])

    def test_refresh_does_not_add_an_entry(self):
        self.open_notes()
        self.open_folder(self.first)
        self.open_folder(self.first)
        self.assertEqual(self.client.session[SESSION_KEY]["entries"], [None, self.first.pk])

    def test_form_pages_are_not_recorded(self):
        self.open_notes()
        self.open_folder(self.first)
        self.client.get(reverse("notes:folder_create"))
        self.client.get(reverse("notes:subfolder_create", args=[self.first.pk]))
        self.client.get(reverse("notes:folder_rename", args=[self.first.pk]))
        self.assertEqual(self.client.session[SESSION_KEY]["entries"], [None, self.first.pk])

    def test_note_pages_are_not_recorded(self):
        note = Note.objects.create(user=self.user, folder=self.first, title="Ports", content="")
        self.open_notes()
        self.open_folder(self.first)
        self.client.get(reverse("notes:note_detail", args=[note.pk]))
        self.assertEqual(self.client.session[SESSION_KEY]["entries"], [None, self.first.pk])

    def test_deleted_folder_is_skipped(self):
        temporary = Folder.objects.create(user=self.user, name="Temporary")
        self.open_folder(self.first)
        self.open_folder(temporary)
        self.open_folder(self.second)
        temporary.delete()

        response = self.back()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["folder"], self.first)

    def test_deleting_current_folder_lands_without_404(self):
        temporary = Folder.objects.create(user=self.user, name="Temporary")
        self.open_notes()
        self.open_folder(temporary)
        response = self.client.post(reverse("notes:folder_delete", args=[temporary.pk]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertButtons(response, back=False, forward=False)

    def test_neighbours_merge_after_delete(self):
        temporary = Folder.objects.create(user=self.user, name="Temporary")
        self.open_notes()
        self.open_folder(temporary)
        self.open_notes()
        temporary.delete()
        self.assertButtons(self.open_notes(), back=False, forward=False)

    def test_history_length_is_capped(self):
        for _ in range(MAX_ENTRIES):
            self.open_folder(self.first)
            self.open_folder(self.second)
        self.assertEqual(len(self.client.session[SESSION_KEY]["entries"]), MAX_ENTRIES)

    def test_back_requires_post(self):
        self.assertEqual(self.client.get(reverse("notes:history_back")).status_code, 405)
        self.assertEqual(self.client.get(reverse("notes:history_forward")).status_code, 405)

    def test_anonymous_user_is_redirected(self):
        self.client.logout()
        self.assertEqual(self.client.post(reverse("notes:history_back")).status_code, 302)

    def test_other_users_folder_is_not_recorded(self):
        theirs = Folder.objects.create(user=self.other_user, name="Secret")
        self.open_notes()
        self.assertEqual(self.open_folder(theirs).status_code, 404)
        self.assertEqual(self.client.session[SESSION_KEY]["entries"], [None])
