from django.contrib.auth import get_user_model
from django.test import TestCase

from django.urls import reverse

from agency.forms import TopicSearchForm, NewspaperSearchForm
from agency.models import Topic, Redactor, Newspaper

TOPIC_LIST_VIEW_URL = reverse("agency:topic-list")
TOPIC_CREATE_VIEW_URL = reverse("agency:topic-create")

NEWSPAPER_LIST_VIEW_URL = reverse("agency:newspaper-list")
NEWSPAPER_CREATE_VIEW_URL = reverse("agency:newspaper-create")

REDACTOR_LIST_VIEW_URL = reverse("agency:redactor-list")
REDACTOR_CREATE_VIEW_URL = reverse("agency:redactor-create")


class PrivateViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test user",
            password="test12345",
        )
        self.client.force_login(self.user)

    def test_topic_list_view(self):
        Topic.objects.create(name="Sport")
        Topic.objects.create(name="Business")
        response = self.client.get(TOPIC_LIST_VIEW_URL)
        self.assertEqual(response.status_code, 200)
        topic = Topic.objects.all()
        self.assertEqual(
            list(response.context["object_list"]),
            list(topic)
        )
        self.assertTemplateUsed(response, "agency/topic_list.html")

    def test_topic_create_view(self):
        response = self.client.get(TOPIC_CREATE_VIEW_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "agency/topic_form.html")

        form_data = {"name": "Sport"}
        response = self.client.post(TOPIC_CREATE_VIEW_URL, data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Topic.objects.filter(name="Sport").exists()
        )
        self.assertRedirects(response, reverse("agency:topic-list"))

    def test_topic_update_view(self):
        topic = Topic.objects.create(name="Sport")
        topic_update_url = reverse(
            "agency:topic-update",
            kwargs={"pk": topic.id},
        )
        response = self.client.get(topic_update_url)
        self.assertEqual(response.status_code, 200)

        update_data = {"name": "Market"}
        response = self.client.post(
            topic_update_url,
            data=update_data
        )
        self.assertEqual(response.status_code, 302)
        topic.refresh_from_db()
        self.assertEqual(topic.name, "Market")
        response = self.client.get(TOPIC_LIST_VIEW_URL)
        self.assertContains(response, "Market")

    def test_topic_delete_view(self):
        topic = Topic.objects.create(name="Sport")
        topic_delete_url = reverse(
            "agency:topic-delete",
            kwargs={"pk": topic.id},
        )
        response = self.client.get(topic_delete_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "agency/topic_confirm_delete.html")
        response = self.client.post(topic_delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Topic.objects.filter(id=topic.id).exists())
        response = self.client.get(TOPIC_LIST_VIEW_URL)
        self.assertNotContains(response, "Sport")

    def test_retrieve_newspaper_list_view(self):
        topic1 = Topic.objects.create(name="Sport")
        topic2 = Topic.objects.create(name="Business")
        redactor1 = Redactor.objects.create(
            username="markkoop",
            password="test12345"
        )
        redactor2 = Redactor.objects.create(
            username="johnny",
            password="test12345"
        )
        newspaper = Newspaper.objects.create(
            title="bitcoin",
            content="test content",
            published_date="2025-01-01",
        )
        newspaper.topics.add(topic1, topic2)
        newspaper.publishers.add(redactor1, redactor2)

        response = self.client.get(NEWSPAPER_LIST_VIEW_URL)
        self.assertEqual(response.status_code, 200)
        newspaper_list = Newspaper.objects.all()
        self.assertEqual(
            list(response.context["object_list"]),
            list(newspaper_list)
        )
        self.assertTemplateUsed(response, "agency/newspaper_list.html")

    def test_newspaper_create_view(self):
        topic = Topic.objects.create(name="politics")
        redactor = Redactor.objects.create(
            username="albertis",
            password="test12345"
        )
        response = self.client.get(NEWSPAPER_CREATE_VIEW_URL)
        self.assertTemplateUsed(response, "agency/newspaper_form.html")

        form_data = {
            "title": "presidents",
            "content": "test content",
            "topics": [topic.id],
            "publishers": [redactor.id]
        }
        response = self.client.post(NEWSPAPER_CREATE_VIEW_URL, data=form_data)
        self.assertEqual(response.status_code, 302)
        newspaper = Newspaper.objects.get(title="presidents")
        self.assertEqual(newspaper.content, "test content")
        self.assertIn(topic, newspaper.topics.all())
        self.assertIn(redactor, newspaper.publishers.all())

    def test_newspaper_update_view(self):
        topic = Topic.objects.create(name="politics")
        redactor = Redactor.objects.create(
            username="albertis",
            password="test12345"
        )
        newspaper = Newspaper.objects.create(
            title="presidents",
            content="test content",
        )
        newspaper.topics.set([topic])
        newspaper.publishers.set([redactor])
        newspaper_update_url = reverse(
            "agency:newspaper-update",
            kwargs={"pk": newspaper.id},
        )
        response = self.client.get(newspaper_update_url)
        self.assertEqual(response.status_code, 200)

        update_data = {
            "title": "space ships",
            "content": "test content1",
            "topics": [topic.id],
            "publishers": [redactor.id],
        }
        response = self.client.post(newspaper_update_url, data=update_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, NEWSPAPER_LIST_VIEW_URL)
        newspaper.refresh_from_db()
        self.assertEqual(newspaper.title, "space ships")
        self.assertEqual(newspaper.content, "test content1")
        self.assertIn(topic, newspaper.topics.all())
        self.assertIn(redactor, newspaper.publishers.all())

        response = self.client.get(NEWSPAPER_LIST_VIEW_URL)
        self.assertContains(response, "space ships")
        self.assertNotContains(response, "presidents")

    def test_newspaper_delete_view(self):
        topic = Topic.objects.create(name="race")
        redactor = Redactor.objects.create(
            username="misha",
            password="test12345"
        )
        newspaper = Newspaper.objects.create(
            title="racers",
            content="test content",
        )
        newspaper.topics.set([topic])
        newspaper.publishers.set([redactor])
        newspaper_delete_url = reverse(
            "agency:newspaper-delete",
            kwargs={"pk": newspaper.id},
        )
        response = self.client.get(newspaper_delete_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "agency/newspaper_confirm_delete.html")
        response = self.client.post(newspaper_delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Newspaper.objects.filter(id=newspaper.id).exists())
        response = self.client.get(NEWSPAPER_LIST_VIEW_URL)
        self.assertNotContains(response, "racers")
        self.assertEqual(Newspaper.objects.count(), 0)

    def test_newspaper_detail_view(self):
        topic1 = Topic.objects.create(name="Politics")
        topic2 = Topic.objects.create(name="Race")
        redactor1 = get_user_model().objects.create_user(
            username="mark",
            password="test12345",
            first_name="Mark",
            last_name="Smith"
        )
        redactor2 = get_user_model().objects.create_user(
            username="john",
            password="test12345",
            first_name="John",
            last_name="Doe"
        )
        newspaper = Newspaper.objects.create(
            title="World news",
            content="test content for the newspaper.",
        )
        newspaper.topics.add(topic1, topic2)
        newspaper.publishers.set([redactor1, redactor2])
        newspaper_detail_url = reverse(
            "agency:newspaper-detail",
            kwargs={"pk": newspaper.id},
        )
        response = self.client.get(newspaper_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "agency/newspaper_detail.html")

        self.assertContains(response, "World news")
        self.assertContains(response, "test content for the newspaper.")
        self.assertContains(response, "Politics")
        self.assertContains(response, "Race")
        self.assertContains(response, "mark")
        self.assertContains(response, "john")

    def test_retrieve_redactor_list_view(self):
        Redactor.objects.create(
            username="markkoop",
            first_name="Mark",
            last_name="Koop",
            years_of_experience=5
        )
        Redactor.objects.create(
            username="johnny",
            first_name="John",
            last_name="Doe",
            years_of_experience=2
        )
        response = self.client.get(REDACTOR_LIST_VIEW_URL)
        self.assertEqual(response.status_code, 200)
        list_redactor = Redactor.objects.all()
        self.assertEqual(
            list(response.context["object_list"]),
            list(list_redactor)
        )
        self.assertTemplateUsed(response, "agency/redactor_list.html")

    def test_redactor_create_view(self):
        format_data = {
            "username": "tonyst",
            "password1": "test12345",
            "password2": "test12345",
            "first_name": "Tony",
            "last_name": "Stone",
            "years_of_experience": 2
        }
        response = self.client.get(REDACTOR_CREATE_VIEW_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "agency/redactor_form.html")

        response = self.client.post(REDACTOR_CREATE_VIEW_URL, format_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("agency:redactor-list"))

        new_user = get_user_model().objects.get(
            username=format_data["username"]
        )
        self.assertEqual(new_user.first_name, format_data["first_name"])
        self.assertEqual(new_user.last_name, format_data["last_name"])
        self.assertEqual(
            new_user.years_of_experience,
            format_data["years_of_experience"],
        )

    def test_redactor_delete_view(self):
        redactor = Redactor.objects.create(
            username="Tims",
            first_name="Tims",
            last_name="Cooper",
            years_of_experience=4
        )
        redactor_delete_url = reverse(
            "agency:redactor-delete",
            kwargs={"pk": redactor.id},
        )
        response = self.client.get(redactor_delete_url)
        self.assertEqual(response.status_code, 200)
        Redactor.objects.filter(pk=redactor.id).delete()
        res = self.client.get(REDACTOR_LIST_VIEW_URL)
        self.assertNotContains(res, redactor)
        self.assertTemplateUsed(response, "agency/redactor_confirm_delete.html")

    def test_redactor_detail_view(self):
        redactor = Redactor.objects.create(
            username="Martin",
            first_name="Martin",
            last_name="Newman",
            years_of_experience=7,
            is_staff=True,
        )
        topic = Topic.objects.create(
            name="testname"
        )
        newspaper = Newspaper.objects.create(
            title="testtitle",
            content="testcontent"
        )
        newspaper.topics.add(topic)
        newspaper.publishers.set([redactor])
        redactor_detail_url = reverse(
            "agency:redactor-detail",
            kwargs={"pk": redactor.id},
        )
        response = self.client.get(redactor_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, redactor.username)
        self.assertContains(response, newspaper.title)
        self.assertTemplateUsed(response, "agency/redactor_detail.html")

    def test_redactor_years_of_experience_update_view(self):
        redactor = Redactor.objects.create(
            username="markkoop",
            years_of_experience=5,
        )
        redactor.years_of_experience = 2
        redactor.save()
        self.assertTrue(redactor.years_of_experience, 10)