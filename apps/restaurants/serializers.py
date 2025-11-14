from rest_framework import serializers
from .models import Restaurant


class RestaurantSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Restaurant
        fields = ["id", "name", "owner", "address", "created_at"]
        read_only_fields = ["id", "created_at"]
