from decimal import Decimal
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from apps.apartments.models import Apartment

User = get_user_model()


class AuthTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.test_user_email = "test@example.com"
        cls.test_user_password = "pass1234"
        cls.user = User.objects.create_user(
            email=cls.test_user_email, password=cls.test_user_password
        )
        cls.login_url = reverse("login")
        cls.logout_url = reverse("logout")
        cls.me_url = reverse("me")
        cls.refresh_url = reverse("refresh")

        cls.login_credentials = {
            "email": cls.test_user_email,
            "password": cls.test_user_password,
        }

    def test_login_success(self):
        """Test successful user login."""
        response = self.client.post(self.login_url, self.login_credentials)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn("access_token", response.cookies)

    def test_me_unauthenticated(self):
        """Test accessing the 'me' endpoint without authentication."""
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_me_authenticated(self):
        """Test accessing the 'me' endpoint with authentication."""
        login_response = self.client.post(self.login_url, self.login_credentials)
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("email"), self.test_user_email)

    def test_logout_success(self):
        """Test successful user logout."""
        login_response = self.client.post(self.login_url, self.login_credentials)
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ApartmentTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.owner_email = "owner@example.com"
        cls.owner_password = "ownerpass"
        cls.owner = User.objects.create_user(
            email=cls.owner_email, password=cls.owner_password
        )
        cls.apartment_list_url = reverse("apartments-list")

        cls.apartment_data = {
            "name": "Test Apartment",
            "description": "Cozy place",
            "number_of_rooms": 2,
            "square": Decimal(40.5),
            "price": Decimal(100000),
        }

        cls.owner_credentials = {
            "email": cls.owner_email,
            "password": cls.owner_password,
        }

    def setUp(self):

        super().setUp()

        login_response = self.client.post(reverse("login"), self.owner_credentials)
        self.assertEqual(
            login_response.status_code, status.HTTP_200_OK, "Login failed in setUp"
        )

    def test_create_apartment_success(self):
        """Test successful apartment creation."""
        response = self.client.post(
            self.apartment_list_url, self.apartment_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Apartment.objects.count(), 1)
        created_apartment = Apartment.objects.first()
        self.assertEqual(created_apartment.name, self.apartment_data["name"])
        self.assertEqual(created_apartment.owner, self.owner)

    def test_list_apartments_success(self):
        """Test successful apartment listing."""
        Apartment.objects.create(owner=self.owner, slug="apt-1", **self.apartment_data)
        response = self.client.get(self.apartment_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["results"][0]["name"], self.apartment_data["name"]
        )
        self.assertEqual(
            response.data["results"][0]["description"],
            self.apartment_data["description"],
        )
        self.assertEqual(
            response.data["results"][0]["number_of_rooms"],
            self.apartment_data["number_of_rooms"],
        )
        self.assertEqual(
            Decimal(response.data["results"][0]["square"]),
            Decimal(self.apartment_data["square"]),
        )
        self.assertEqual(
            Decimal(response.data["results"][0]["price"]),
            Decimal(self.apartment_data["price"]),
        ),
        self.assertEqual(response.data["results"][0]["owner_email"], self.owner.email)

    def test_update_apartment_by_owner_success(self):
        """Test successful apartment update by its owner."""
        apt = Apartment.objects.create(
            owner=self.owner, slug="apt-to-update", **self.apartment_data
        )
        detail_url = reverse("apartments-detail", kwargs={"slug": apt.slug})
        updated_data = {**self.apartment_data, "price": 99999, "name": "Updated Name"}

        response = self.client.put(detail_url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        apt.refresh_from_db()
        self.assertEqual(apt.price, 99999)
        self.assertEqual(apt.name, "Updated Name")

    def test_update_apartment_by_another_user_forbidden(self):
        """Test forbidden apartment update by another user."""
        apt = Apartment.objects.create(
            owner=self.owner, slug="apt-permission", **self.apartment_data
        )
        detail_url = reverse("apartments-detail", kwargs={"slug": apt.slug})

        other_user_email = "other@example.com"
        other_user_password = "otherpass"
        User.objects.create_user(email=other_user_email, password=other_user_password)

        self.client.logout()

        other_login_response = self.client.post(
            reverse("login"),
            {"email": other_user_email, "password": other_user_password},
        )
        self.assertEqual(other_login_response.status_code, status.HTTP_200_OK)
        updated_data = {**self.apartment_data, "price": 12345}
        response = self.client.put(detail_url, updated_data, format="json")
        self.assertIn(
            response.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND]
        )

    def test_delete_apartment_by_owner_success(self):
        """Test successful apartment deletion by its owner."""
        apt = Apartment.objects.create(
            owner=self.owner, slug="apt-to-delete", **self.apartment_data
        )
        detail_url = reverse("apartments-detail", kwargs={"slug": apt.slug})

        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Apartment.objects.count(), 0)
