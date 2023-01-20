from django.contrib import admin
from django.urls import path, include, re_path
from django_hyperlink.settings import API_PATH, API_FOLDER, DEBUG


urlpatterns = [
    path('users/', include('users.urls')),

    path('admin/', admin.site.urls),
    path('', include('link.urls')),

    path(API_PATH, include(API_FOLDER))
]

if DEBUG:
    from rest_framework import permissions
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
        re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    ]
    urlpatterns += yasg_patterns
    urlpatterns.append(path('__debug__/', include('debug_toolbar.urls')))