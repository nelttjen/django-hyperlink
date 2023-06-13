from django.contrib import admin
from django.http import HttpResponsePermanentRedirect
from django.urls import path, include, re_path
from django_hyperlink.settings import API_PATH, API_FOLDER, DEBUG
from rest_framework.schemas import get_schema_view


urlpatterns = [
    path('admin/login/', lambda x: HttpResponsePermanentRedirect('/users/login/?next=/admin')),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('schema/', get_schema_view()),

    path('', include('link.urls')),

    path(API_PATH, include(API_FOLDER))
]

if DEBUG:
    from drf_yasg.views import get_schema_view
    from drf_yasg import openapi

    schema_view = get_schema_view(
        openapi.Info(
            title="API приложения",
            default_version='v1',
            description="Все методы и требуеммые даннные для взаимодействия с приложением",
            terms_of_service="None",
            contact=openapi.Contact(email="artemy96@gmail.com"),
            license=openapi.License(name="MIT License"),
        ),
    )

    yasg_patterns = [
        re_path(r'^docs/swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        re_path(r'^docs/swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        re_path(r'^docs/redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    ]
    urlpatterns += yasg_patterns
    urlpatterns.append(path('__debug__/', include('debug_toolbar.urls')))