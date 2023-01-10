# pages/tests.py
from django.test import SimpleTestCase
from django.urls import reverse


class HomepageTests(SimpleTestCase):
    def setUp(self) -> None:
        url = reverse("home")
        self.response = self.client.get(url)

    def test_url_exists_at_correct_location(self) -> None:
        self.assertEqual(self.response.status_code, 200)

    def test_homepage_template(self) -> None:
        self.assertTemplateUsed(self.response, "home.html")

    def test_homepage_contains_correct_html(self) -> None:
        self.assertContains(self.response, "Tasks app")

    def test_homepage_does_not_contain_incorrect_html(self) -> None:
        self.assertNotContains(self.response, "Hi there! I should not be on the page.")
