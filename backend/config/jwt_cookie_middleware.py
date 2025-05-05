class JWTAuthenticationFromCookieMiddleware:
    """
    Middleware to enable JWT authentication from cookies.

    This middleware checks for the presence of an 'access_token' in the request cookies.
    If found and the Authorization header is not already set, it adds the Authorization
    header with the access token as a Bearer token.
    """

    def __init__(self, get_response):
        """Initializes the middleware."""
        self.get_response = get_response

    def __call__(self, request):
        """
        Processes each request.
        """
        access_token = request.COOKIES.get("access_token")
        if access_token and "HTTP_AUTHORIZATION" not in request.META:
            request.META["HTTP_AUTHORIZATION"] = f"Bearer {access_token}"
        return self.get_response(request)
