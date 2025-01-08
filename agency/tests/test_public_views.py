from django.test import TestCase
from django.urls import reverse

TOPIC_LIST_VIEW_URL = reverse("agency:topic-list")
TOPIC_CREATE_VIEW_URL = reverse("agency:topic-create")

NEWSPAPER_LIST_VIEW_URL = reverse("agency:newspaper-list")
NEWSPAPER_CREATE_VIEW_URL = reverse("agency:newspaper-create")

REDACTOR_LIST_VIEW_URL = reverse("agency:redactor-list")
REDACTOR_CREATE_VIEW_URL = reverse("agency:redactor-create")


class PublicViewTest(TestCase):
    def test_topic_list_view(self):
        response = self.client.get(TOPIC_LIST_VIEW_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_topic_create_view(self):
        response = self.client.get(TOPIC_CREATE_VIEW_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_topic_update_view(self):
        topic_update_view_url = reverse(
            "agency:topic-update",
            args=[1]
        )
        response = self.client.get(topic_update_view_url)
        self.assertNotEqual(response.status_code, 200)

    def test_topic_delete_view(self):
        topic_delete_view_url = reverse(
            "agency:topic-delete",
            args=[1]
        )
        response = self.client.get(topic_delete_view_url)
        self.assertNotEqual(response.status_code, 200)

    def test_newspaper_list_view(self):
        response = self.client.get(NEWSPAPER_LIST_VIEW_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_newspaper_create_view(self):
        response = self.client.get(NEWSPAPER_CREATE_VIEW_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_newspaper_update_view(self):
        newspaper_update_view_url = reverse(
            "agency:newspaper-update",
            args=[1]
        )
        response = self.client.get(newspaper_update_view_url)
        self.assertNotEqual(response.status_code, 200)

    def test_newspaper_delete_view(self):
        newspaper_delete_view_url = reverse(
            "agency:newspaper-delete",
            args=[1]
        )
        response = self.client.get(newspaper_delete_view_url)
        self.assertNotEqual(response.status_code, 200)

    def test_newspaper_detail_view(self):
        newspaper_detail_view_url = reverse(
            "agency:newspaper-detail",
            args=[1]
        )
        response = self.client.get(newspaper_detail_view_url)
        self.assertNotEqual(response.status_code, 200)

    def test_redactor_list_view(self):
        response = self.client.get(REDACTOR_LIST_VIEW_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_redactor_create_view(self):
        response = self.client.get(REDACTOR_CREATE_VIEW_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_redactor_update_view(self):
        redactor_update_view_url = reverse(
            "agency:redactor-update",
            args=[1]
        )
        response = self.client.get(redactor_update_view_url)
        self.assertNotEqual(response.status_code, 200)

    def test_redactor_delete_view(self):
        redactor_delete_view_url = reverse(
            "agency:redactor-delete",
            args=[1]
        )
        response = self.client.get(redactor_delete_view_url)
        self.assertNotEqual(response.status_code, 200)

    def test_redactor_detail_view(self):
        redactor_detail_view_url = reverse(
            "agency:redactor-detail",
            args=[1]
        )
        response = self.client.get(redactor_detail_view_url)
        self.assertNotEqual(response.status_code, 200)
