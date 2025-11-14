from django.urls import path
from .views import MenuCreateView, MenuTodayView, MenuUpdateView

urlpatterns = [
    path("", MenuCreateView.as_view(), name="menu-create"),
    path("today/", MenuTodayView.as_view(), name="menu-today"),
    path("<int:pk>/", MenuUpdateView.as_view(), name="menu-update"),
]

