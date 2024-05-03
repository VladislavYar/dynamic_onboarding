from django.core.handlers.wsgi import WSGIRequest
from django.http.response import HttpResponse
from django.shortcuts import redirect


class HttpResponseNotAllowedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: WSGIRequest) -> HttpResponse:
        """
        Редирект на главную страницу в случае
        ошибки 405.
        """
        response = self.get_response(request)
        if response.status_code == 405:
            return redirect('onboarding:index')
        return response
