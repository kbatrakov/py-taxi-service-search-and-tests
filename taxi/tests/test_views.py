from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from taxi.models import Manufacturer, Driver

MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTest(TestCase):

    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturingTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="Test_user123"
        )

        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(
            name="BYD",
            country="China"
        )

        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)

        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturers_list"]),
            list(manufacturers))
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class PrivateDriverTests(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="Eduardo",
            password="Ed123456")
        self.client.force_login(self.driver)

    def test_create_driver(self):
        form_data = {
            "username": "LeBronnnieJames",
            "password1": "Lbj12345_king",
            "password2": "Lbj12345_king",
            "first_name": "Lebron",
            "last_name": "James",
            "license_number": "LBJ12345"
        }

        self.client.post(reverse("taxi:driver-create"), data=form_data)

        new_driver = get_user_model().objects.get(
            username=form_data["username"])
        self.assertEqual(new_driver.first_name,
                         form_data["first_name"])
        self.assertEqual(new_driver.last_name,
                         form_data["last_name"])
        self.assertEqual(new_driver.license_number,
                         form_data["license_number"])
