from typing import Any, Optional, Dict
from rest_framework.response import Response


def success(result: Any = None, message: str = "OK", code: int = 200, headers: Optional[Dict[str, str]] = None) -> Response:
    return Response(
        {
            "success": True,
            "message": message,
            "code": code,
            "result": result,
        },
        status=code,
        headers=headers or {},
    )


def error(message: str = "Error", code: int = 400, errors: Any = None, headers: Optional[Dict[str, str]] = None) -> Response:
    payload = {
        "success": False,
        "message": message,
        "code": code,
        "result": None,
    }
    if errors is not None:
        payload["errors"] = errors
    return Response(payload, status=code, headers=headers or {})

