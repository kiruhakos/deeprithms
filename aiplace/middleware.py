from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from datetime import date
from django.http import HttpResponseForbidden
from ipware import get_client_ip
from django.utils.translation import activate, get_language

class JWTTokenMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Check if the user is authenticated and if the Authorization header is not already set
        if request.user.is_authenticated and "HTTP_AUTHORIZATION" not in request.META:
            refresh = RefreshToken.for_user(request.user)
            token = str(refresh.access_token)
            # Add the JWT token to the Authorization header in the request.META dictionary
            request.META["HTTP_AUTHORIZATION"] = f"Bearer {token}"

class UKTranslationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip, routable = get_client_ip(request)
        
        if ip and routable:
            country_code = get_country_code_from_ip(client_ip)

            if country_code == "UA":
                activate('uk')
            else:
                activate('en')

        response = self.get_response(request)
        return response

class RestrictruUsersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip, _ = get_client_ip(request)
        if ip is not None and ip.startswith("RU"):
            return HttpResponseForbidden("Deeprithms не доступний у рф. Deeprithms is unavailable in rf.")
        return self.get_response(request)