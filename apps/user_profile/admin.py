"""
Admin configuration for User Profile management.
"""
from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Admin interface for UserProfile model.
    """
    list_display = [
        'id',
        'email',
        'first_name',
        'last_name',
        'phone_number',
        'city',
        'state',
        'country',
        'is_active',
        'created_at',
    ]
    list_filter = [
        'is_active',
        'country',
        'state',
        'created_at',
    ]
    search_fields = [
        'email',
        'first_name',
        'last_name',
        'phone_number',
    ]
    readonly_fields = [
        'id',
        'created_at',
        'updated_at',
        'full_name',
        'full_address',
    ]
    fieldsets = (
        ('Basic Information', {
            'fields': ('email', 'first_name', 'last_name', 'full_name', 'phone_number')
        }),
        ('Address Information', {
            'fields': (
                'address_line1',
                'address_line2',
                'city',
                'state',
                'postal_code',
                'country',
                'full_address',
            )
        }),
        ('Additional Information', {
            'fields': ('date_of_birth', 'bio')
        }),
        ('Status & Metadata', {
            'fields': ('is_active', 'created_at', 'updated_at')
        }),
    )
    ordering = ['-created_at']
    list_per_page = 25

    def get_queryset(self, request):
        """
        Override to include soft-deleted profiles in admin.
        """
        return super().get_queryset(request)
