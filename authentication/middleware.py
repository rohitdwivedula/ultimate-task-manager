from rest_framework_simplejwt import authentication

from .conf import JWT_COOKIE_KEY

class JWTCookieAuthentication(authentication.JWTAuthentication):
    """Authentication pluging that uses Bearer token set in cookie"""
    def authenticate(self, request):
        token = request.COOKIES.get(JWT_COOKIE_KEY, "")

        if not token:
            return None

        validated_token = self.get_validated_token(token)

        return self.get_user(validated_token), validated_token