from typing import Any
from django.shortcuts import redirect

class CookieAcceptanceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.session.test_cookie_worked():
            if request.path != "/api/authentication/cookie-acceptance":
                return redirect("/api/authentication/cookie-acceptance")
        response = self.get_response(request)
        return response