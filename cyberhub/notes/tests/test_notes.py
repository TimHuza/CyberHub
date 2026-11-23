from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Folder, Note

User = get_user_model()


class NoteTestCase(TestCase):
    """Two users, so every test can check that one can't touch the other's data."""

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="owner", password="test-pass-123")
        cls.other_user = User.objects.create_user(username="other", password="test-pass-123")
        cls.folder = Folder.objects.create(user=cls.user, name="Networking")
        cls.other_folder = Folder.objects.create(user=cls.other_user, name="Secret")

    def setUp(self):
        self.client.force_login(self.user)

    def make_note(self, title="Subnetting", content="Some text"):
        return Note.objects.create(user=self.user, folder=self.folder, title=title, content=content)


class NoteCreateTests(NoteTestCase):
    def test_anonymous_user_is_redirected(self):
        self.client.logout()
        response = self.client.get(reverse("notes:note_create", args=[self.folder.pk]))
        self.assertEqual(response.status_code, 302)

    def test_create_note_saves_owner_and_folder(self):
        url = reverse("notes:note_create", args=[self.folder.pk])
        response = self.client.post(url, {"title": "Subnetting", "content": "# Hello"})
        note = Note.objects.get()
        self.assertRedirects(response, reverse("notes:note_detail", args=[note.pk]))
        self.assertEqual((note.user, note.folder, note.content), (self.user, self.folder, "# Hello"))

    def test_content_keeps_leading_indentation(self):
        url = reverse("notes:note_create", args=[self.folder.pk])
        self.client.post(url, {"title": "Code", "content": "    indented code"})
        self.assertEqual(Note.objects.get().content, "    indented code")

    def test_title_is_required(self):
        url = reverse("notes:note_create", args=[self.folder.pk])
        response = self.client.post(url, {"title": "   ", "content": "Text"})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Note.objects.exists())

    def test_duplicate_title_in_same_folder_is_rejected(self):
        self.make_note()
        url = reverse("notes:note_create", args=[self.folder.pk])
        response = self.client.post(url, {"title": "Subnetting", "content": ""})
        self.assertContains(response, "already exists")
        self.assertEqual(Note.objects.count(), 1)

    def test_same_title_in_different_folder_is_allowed(self):
        self.make_note()
        second = Folder.objects.create(user=self.user, name="Security")
        self.client.post(reverse("notes:note_create", args=[second.pk]), {"title": "Subnetting", "content": ""})
        self.assertEqual(Note.objects.count(), 2)

    def test_database_blocks_duplicate_title(self):
        self.make_note()
        with self.assertRaises(IntegrityError), transaction.atomic():
            self.make_note()

    def test_cannot_create_note_in_other_users_folder(self):
        url = reverse("notes:note_create", args=[self.other_folder.pk])
        response = self.client.post(url, {"title": "Sneaky", "content": ""})
        self.assertEqual(response.status_code, 404)
        self.assertFalse(Note.objects.exists())

    def test_browser_cannot_choose_owner_or_folder(self):
        url = reverse("notes:note_create", args=[self.folder.pk])
        self.client.post(url, {"title": "Mine", "content": "", "user": self.other_user.pk, "folder": self.other_folder.pk})
        note = Note.objects.get()
        self.assertEqual((note.user, note.folder), (self.user, self.folder))


