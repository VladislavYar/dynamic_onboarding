from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('api/', include('api.urls', namespace='api')),
    path('', include('onboarding.urls', namespace='onboarding')),
    path('', include('users.urls', namespace='users')),
    path('admin/', admin.site.urls),
]

handler400 = 'config.views.page_4xx'
handler403 = 'config.views.page_4xx'
handler404 = 'config.views.page_4xx'


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
