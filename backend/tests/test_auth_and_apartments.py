import os
import django
import logging

logger = logging.getLogger(__name__)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")
django.setup()

from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.apartments.models import Apartment


User = get_user_model()


class AuthTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com", password="pass1234"
        )
        self.login_url = reverse("login")
        self.logout_url = reverse("logout")
        self.me_url = reverse("me")
        self.refresh_url = reverse("refresh")

    def test_login_success(self):
        response = self.client.post(
            self.login_url, {"email": "test@example.com", "password": "pass1234"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.cookies)

    def test_me_unauthenticated(self):
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout(self):
        self.client.login(email="test@example.com", password="pass1234")
        self.client.post(
            self.login_url, {"email": "test@example.com", "password": "pass1234"}
        )
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ApartmentTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="owner@example.com", password="ownerpass"
        )
        self.client.login(email="owner@example.com", password="ownerpass")
        self.client.post(
            reverse("login"), {"email": "owner@example.com", "password": "ownerpass"}
        )
        self.apartment_data = {
            "name": "Test Apartment",
            "description": "Cozy place",
            "number_of_rooms": 2,
            "square": 40.5,
            "price": 100000,
        }

    def test_create_apartment(self):
        response = self.client.post("/api/v1/apartments/", self.apartment_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Apartment.objects.count(), 1)

    def test_list_apartments(self):
        Apartment.objects.create(owner=self.user, slug="apt-1", **self.apartment_data)
        response = self.client.get("/api/v1/apartments/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)

    def test_update_apartment_permission(self):
        apt = Apartment.objects.create(
            owner=self.user, slug="apt-1", **self.apartment_data
        )
        response = self.client.put(
            f"/api/v1/apartments/{apt.slug}/", {**self.apartment_data, "price": 99999}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        apt.refresh_from_db()
        self.assertEqual(apt.price, 99999)
