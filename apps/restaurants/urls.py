from django.urls import path
from .views import RestaurantListCreateView, RestaurantRetrieveView

urlpatterns = [
    path("", RestaurantListCreateView.as_view(), name="restaurant-list-create"),
    path("<int:pk>/", RestaurantRetrieveView.as_view(), name="restaurant-retrieve"),
]
