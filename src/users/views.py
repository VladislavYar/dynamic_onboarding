from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.views import LoginView
from django.core.handlers.wsgi import WSGIRequest
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.views import View

from users.forms import CustomUserCreationForm

User = get_user_model()


class LoginSignUpView(View):
    """View регистрации или авторизации пользователя."""

    def user_registration(
            self,
            request: WSGIRequest,
            email: str | None,
            password1: str | None,
            password2: str | None
            ) -> None:
        """Регистрация пользователя."""
        form = CustomUserCreationForm(
                {
                 'email': email,
                 'password1': password1,
                 'password2': password2
                }
            )
        if not form.is_valid():
            return render(request, 'onboarding/index.html', {'form': form})
        new_user = form.save()
        new_user = authenticate(
                username=form.cleaned_data['email'],
                password=form.cleaned_data['password1'],
            )
        login(request, new_user)
        return redirect('onboarding:index')

    def post(self, request: WSGIRequest) -> HttpResponse:
        """Регистрация или авторизация пользователя."""
        if request.user.is_authenticated and request.method != 'POST':
            return redirect('onboarding:index')

        email = request.POST.get('username')
        if User.objects.filter(email=email).exists():
            return LoginView.as_view()(request)

        password = request.POST.get('password')
        return self.user_registration(request, email, password, password)
