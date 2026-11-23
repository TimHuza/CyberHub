from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.test import TestCase
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

    def test_folder_with_note_cannot_be_deleted(self):
        self.make_note()
        self.client.post(reverse("notes:folder_delete", args=[self.folder.pk]))
        self.assertTrue(Folder.objects.filter(pk=self.folder.pk).exists())
