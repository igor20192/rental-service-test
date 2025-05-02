from rest_framework import serializers
from apps.apartments.models import Apartment


class ApartmentSerializer(serializers.ModelSerializer):
    owner_email = serializers.EmailField(source="owner.email", read_only=True)

    class Meta:
        model = Apartment
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "price",
            "number_of_rooms",
            "square",
            "availability",
            "owner_email",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ("slug", "owner_email", "created_at", "updated_at")

    def create(self, validated_data):
        validated_data["owner"] = self.context["request"].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop("owner", None)
        return super().update(instance, validated_data)
