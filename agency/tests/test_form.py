from django.test import TestCase

from agency.forms import (
    TopicSearchForm,
    NewspaperSearchForm,
    RedactorSearchForm,
    RedactorCreationForm
)


class TestForm(TestCase):
    def test_redactor_creation_form_with_years_of_experience_is_valid(self):
        form_data = {
            "username": "johnytest",
            "password1": "test12345",
            "password2": "test12345",
            "email": "email@mail.com",
            "first_name": "John",
            "last_name": "Doe",
            "years_of_experience": 10
        }
        form = RedactorCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_topic_search_form(self):
        form_data = {
            "name": "test"
        }
        form = TopicSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_newspaper_search_form(self):
        form_data = {
            "title": "test"
        }
        form = NewspaperSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_redactor_search_form(self):
        form_data = {
            "username": "testname"
        }
        form = RedactorSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
