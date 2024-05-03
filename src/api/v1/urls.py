from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from api.v1.views import SurveyDataListView

app_name = 'v1'


urlpatterns = (
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path(
        'docs/', SpectacularSwaggerView.as_view(url_name='api:v1:schema'),
        name='docs',
        ),
    path('survey-data/', SurveyDataListView.as_view(), name='survey_data'),
)
