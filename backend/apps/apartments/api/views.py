import logging
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework import viewsets, permissions, filters
from rest_framework.exceptions import APIException
from django_filters.rest_framework import DjangoFilterBackend

from apps.apartments.models import Apartment
from apps.apartments.api.serializers import ApartmentSerializer
from apps.apartments.api.permissions import IsOwnerOrReadOnly

logger = logging.getLogger(__name__)


@method_decorator(cache_page(60 * 5), name="list")
@method_decorator(cache_page(60 * 5), name="retrieve")
class ApartmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing apartments.
    """

    serializer_class = ApartmentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    lookup_field = "slug"
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["availability", "number_of_rooms"]
    search_fields = ["name", "description"]

    def get_queryset(self):
        """
        Returns a queryset of apartments with optional filtering by price.

        Supports filtering by minimum and maximum price through the query parameters
        `price_min` and `price_max` respectively.
        """
        queryset = Apartment.objects.select_related("owner").only(
            "id",
            "name",
            "slug",
            "description",
            "price",
            "number_of_rooms",
            "square",
            "availability",
            "owner__email",
            "created_at",
            "updated_at",
        )
        price_min = self.request.query_params.get("price_min")
        price_max = self.request.query_params.get("price_max")
        if price_min:
            queryset = queryset.filter(price__gte=price_min)
        if price_max:
            queryset = queryset.filter(price__lte=price_max)
        return queryset

    def perform_create(self, serializer):
        """
        Creates a new apartment.

        Automatically sets the owner of the apartment to the current user.
        Handles potential exceptions during creation.
        """
        try:
            serializer.save(owner=self.request.user)
            logger.info(f"Apartment created by {self.request.user.email}")
        except Exception as e:
            logger.exception("Error creating apartment")
            raise APIException("Error creating apartment")

    def perform_update(self, serializer):
        """
        Updates an existing apartment.

        Handles potential exceptions during the update. The owner cannot be changed,
        as it is set during creation.
        """
        try:
            serializer.save()
            logger.info(f"Apartment updated by {self.request.user.email}")
        except Exception as e:
            logger.exception("Error updating apartment")
            raise APIException("Error updating apartment")

    def perform_destroy(self, instance):
        """
        Deletes an apartment.

        Handles potential exceptions during deletion.
        """
        try:
            logger.info(f"Apartment deleted by {self.request.user.email}")
            instance.delete()
        except Exception as e:
            logger.exception("Error while deleting apartment")
            raise APIException("Error while deleting apartment")
