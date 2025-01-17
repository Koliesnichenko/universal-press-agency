from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="testadmin",
        )
        self.client.force_login(self.admin_user)
        self.redactor = get_user_model().objects.create_user(
            username="redactor",
            password="testredactor",
            years_of_experience=1,
        )

    def test_redactor_years_of_experience_listed(self):
        """
        Test that redactor's years of experience is in list_display on admin page
        :return:
        """

        url = reverse("admin:agency_redactor_changelist")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.redactor.years_of_experience)

    def test_redactor_detail_years_of_experience_listed(self):
        """
        Test that redactor's years of experience is on redactor detail admin page
        :return:
        """
        url = reverse("admin:agency_redactor_change", args=[self.redactor.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.redactor.years_of_experience)

    def test_redactor_detail_first_last_name_listed(self):
        """
        Test that first, last name and years of experience is on redactor detail admin page
        :return:
        """
        url = reverse("admin:agency_redactor_change", args=[self.redactor.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.redactor.first_name)
        self.assertContains(res, self.redactor.last_name)
        self.assertContains(res, self.redactor.years_of_experience)


