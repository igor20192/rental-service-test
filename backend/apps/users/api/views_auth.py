from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, exceptions
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class LoginView(APIView):
    """
    API view for user login.

    Allows users to log in by providing their email and password.
    Upon successful authentication, it returns a response with a success message
    and sets HTTP-only cookies for access and refresh tokens.

    Raises:
        AuthenticationFailed: If the provided email or password is incorrect.
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(request, email=email, password=password)
        if not user:
            logger.warning(f"Failed login attempt for {email}")
            raise exceptions.AuthenticationFailed("Incorrect email or password")

        refresh = RefreshToken.for_user(user)
        response = Response({"message": "Successful login"})

        access_expiry = int(
            settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds()
        )
        refresh_expiry = int(
            settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds()
        )

        # Install httpOnly cookie
        response.set_cookie(
            key="access_token",
            value=str(refresh.access_token),
            httponly=True,
            secure=False,  # True on production!
            samesite="Lax",
            max_age=access_expiry,
        )
        response.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age=refresh_expiry,
        )

        return response


class LogoutView(APIView):
    """
    API view for user logout.

    Allows authenticated users to log out. It returns a response with a success
    message and deletes the access and refresh token cookies.

    Requires:
        Authentication: The user must be authenticated to access this view.
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        response = Response({"message": "Exit completed"})
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response


class MeView(APIView):
    """
    API view to retrieve the current user's information.

    Returns the email, first name, last name, and verification status of the
    currently authenticated user.

    Requires:
        Authentication: The user must be authenticated to access this view.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response(
            {
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "is_verified": user.is_verified,
            }
        )


class RefreshTokenView(APIView):
    """
    API view to refresh the access token using a refresh token.

    Retrieves the refresh token from the HTTP-only cookies, validates it, and
    returns a new access token as an HTTP-only cookie.

    Raises:
        AuthenticationFailed: If the refresh token is not found in the cookies.
        InvalidToken: If the refresh token is invalid or expired.

    """

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            raise exceptions.AuthenticationFailed("Refresh token not found")

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
        except Exception:
            raise InvalidToken("Invalid refresh token")

        response = Response({"message": "Token updated"})

        access_expiry = int(
            settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds()
        )

        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age=access_expiry,
        )
        return response
