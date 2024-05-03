from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import EmailField

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    """Кастомная форма создания пользователя."""

    email = EmailField()

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')
