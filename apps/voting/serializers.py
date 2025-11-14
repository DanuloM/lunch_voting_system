from rest_framework import serializers
from .models import Vote
from apps.menus.models import Menu
from datetime import date


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ["id", "employee", "menu", "date", "created_at"]
        read_only_fields = ["id", "employee", "date", "created_at"]

    def validate(self, data):
        user = self.context["request"].user
        menu = data["menu"]
        today = date.today()

        if menu.date != today:
            raise serializers.ValidationError("You can only vote for today's menu.")

        if Vote.objects.filter(employee=user, date=today).exists():
            raise serializers.ValidationError("You already voted today.")

        return data

    def create(self, validated_data):
        validated_data["employee"] = self.context["request"].user
        validated_data["date"] = date.today()
        return super().create(validated_data)
