"""
URL configuration for user profile microservice.
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    # Admin interface
    path('admin/', admin.site.urls),

    # Health check endpoint (for microservice monitoring)
    path('health/', include('health_check.urls')),

    # API endpoints
    path('api/v1/profiles/', include('apps.user_profile.urls')),

    # API documentation (OpenAPI/Swagger)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
