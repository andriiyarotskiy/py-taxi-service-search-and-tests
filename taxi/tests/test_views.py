from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class PublicDriverDeleteFormTest(TestCase):
    def setUp(self):
        self.test_user = get_user_model().objects.create_user(
            username="test_user",
            password="password123"
        )

    def test_driver_delete_login_required(self):
        url = reverse("taxi:driver-delete", args=[str(self.test_user.id)])
        res = self.client.get(url)
        self.assertNotEqual(res.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create(
            username="driver_1",
            password="best_driver_123",
            license_number="JAM12345",
        )
        self.client.force_login(self.driver)

    def test_retrieve_drivers_list(self):
        url = reverse("taxi:driver-list")
        get_user_model().objects.create(
            username="driver_2",
            password="best_driver_also",
            license_number="ABC32145",
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        drivers = get_user_model().objects.all()
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )

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
