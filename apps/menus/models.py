from django.db import models
from apps.restaurants.models import Restaurant


class Menu(models.Model):
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="menus"
    )
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["restaurant", "date"]
        ordering = ["-date"]

    def __str__(self):
        return f"{self.restaurant.name} - {self.date}"


class MenuItem(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="items")
    CATEGORY_CHOICES = (
        ("main", "MAIN"),
        ("side", "SIDE"),
        ("dessert", "DESSERT"),
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=10, default="main")

    def __str__(self):
        return f"{self.name} ({self.category}) - {self.price}"
