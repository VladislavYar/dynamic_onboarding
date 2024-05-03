import django_filters
from django.contrib.auth import get_user_model

from onboarding.models import Survey, SurveyData

User = get_user_model()


class SurveyDataFilter(django_filters.FilterSet):
    """Фильтр данных по опросам."""

    survey = django_filters.CharFilter(
        field_name='survey__slug',
        lookup_expr='exact',
        label=Survey._meta.get_field('slug').verbose_name,
        )
    user = django_filters.CharFilter(
        field_name='user__email',
        lookup_expr='exact',
        label=User._meta.get_field('email').verbose_name,
        )

    class Meta:
        model = SurveyData
        fields = (
            'survey',
            'user',
        )
