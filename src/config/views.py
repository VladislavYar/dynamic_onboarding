from django.core.handlers.wsgi import WSGIRequest
from django.http.response import Http404, HttpResponse
from django.shortcuts import redirect


def page_4xx(request: WSGIRequest, exception: Http404) -> HttpResponse:
    """Редирект ошибок 4xx."""
    return redirect('onboarding:index')
