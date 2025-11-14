from django.db import models
from apps.menus.models import Menu
from django.contrib.auth import get_user_model

User = get_user_model()


class Vote(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="votes")
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="votes")
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["employee", "date"]
        ordering = ["-created_at"]

    def __str__(self):
        username = getattr(self.employee, "username", None)
        return f"{username} voted for {self.menu}"
