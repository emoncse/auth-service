from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

api_docs_schema_view = get_schema_view(
   openapi.Info(
      title="Organization Service",
      default_version='v1',
      description="Organization Service API documentation",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)