class NoteDisplayTests(NoteTestCase):
    def test_folder_lists_its_notes_with_date(self):
        note = self.make_note()
        response = self.client.get(reverse("notes:folder_detail", args=[self.folder.pk]))
        self.assertEqual(list(response.context["notes"]), [note])
        self.assertContains(response, note.created_at.strftime("%Y"))

    def test_owner_can_open_note(self):
        note = self.make_note()
        response = self.client.get(reverse("notes:note_detail", args=[note.pk]))
        self.assertContains(response, "Some text")

    def test_cannot_open_other_users_note(self):
        note = Note.objects.create(user=self.other_user, folder=self.other_folder, title="Private")
        response = self.client.get(reverse("notes:note_detail", args=[note.pk]))
        self.assertEqual(response.status_code, 404)

    def test_title_and_content_are_escaped(self):
        note = self.make_note(title="<script>alert(1)</script>", content="<img src=x onerror=alert(2)>")
        response = self.client.get(reverse("notes:note_detail", args=[note.pk]))
        self.assertNotContains(response, "<script>alert(1)</script>")
        self.assertNotContains(response, "<img src=x")

    def test_note_content_is_rendered_as_markdown(self):
        note = self.make_note(content="# Heading")
        response = self.client.get(reverse("notes:note_detail", args=[note.pk]))
        self.assertContains(response, "<h1>Heading</h1>", html=True)

    def test_script_in_content_is_not_active(self):
        note = self.make_note(content="<script>alert(1)</script>")
        response = self.client.get(reverse("notes:note_detail", args=[note.pk]))
        self.assertNotContains(response, "<script>alert(1)</script>")
        self.assertContains(response, "&lt;script&gt;alert(1)&lt;/script&gt;")

    def test_note_page_has_back_link_to_its_folder(self):
        note = self.make_note()
        response = self.client.get(reverse("notes:note_detail", args=[note.pk]))
        folder_url = reverse("notes:folder_detail", args=[self.folder.pk])
        self.assertContains(response, f'href="{folder_url}" aria-label="Back to folder"')

    def test_returning_from_note_keeps_history_unchanged(self):
        note = self.make_note()
        folder_url = reverse("notes:folder_detail", args=[self.folder.pk])
        self.client.get(reverse("notes:list"))
        self.client.get(folder_url)
        before = self.client.session["notes_history"]
        self.client.get(reverse("notes:note_detail", args=[note.pk]))
        self.client.get(folder_url)
        self.assertEqual(self.client.session["notes_history"], before)

    def test_folder_with_note_cannot_be_deleted(self):
        self.make_note()
        self.client.post(reverse("notes:folder_delete", args=[self.folder.pk]))
        self.assertTrue(Folder.objects.filter(pk=self.folder.pk).exists())


class NoteEditTests(NoteTestCase):
    def test_anonymous_user_is_redirected(self):
        note = self.make_note()
        self.client.logout()
        response = self.client.get(reverse("notes:note_edit", args=[note.pk]))
        self.assertEqual(response.status_code, 302)

    def test_form_is_filled_with_current_note(self):
        note = self.make_note(content="Existing text")
        response = self.client.get(reverse("notes:note_edit", args=[note.pk]))
        self.assertContains(response, "Subnetting")
        self.assertContains(response, "Existing text")

    def test_edit_saves_changes_and_redirects(self):
        note = self.make_note()
        url = reverse("notes:note_edit", args=[note.pk])
        response = self.client.post(url, {"title": "New title", "content": "New text"})
        self.assertRedirects(response, reverse("notes:note_detail", args=[note.pk]))
        note.refresh_from_db()
        self.assertEqual((note.title, note.content), ("New title", "New text"))

    def test_can_save_with_same_title(self):
        note = self.make_note()
        self.client.post(reverse("notes:note_edit", args=[note.pk]), {"title": "Subnetting", "content": "Changed"})
        note.refresh_from_db()
        self.assertEqual(note.content, "Changed")

    def test_cannot_rename_to_another_notes_title(self):
        self.make_note(title="Taken")
        note = self.make_note(title="Mine")
        response = self.client.post(reverse("notes:note_edit", args=[note.pk]), {"title": "Taken", "content": ""})
        self.assertContains(response, "already exists")
        note.refresh_from_db()
        self.assertEqual(note.title, "Mine")

    def test_cannot_view_or_edit_other_users_note(self):
        note = Note.objects.create(user=self.other_user, folder=self.other_folder, title="Private", content="Secret")
        url = reverse("notes:note_edit", args=[note.pk])
        self.assertEqual(self.client.get(url).status_code, 404)
        self.assertEqual(self.client.post(url, {"title": "Hacked", "content": ""}).status_code, 404)
        note.refresh_from_db()
        self.assertEqual(note.title, "Private")

    def test_browser_cannot_move_note_or_change_owner(self):
        note = self.make_note()
        url = reverse("notes:note_edit", args=[note.pk])
        self.client.post(url, {"title": "Same", "content": "", "user": self.other_user.pk, "folder": self.other_folder.pk})
        note.refresh_from_db()
        self.assertEqual((note.user, note.folder), (self.user, self.folder))


