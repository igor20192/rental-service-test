from rest_framework import serializers
from apps.apartments.models import Apartment


class ApartmentSerializer(serializers.ModelSerializer):
    owner_email = serializers.EmailField(source="owner.email", read_only=True)
    """
    Serializer for the Apartment model.
    """

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
        """
        Creates a new apartment instance.

        Sets the owner of the apartment to the current user making the request.
        """
        validated_data["owner"] = self.context["request"].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        Updates an existing apartment instance.

        Removes the 'owner' field from the validated data to prevent changing the owner
        during updates.
        """
        validated_data.pop("owner", None)
        return super().update(instance, validated_data)
