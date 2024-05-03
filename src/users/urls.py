from django.contrib.auth.views import LogoutView
from django.urls import path

from users.views import LoginSignUpView

app_name = 'users'

urlpatterns = (
    path(
        'login/', LoginSignUpView.as_view(http_method_names=['post']),
        name='login',
        ),
    path(
        'logout/', LogoutView.as_view(http_method_names=['post']),
        name='logout',
        ),
)
