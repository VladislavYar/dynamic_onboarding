from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.core.handlers.wsgi import WSGIRequest

User = get_user_model()


def login_form(request: WSGIRequest) -> dict[AuthenticationForm]:
    """Добавляет форму входа."""
    return {
        'login_form': AuthenticationForm()
    }
