from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class PrivateDriverTest(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create(
            username="driver_1",
            password="best_driver_123",
            license_number="JAM12345",
        )
        self.client.force_login(self.driver)

    def test_create_driver(self):
        form_data = {
            "username": "driver_2",
            "license_number": "ABC12345",
            "first_name": "Andrii",
            "last_name": "Yarotskiy",
            "password1": "django1234",
            "password2": "django1234",
        }

        res = self.client.post(reverse("taxi:driver-create"), data=form_data)
        self.assertEqual(res.status_code, 302)
        new_driver = get_user_model().objects.get(
            license_number=form_data["license_number"]
        )
        self.assertEqual(
            new_driver.license_number, form_data["license_number"]
        )
        self.assertEqual(new_driver.username, form_data["username"])
        self.assertTrue(new_driver.check_password(form_data["password1"]))
