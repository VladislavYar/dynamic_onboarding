from rest_framework.generics import ListAPIView

from api.v1.filters import SurveyDataFilter
from api.v1.paginations import SurveyDataPagination
from api.v1.serializers import SurveyDataSerializer
from onboarding.models import SurveyData


class SurveyDataListView(ListAPIView):
    """View вывода списка ответов на опросы."""

    queryset = SurveyData.objects.all()
    serializer_class = SurveyDataSerializer
    pagination_class = SurveyDataPagination
    filterset_class = SurveyDataFilter
