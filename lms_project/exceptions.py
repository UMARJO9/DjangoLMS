from typing import Optional

from django.conf import settings
from rest_framework.views import exception_handler as drf_default_exception_handler
from rest_framework.response import Response

from .api import error


def drf_exception_handler(exc, context) -> Optional[Response]:
    """Wrap DRF exceptions into a unified API envelope.

    Returns: Response with shape {success, message, code, result, errors?}
    """
    response = drf_default_exception_handler(exc, context)

    if response is not None:
        message = _extract_message(response.data)
        return error(message=message, code=response.status_code, errors=response.data)

    # Unhandled exceptions -> 500
    message = "Internal Server Error"
    if getattr(settings, "DEBUG", False):
        message = f"{message}: {exc}"
    return error(message=message, code=500)


def _extract_message(data) -> str:
    """Try to derive a human-friendly message from DRF error payloads."""
    if isinstance(data, dict):
        for key in ("detail", "non_field_errors"):
            if key in data:
                val = data[key]
                if isinstance(val, (list, tuple)) and val:
                    return str(val[0])
                return str(val)
        # Fallback: first item
        if data:
            first_key = next(iter(data.keys()))
            val = data[first_key]
            if isinstance(val, (list, tuple)) and val:
                return str(val[0])
            return f"{first_key}: {val}"
    elif isinstance(data, (list, tuple)) and data:
        return str(data[0])
    return "Error"

