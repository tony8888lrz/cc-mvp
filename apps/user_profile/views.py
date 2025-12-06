"""
Views for User Profile API endpoints.
Following RESTful principles and microservice best practices.
"""
import logging
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view

from .models import UserProfile
from .serializers import (
    UserProfileSerializer,
    UserProfileCreateSerializer,
    UserProfileUpdateSerializer,
    UserProfileListSerializer,
)

logger = logging.getLogger(__name__)


@extend_schema_view(
    list=extend_schema(description='List all user profiles with pagination and filtering'),
    create=extend_schema(description='Create a new user profile'),
    retrieve=extend_schema(description='Retrieve a specific user profile by ID'),
    update=extend_schema(description='Update a user profile completely'),
    partial_update=extend_schema(description='Partially update a user profile'),
    destroy=extend_schema(description='Delete a user profile (soft delete)'),
)
class UserProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing user profiles.

    Provides CRUD operations:
    - GET /api/v1/profiles/ - List all profiles (with pagination)
    - POST /api/v1/profiles/ - Create a new profile
    - GET /api/v1/profiles/{id}/ - Retrieve a specific profile
    - PUT /api/v1/profiles/{id}/ - Update a profile (full update)
    - PATCH /api/v1/profiles/{id}/ - Partially update a profile
    - DELETE /api/v1/profiles/{id}/ - Delete a profile (soft delete)
    """

    queryset = UserProfile.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'country', 'state', 'city']
    search_fields = ['email', 'first_name', 'last_name', 'phone_number']
    ordering_fields = ['created_at', 'updated_at', 'email', 'last_name']
    ordering = ['-created_at']

    def get_serializer_class(self):
        """
        Return appropriate serializer class based on action.
        """
        if self.action == 'list':
            return UserProfileListSerializer
        elif self.action == 'create':
            return UserProfileCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserProfileUpdateSerializer
        return UserProfileSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new user profile.
        """
        logger.info(f"Creating new user profile with email: {request.data.get('email')}")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Return full profile data
        profile = UserProfile.objects.get(pk=serializer.instance.pk)
        response_serializer = UserProfileSerializer(profile)

        logger.info(f"User profile created successfully: ID {profile.id}")

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        """
        Update a user profile (full update).
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        logger.info(f"Updating user profile: ID {instance.id}")

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Return full profile data
        profile = UserProfile.objects.get(pk=instance.pk)
        response_serializer = UserProfileSerializer(profile)

        logger.info(f"User profile updated successfully: ID {profile.id}")

        return Response(response_serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        Soft delete a user profile by marking it as inactive.
        This follows microservice best practices for data retention.
        """
        instance = self.get_object()

        logger.info(f"Soft deleting user profile: ID {instance.id}")

        # Perform soft delete
        instance.soft_delete()

        logger.info(f"User profile soft deleted successfully: ID {instance.id}")

        return Response(
            {"message": "User profile deactivated successfully"},
            status=status.HTTP_204_NO_CONTENT
        )

    @extend_schema(
        description='Get active user profiles only',
        responses={200: UserProfileListSerializer(many=True)}
    )
    @action(detail=False, methods=['get'])
    def active(self, request):
        """
        Custom endpoint to get only active profiles.
        Endpoint: GET /api/v1/profiles/active/
        """
        active_profiles = self.queryset.filter(is_active=True)
        page = self.paginate_queryset(active_profiles)

        if page is not None:
            serializer = UserProfileListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = UserProfileListSerializer(active_profiles, many=True)
        return Response(serializer.data)

    @extend_schema(
        description='Search profiles by email',
        responses={200: UserProfileSerializer}
    )
    @action(detail=False, methods=['get'])
    def search_by_email(self, request):
        """
        Custom endpoint to search profile by email.
        Endpoint: GET /api/v1/profiles/search_by_email/?email=user@example.com
        """
        email = request.query_params.get('email', None)

        if not email:
            return Response(
                {"error": "Email parameter is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            profile = UserProfile.objects.get(email=email.lower())
            serializer = UserProfileSerializer(profile)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            return Response(
                {"error": "Profile not found"},
                status=status.HTTP_404_NOT_FOUND
            )

    @extend_schema(
        description='Reactivate a deactivated profile',
        responses={200: UserProfileSerializer}
    )
    @action(detail=True, methods=['post'])
    def reactivate(self, request, pk=None):
        """
        Reactivate a soft-deleted (inactive) profile.
        Endpoint: POST /api/v1/profiles/{id}/reactivate/
        """
        instance = self.get_object()

        if instance.is_active:
            return Response(
                {"message": "Profile is already active"},
                status=status.HTTP_400_BAD_REQUEST
            )

        instance.is_active = True
        instance.save()

        logger.info(f"User profile reactivated: ID {instance.id}")

        serializer = UserProfileSerializer(instance)
        return Response(serializer.data)
