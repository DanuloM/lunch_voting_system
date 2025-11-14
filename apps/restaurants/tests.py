from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Restaurant

User = get_user_model()


class RestaurantsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="owner",
            password="pass123",
            role="restaurant_owner"
        )
        self.client.force_authenticate(user=self.user)

    def test_create_restaurant(self):
        data = {
            "name": "Pizza Place",
            "address": "123 Main St"
        }
        response = self.client.post("/api/v1/restaurants/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Pizza Place")
        self.assertEqual(response.data["owner"], "owner")

    def test_list_restaurants(self):
        Restaurant.objects.create(name="Restaurant 1", owner=self.user)
        Restaurant.objects.create(name="Restaurant 2", owner=self.user)
        response = self.client.get("/api/v1/restaurants/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_restaurant(self):
        restaurant = Restaurant.objects.create(name="Test Restaurant", owner=self.user)
        response = self.client.get(f"/api/v1/restaurants/{restaurant.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Test Restaurant")

    def test_create_restaurant_requires_auth(self):
        self.client.force_authenticate(user=None)
        data = {
            "name": "Pizza Place",
            "address": "123 Main St"
        }
        response = self.client.post("/api/v1/restaurants/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