class NoteDeleteTests(NoteTestCase):
    def test_delete_removes_note_and_returns_to_folder(self):
        note = self.make_note()
        response = self.client.post(reverse("notes:note_delete", args=[note.pk]))
        self.assertRedirects(response, reverse("notes:folder_detail", args=[self.folder.pk]))
        self.assertFalse(Note.objects.filter(pk=note.pk).exists())

    def test_delete_leaves_other_notes(self):
        note = self.make_note()
        kept = self.make_note(title="Keep me")
        self.client.post(reverse("notes:note_delete", args=[note.pk]))
        self.assertEqual(list(Note.objects.all()), [kept])

    def test_get_does_not_delete(self):
        note = self.make_note()
        response = self.client.get(reverse("notes:note_delete", args=[note.pk]))
        self.assertEqual(response.status_code, 405)
        self.assertTrue(Note.objects.filter(pk=note.pk).exists())

    def test_anonymous_user_cannot_delete(self):
        note = self.make_note()
        self.client.logout()
        response = self.client.post(reverse("notes:note_delete", args=[note.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Note.objects.filter(pk=note.pk).exists())

    def test_cannot_delete_other_users_note(self):
        note = Note.objects.create(user=self.other_user, folder=self.other_folder, title="Private")
        response = self.client.post(reverse("notes:note_delete", args=[note.pk]))
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Note.objects.filter(pk=note.pk).exists())

    def test_csrf_token_is_required(self):
        note = self.make_note()
        strict_client = Client(enforce_csrf_checks=True)
        strict_client.force_login(self.user)
        response = strict_client.post(reverse("notes:note_delete", args=[note.pk]))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Note.objects.filter(pk=note.pk).exists())

    def test_folder_can_be_deleted_after_its_last_note(self):
        note = self.make_note()
        self.client.post(reverse("notes:note_delete", args=[note.pk]))
        self.client.post(reverse("notes:folder_delete", args=[self.folder.pk]))
        self.assertFalse(Folder.objects.filter(pk=self.folder.pk).exists())


class NotePreviewTests(NoteTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse("notes:note_preview")

    def test_renders_markdown(self):
        response = self.client.post(self.url, {"content": "# Heading"})
        self.assertContains(response, "<h1>Heading</h1>", html=True)

    def test_output_is_sanitized(self):
        response = self.client.post(self.url, {"content": "<script>alert(1)</script>\n\n[x](javascript:alert(2))"})
        self.assertNotContains(response, "<script>")
        self.assertNotContains(response, "href=")

    def test_preview_saves_nothing(self):
        self.client.post(self.url, {"content": "Draft"})
        self.assertFalse(Note.objects.exists())

    def test_get_is_not_allowed(self):
        self.assertEqual(self.client.get(self.url).status_code, 405)

    def test_anonymous_user_is_redirected(self):
        self.client.logout()
        self.assertEqual(self.client.post(self.url, {"content": "x"}).status_code, 302)

    def test_csrf_token_is_required(self):
        strict_client = Client(enforce_csrf_checks=True)
        strict_client.force_login(self.user)
        self.assertEqual(strict_client.post(self.url, {"content": "x"}).status_code, 403)
