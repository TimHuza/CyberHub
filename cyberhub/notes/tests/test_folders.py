from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Folder, Note

User = get_user_model()


class FolderTestCase(TestCase):
    """Two users, so every test can check that one can't touch the other's data."""

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="owner", password="test-pass-123")
        cls.other_user = User.objects.create_user(username="other", password="test-pass-123")

    def setUp(self):
        self.client.force_login(self.user)


class FolderPageTests(FolderTestCase):
    def test_anonymous_user_is_redirected(self):
        self.client.logout()
        response = self.client.get(reverse("notes:list"))
        self.assertEqual(response.status_code, 302)

    def test_list_shows_only_own_top_level_folders(self):
        mine = Folder.objects.create(user=self.user, name="Networking")
        Folder.objects.create(user=self.user, parent=mine, name="Subnetting")
        Folder.objects.create(user=self.other_user, name="Secret")
        response = self.client.get(reverse("notes:list"))
        self.assertEqual(list(response.context["folders"]), [mine])

    def test_detail_shows_subfolders_and_breadcrumbs(self):
        top = Folder.objects.create(user=self.user, name="Networking")
        child = Folder.objects.create(user=self.user, parent=top, name="Subnetting")
        grandchild = Folder.objects.create(user=self.user, parent=child, name="Lesson 1")
        response = self.client.get(reverse("notes:folder_detail", args=[child.pk]))
        self.assertEqual(list(response.context["folders"]), [grandchild])
        self.assertEqual(response.context["breadcrumbs"], [top, child])

    def test_folder_name_is_escaped(self):
        folder = Folder.objects.create(user=self.user, name="<script>alert(1)</script>")
        response = self.client.get(reverse("notes:folder_detail", args=[folder.pk]))
        self.assertNotContains(response, "<script>alert(1)</script>")


class FolderCreateTests(FolderTestCase):
    def test_create_top_level_folder(self):
        response = self.client.post(reverse("notes:folder_create"), {"name": "Networking"})
        self.assertRedirects(response, reverse("notes:list"))
        folder = Folder.objects.get(name="Networking")
        self.assertEqual(folder.user, self.user)
        self.assertIsNone(folder.parent)

    def test_create_subfolder(self):
        parent = Folder.objects.create(user=self.user, name="Networking")
        self.client.post(reverse("notes:subfolder_create", args=[parent.pk]), {"name": "Subnetting"})
        self.assertEqual(Folder.objects.get(name="Subnetting").parent, parent)

    def test_browser_cannot_choose_owner_or_parent(self):
        other_folder = Folder.objects.create(user=self.other_user, name="Secret")
        self.client.post(reverse("notes:folder_create"), {"name": "Mine", "user": self.other_user.pk, "parent": other_folder.pk})
        folder = Folder.objects.get(name="Mine")
        self.assertEqual(folder.user, self.user)
        self.assertIsNone(folder.parent)

    def test_duplicate_top_level_name_shows_error(self):
        Folder.objects.create(user=self.user, name="Networking")
        response = self.client.post(reverse("notes:folder_create"), {"name": "Networking"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "already exists here")
        self.assertEqual(Folder.objects.filter(user=self.user).count(), 1)

    def test_different_capitalization_is_allowed(self):
        Folder.objects.create(user=self.user, name="test")
        response = self.client.post(reverse("notes:folder_create"), {"name": "TeSt"})
        self.assertRedirects(response, reverse("notes:list"))
        self.assertEqual(Folder.objects.filter(user=self.user, name__iexact="test").count(), 2)

    def test_same_name_allowed_in_different_parents(self):
        first = Folder.objects.create(user=self.user, name="Networking")
        second = Folder.objects.create(user=self.user, name="Linux")
        Folder.objects.create(user=self.user, parent=first, name="Basics")
        self.client.post(reverse("notes:subfolder_create", args=[second.pk]), {"name": "Basics"})
        self.assertEqual(Folder.objects.filter(name="Basics").count(), 2)

    def test_two_users_can_use_the_same_name(self):
        Folder.objects.create(user=self.other_user, name="Networking")
        self.client.post(reverse("notes:folder_create"), {"name": "Networking"})
        self.assertTrue(Folder.objects.filter(user=self.user, name="Networking").exists())

    def test_blank_name_is_rejected(self):
        response = self.client.post(reverse("notes:folder_create"), {"name": "   "})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Folder.objects.exists())


