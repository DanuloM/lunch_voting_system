from rest_framework import serializers
from rest_framework.relations import StringRelatedField

from .models import MenuItem, Menu


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ["id", "name", "description", "price", "category"]


class MenuSerializer(serializers.ModelSerializer):
    items = MenuItemSerializer(many=True)
    restaurant_name = StringRelatedField(source="restaurant", read_only=True)

    class Meta:
        model = Menu
        fields = ["id", "restaurant", "restaurant_name", "date", "items", "created_at"]
        read_only_fields = ["id", "created_at"]

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        menu = Menu.objects.create(**validated_data)

        for item in items_data:
            MenuItem.objects.create(menu=menu, **item)

        return menu

    def update(self, instance, validated_data):
        items_data = validated_data.pop("items", [])

        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()

        instance.items.all().delete()

        for item in items_data:
            MenuItem.objects.create(menu=instance, **item)

        return instance
