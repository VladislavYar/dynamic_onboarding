from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class OnboardingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'onboarding'
    verbose_name = _('Динамические онбординги')
