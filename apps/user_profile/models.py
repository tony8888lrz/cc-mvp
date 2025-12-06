"""
User Profile models for storing user information.
"""
from django.db import models, transaction
from django.core.validators import EmailValidator, RegexValidator
from django.utils import timezone


class UserProfile(models.Model):
    """
    User profile model for storing user information.

    This model follows microservice best practices by being self-contained
    and not relying on Django's built-in User model (for service independence).
    """

    # Phone number validator
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )

    # Basic Information
    email = models.EmailField(
        unique=True,
        validators=[EmailValidator()],
        db_index=True,
        help_text="User's email address (unique identifier)"
    )
    first_name = models.CharField(
        max_length=50,
        help_text="User's first name"
    )
    last_name = models.CharField(
        max_length=50,
        help_text="User's last name"
    )
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=17,
        blank=True,
        null=True,
        help_text="User's phone number"
    )

    # Address Information
    address_line1 = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Primary address line"
    )
    address_line2 = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Secondary address line (apartment, suite, etc.)"
    )
    city = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="City"
    )
    state = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="State or province"
    )
    postal_code = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="Postal or ZIP code"
    )
    country = models.CharField(
        max_length=100,
        default='USA',
        help_text="Country"
    )

    # Additional Information
    date_of_birth = models.DateField(
        blank=True,
        null=True,
        help_text="User's date of birth"
    )
    bio = models.TextField(
        blank=True,
        null=True,
        max_length=500,
        help_text="Short biography or description"
    )

    # Status and Metadata
    is_active = models.BooleanField(
        default=True,
        help_text="Whether the profile is active"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the profile was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the profile was last updated"
    )

    class Meta:
        db_table = 'user_profiles'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['created_at']),
            models.Index(fields=['is_active']),
        ]
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

    @property
    def full_name(self):
        """Returns the user's full name."""
        return f"{self.first_name} {self.last_name}"

    @property
    def full_address(self):
        """Returns the complete address as a formatted string."""
        address_parts = [
            self.address_line1,
            self.address_line2,
            self.city,
            self.state,
            self.postal_code,
            self.country
        ]
        return ', '.join(filter(None, address_parts))

    @transaction.atomic
    def soft_delete(self):
        """Soft delete the profile by marking it as inactive."""
        self.is_active = False
        self.save(update_fields=['is_active', 'updated_at'])
