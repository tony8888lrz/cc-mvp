"""
URL routing for User Profile API.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet

# Create a router and register our viewset
router = DefaultRouter()
router.register(r'', UserProfileViewSet, basename='userprofile')

urlpatterns = [
    path('', include(router.urls)),
]
