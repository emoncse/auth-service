from django.contrib import admin
from django.urls import path, include

from .api_docs import api_docs_schema_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('authentication.urls')),
    path('api/v1/', include('authorization.urls')),
    path(
        'docs',
        api_docs_schema_view.with_ui('swagger', cache_timeout=0),
        name='api-docs-swagger'
    ),
    path(
        'redoc',
        api_docs_schema_view.with_ui('redoc', cache_timeout=0),
        name='api-docs-redoc'
    ),
]
