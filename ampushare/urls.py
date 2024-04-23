import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework.versioning import URLPathVersioning

admin.site.site_header = 'AmpuShare Admin'
admin.site.index_title = 'Admin'

schema_view = get_schema_view(
    openapi.Info(
        title="Ampushare API",
        default_version='v1', ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

api_urlpatterns = [
    path('booking/', include('booking.urls')),
    path('social/', include('social.urls')),
    path('user/', include('user.urls')),
]
urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('__debug__/', include(debug_toolbar.urls)),
                  path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
                  path('api/schema/', SpectacularAPIView.as_view(versioning_class=URLPathVersioning), name='schema'),
                  path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path('api/', include(api_urlpatterns)),
]