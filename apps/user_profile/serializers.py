"""
Serializers for User Profile API.
"""
from rest_framework import serializers
from .models import UserProfile
from datetime import date


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for UserProfile model with comprehensive validation.
    """
    full_name = serializers.ReadOnlyField()
    full_address = serializers.ReadOnlyField()

    class Meta:
        model = UserProfile
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'full_name',
            'phone_number',
            'address_line1',
            'address_line2',
            'city',
            'state',
            'postal_code',
            'country',
            'full_address',
            'date_of_birth',
            'bio',
            'is_active',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'full_name', 'full_address']

    def validate_email(self, value):
        """
        Validate email is unique (except for updates).
        """
        if value:
            value = value.lower().strip()
            # Check if email already exists (excluding current instance on update)
            queryset = UserProfile.objects.filter(email=value)
            if self.instance:
                queryset = queryset.exclude(pk=self.instance.pk)
            if queryset.exists():
                raise serializers.ValidationError("A profile with this email already exists.")
        return value

    def validate_date_of_birth(self, value):
        """
        Validate date of birth is not in the future.
        """
        if value and value > date.today():
            raise serializers.ValidationError("Date of birth cannot be in the future.")
        return value

    def validate_bio(self, value):
        """
        Validate bio length.
        """
        if value and len(value) > 500:
            raise serializers.ValidationError("Bio cannot exceed 500 characters.")
        return value


class UserProfileCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating user profiles with required fields.
    """

    class Meta:
        model = UserProfile
        fields = [
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'address_line1',
            'address_line2',
            'city',
            'state',
            'postal_code',
            'country',
            'date_of_birth',
            'bio',
        ]

    def validate_email(self, value):
        """
        Validate email is unique and properly formatted.
        """
        if value:
            value = value.lower().strip()
            if UserProfile.objects.filter(email=value).exists():
                raise serializers.ValidationError("A profile with this email already exists.")
        return value

    def validate_date_of_birth(self, value):
        """
        Validate date of birth is not in the future.
        """
        if value and value > date.today():
            raise serializers.ValidationError("Date of birth cannot be in the future.")
        return value


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user profiles (partial updates allowed).
    """

    class Meta:
        model = UserProfile
        fields = [
            'first_name',
            'last_name',
            'phone_number',
            'address_line1',
            'address_line2',
            'city',
            'state',
            'postal_code',
            'country',
            'date_of_birth',
            'bio',
        ]

    def validate_date_of_birth(self, value):
        """
        Validate date of birth is not in the future.
        """
        if value and value > date.today():
            raise serializers.ValidationError("Date of birth cannot be in the future.")
        return value


class UserProfileListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing user profiles.
    """
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = UserProfile
        fields = [
            'id',
            'email',
            'full_name',
            'city',
            'state',
            'is_active',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at', 'full_name']
