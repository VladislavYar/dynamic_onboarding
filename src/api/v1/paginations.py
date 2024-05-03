from django.utils.translation import gettext_lazy as _
from rest_framework.pagination import LimitOffsetPagination


class SurveyDataPagination(LimitOffsetPagination):
    """Limit offset данных по опросам."""

    limit_query_description = _(
        'Количество результатов, возвращаемых на страницу.'
        )
    offset_query_description = _(
        'Начальный индекс, по которому будут выводиться результаты.'
        )
    max_limit = 5
    default_limit = 5
