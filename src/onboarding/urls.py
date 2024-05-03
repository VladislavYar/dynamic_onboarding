from django.urls import path

from onboarding.views import OnboardingView

app_name = 'onboarding'


urlpatterns = (
    path('', OnboardingView.as_view(
            http_method_names=('get', 'post',)
        ), name='index'),
    )
