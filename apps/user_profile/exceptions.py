"""
Custom exception handler for consistent error responses.
Following microservice best practices for error handling.
"""
import logging
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Custom exception handler that provides consistent error response format.

    Returns error responses in the format:
    {
        "error": "error_type",
        "message": "detailed error message",
        "details": {...}  # optional
    }
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)

    if response is not None:
        # Log the error
        logger.error(
            f"API Error: {exc.__class__.__name__} - {str(exc)}",
            extra={'context': context}
        )

        # Customize the response format
        custom_response_data = {
            'error': exc.__class__.__name__,
            'message': str(exc),
        }

        # Add validation errors if present
        if hasattr(exc, 'detail'):
            custom_response_data['details'] = response.data

        response.data = custom_response_data

    return response
