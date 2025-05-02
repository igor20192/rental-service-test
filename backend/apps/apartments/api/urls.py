from rest_framework.routers import DefaultRouter
from django.urls import path, include
from apps.apartments.api.views import ApartmentViewSet

router = DefaultRouter()
router.register(r"", ApartmentViewSet, basename="apartments")

urlpatterns = [
    path("", include(router.urls)),
]
