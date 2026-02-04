from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import ManufacturerSearchForm


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


class ManufacturerSearchFormTest(TestCase):
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
