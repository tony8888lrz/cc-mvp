"""
URL configuration for user profile microservice.
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    # Metrics endpoint for Prometheus
    path('', include('django_prometheus.urls')),

    # Admin interface
    path('admin/', admin.site.urls),

    # Auth (built-in login/logout/password management)
    path('accounts/', include('django.contrib.auth.urls')),

    # Simple front-end page for profile CRUD demo
    path('profiles/demo/', TemplateView.as_view(template_name='profiles/dashboard.html'), name='profiles-demo'),

    # Health check endpoint (for microservice monitoring)
    path('health/', include('health_check.urls')),

    # API endpoints
    path('api/v1/profiles/', include('apps.user_profile.urls')),

    # API documentation (OpenAPI/Swagger)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
