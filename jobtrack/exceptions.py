"""
Custom exception handling for the JobTrack API.

Wraps DRF's default exception handler so that:
  * Expected errors (validation, auth, permission, not-found) are returned
    with clear, user-friendly messages.
  * Unexpected server errors are logged, but a generic message is returned
    to the client instead of leaking internal details (stack traces, SQL,
    etc.) to end users.
"""

import logging

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        # Normalise the error payload shape: {"detail": ..., "errors": {...}}
        if isinstance(response.data, dict) and "detail" not in response.data:
            response.data = {"detail": "Please correct the errors below.", "errors": response.data}
        return response

    # Anything not handled by DRF is an unexpected server error.
    logger.exception("Unhandled server error: %s", exc)
    return Response(
        {"detail": "Something went wrong on our end. Please try again later."},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
