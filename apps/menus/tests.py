from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from datetime import date, timedelta
from apps.restaurants.models import Restaurant
from .models import Menu, MenuItem

User = get_user_model()


class MenusTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.owner = User.objects.create_user(
            username="owner",
            password="pass123",
            role="restaurant_owner"
        )
        self.restaurant = Restaurant.objects.create(
            name="Test Restaurant",
            owner=self.owner
        )
        self.client.force_authenticate(user=self.owner)

    def test_create_menu(self):
        data = {
            "restaurant": self.restaurant.id,
            "date": str(date.today()),
            "items": [
                {
                    "name": "Pizza",
                    "description": "Delicious pizza",
                    "price": "12.50",
                    "category": "main"
                }
            ]
        }
        response = self.client.post("/api/v1/menus/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data["items"]), 1)

    def test_get_today_menu(self):
        menu = Menu.objects.create(
            restaurant=self.restaurant,
            date=date.today()
        )
        MenuItem.objects.create(
            menu=menu,
            name="Pizza",
            description="Test",
            price="12.50"
        )
        response = self.client.get("/api/v1/menus/today/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_today_menu_empty(self):
        menu = Menu.objects.create(
            restaurant=self.restaurant,
            date=date.today() - timedelta(days=1)
        )
        response = self.client.get("/api/v1/menus/today/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_update_menu(self):
        menu = Menu.objects.create(
            restaurant=self.restaurant,
            date=date.today()
        )
        MenuItem.objects.create(
            menu=menu,
            name="Old Item",
            description="Old",
            price="10.00"
        )
        data = {
            "restaurant": self.restaurant.id,
            "date": str(date.today()),
            "items": [
                {
                    "name": "New Item",
                    "description": "New",
                    "price": "15.00",
                    "category": "main"
                }
            ]
        }
        response = self.client.put(f"/api/v1/menus/{menu.id}/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["items"]), 1)
        self.assertEqual(response.data["items"][0]["name"], "New Item")
