from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from datetime import date
from apps.restaurants.models import Restaurant
from apps.menus.models import Menu, MenuItem
from .models import Vote

User = get_user_model()


class VotingTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.employee = User.objects.create_user(
            username="employee",
            password="pass123",
            role="employee"
        )
        self.owner = User.objects.create_user(
            username="owner",
            password="pass123",
            role="restaurant_owner"
        )
        self.restaurant = Restaurant.objects.create(
            name="Test Restaurant",
            owner=self.owner
        )
        self.menu = Menu.objects.create(
            restaurant=self.restaurant,
            date=date.today()
        )
        MenuItem.objects.create(
            menu=self.menu,
            name="Pizza",
            description="Test",
            price="12.50"
        )
        self.client.force_authenticate(user=self.employee)

    def test_create_vote(self):
        data = {
            "menu": self.menu.id
        }
        response = self.client.post("/api/v1/votes/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Vote.objects.filter(employee=self.employee, date=date.today()).exists())

    def test_cannot_vote_twice(self):
        Vote.objects.create(
            employee=self.employee,
            menu=self.menu,
            date=date.today()
        )
        data = {
            "menu": self.menu.id
        }
        response = self.client.post("/api/v1/votes/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_vote_results(self):
        restaurant2 = Restaurant.objects.create(
            name="Restaurant 2",
            owner=self.owner
        )
        menu2 = Menu.objects.create(
            restaurant=restaurant2,
            date=date.today()
        )
        Vote.objects.create(
            employee=self.employee,
            menu=self.menu,
            date=date.today()
        )
        employee2 = User.objects.create_user(
            username="employee2",
            password="pass123",
            role="employee"
        )
        Vote.objects.create(
            employee=employee2,
            menu=self.menu,
            date=date.today()
        )
        response = self.client.get("/api/v1/votes/results/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["vote_count"], 2)

    def test_get_my_vote(self):
        Vote.objects.create(
            employee=self.employee,
            menu=self.menu,
            date=date.today()
        )
        response = self.client.get("/api/v1/votes/my-vote/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["menu"], self.menu.id)

    def test_get_my_vote_not_exists(self):
        response = self.client.get("/api/v1/votes/my-vote/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
