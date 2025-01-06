from django.contrib.auth import get_user_model
from django.test import TestCase

from agency.models import Newspaper, Topic


class TestModels(TestCase):
    def test_topic_str(self):
        topic = Topic.objects.create(name="test")
        self.assertEqual(
            str(topic),
            f"{topic.name}"
        )

    def test_redactor_str(self):
        redactor = get_user_model().objects.create(
            id="1",
            password="test12345",
            username="testname",
            first_name="first_test",
            last_name="last_test",
        )
        self.assertEqual(
            str(redactor),
            f"{redactor.username}: ({redactor.first_name} {redactor.last_name})"
        )

    def test_newspaper_str(self):
        newspaper = Newspaper.objects.create(
            title="test",
            content="test",
            published_date="2025-01-01",
        )

        self.assertEqual(
            str(newspaper), newspaper.title
        )

    def test_redactor_years_of_experience(self):
        username = "test"
        password = "test12345"
        years_of_experience = 1
        redactor = get_user_model().objects.create_user(
            username=username,
            password=password,
            years_of_experience=years_of_experience,
        )
        self.assertEqual(redactor.username, username)
        self.assertTrue(redactor.check_password(password))
        self.assertEqual(redactor.years_of_experience, years_of_experience)

