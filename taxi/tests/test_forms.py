from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils.http import urlencode

from taxi.forms import ManufacturerSearchForm


class ManufacturerSearchFormTest(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create(
            username="driver-1",
            password="django1234",
        )
        self.client.force_login(self.driver)

    def test_search_drivers_by_username(self):
        get_user_model().objects.create_user(
            username="driver-2",
            password="django4321",
            license_number="ABC12345",
        )

        base_url = reverse("taxi:driver-list")
        query_string = urlencode({"username": "driver-2"})
        url = f"{base_url}?{query_string}"

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "driver-2")

        driver_list = response.context["driver_list"]
        self.assertTrue(any(d.username == "driver-2" for d in driver_list))
        self.assertFalse(any(d.username == "driver-1" for d in driver_list))

    def test_manufacturer_form_label(self):
        form = ManufacturerSearchForm()
        self.assertTrue(
            form.fields["name"].label is None
            or form.fields["name"].label == ""
        )

    def test_manufacturer_form_placeholder(self):
        form = ManufacturerSearchForm()
        placeholder = "Search Manufacturer by Name"
        self.assertEqual(
            form.fields["name"].widget.attrs["placeholder"], placeholder
        )