class FolderRenameTests(FolderTestCase):
    def test_rename(self):
        folder = Folder.objects.create(user=self.user, name="Old")
        self.client.post(reverse("notes:folder_rename", args=[folder.pk]), {"name": "New"})
        folder.refresh_from_db()
        self.assertEqual(folder.name, "New")

    def test_can_change_only_capitalization(self):
        folder = Folder.objects.create(user=self.user, name="networking")
        self.client.post(reverse("notes:folder_rename", args=[folder.pk]), {"name": "Networking"})
        folder.refresh_from_db()
        self.assertEqual(folder.name, "Networking")

    def test_rename_to_sibling_name_is_rejected(self):
        Folder.objects.create(user=self.user, name="Linux")
        folder = Folder.objects.create(user=self.user, name="Networking")
        response = self.client.post(reverse("notes:folder_rename", args=[folder.pk]), {"name": "Linux"})
        self.assertContains(response, "already exists here")
        folder.refresh_from_db()
        self.assertEqual(folder.name, "Networking")


class FolderDeleteTests(FolderTestCase):
    def test_delete_empty_folder(self):
        parent = Folder.objects.create(user=self.user, name="Networking")
        child = Folder.objects.create(user=self.user, parent=parent, name="Empty")
        response = self.client.post(reverse("notes:folder_delete", args=[child.pk]))
        self.assertRedirects(response, reverse("notes:folder_detail", args=[parent.pk]))
        self.assertFalse(Folder.objects.filter(pk=child.pk).exists())

    def test_delete_requires_post(self):
        folder = Folder.objects.create(user=self.user, name="Networking")
        response = self.client.get(reverse("notes:folder_delete", args=[folder.pk]))
        self.assertEqual(response.status_code, 405)
        self.assertTrue(Folder.objects.filter(pk=folder.pk).exists())

    def test_folder_with_subfolder_is_kept(self):
        parent = Folder.objects.create(user=self.user, name="Networking")
        Folder.objects.create(user=self.user, parent=parent, name="Subnetting")
        response = self.client.post(reverse("notes:folder_delete", args=[parent.pk]), follow=True)
        self.assertContains(response, "isn&#x27;t empty")
        self.assertTrue(Folder.objects.filter(pk=parent.pk).exists())

    def test_folder_with_note_is_kept(self):
        folder = Folder.objects.create(user=self.user, name="Networking")
        Note.objects.create(user=self.user, folder=folder, title="Lesson 1")
        self.client.post(reverse("notes:folder_delete", args=[folder.pk]))
        self.assertTrue(Folder.objects.filter(pk=folder.pk).exists())

    def test_deleting_user_removes_their_folders_and_notes(self):
        parent = Folder.objects.create(user=self.user, name="Networking")
        child = Folder.objects.create(user=self.user, parent=parent, name="Subnetting")
        Note.objects.create(user=self.user, folder=child, title="Lesson 1")
        self.user.delete()
        self.assertFalse(Folder.objects.exists())
        self.assertFalse(Note.objects.exists())


class FolderOwnershipTests(FolderTestCase):
    """Changing the ID in the URL must never reach another user's folder."""

    def setUp(self):
        super().setUp()
        self.other_folder = Folder.objects.create(user=self.other_user, name="Secret")

    def test_cannot_view(self):
        response = self.client.get(reverse("notes:folder_detail", args=[self.other_folder.pk]))
        self.assertEqual(response.status_code, 404)

    def test_cannot_create_subfolder(self):
        response = self.client.post(reverse("notes:subfolder_create", args=[self.other_folder.pk]), {"name": "Hack"})
        self.assertEqual(response.status_code, 404)
        self.assertFalse(Folder.objects.filter(name="Hack").exists())

    def test_cannot_rename(self):
        response = self.client.post(reverse("notes:folder_rename", args=[self.other_folder.pk]), {"name": "Hack"})
        self.assertEqual(response.status_code, 404)
        self.other_folder.refresh_from_db()
        self.assertEqual(self.other_folder.name, "Secret")

    def test_cannot_delete(self):
        response = self.client.post(reverse("notes:folder_delete", args=[self.other_folder.pk]))
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Folder.objects.filter(pk=self.other_folder.pk).exists())
