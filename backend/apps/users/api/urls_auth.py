from django.urls import path
from apps.users.api.views_auth import LoginView, LogoutView, MeView, RefreshTokenView

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("me/", MeView.as_view(), name="me"),
    path("refresh/", RefreshTokenView.as_view(), name="refresh"),
]
