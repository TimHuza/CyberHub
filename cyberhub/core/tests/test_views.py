from django.test import TestCase
from django.urls import reverse


class HomeViewTests(TestCase):
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