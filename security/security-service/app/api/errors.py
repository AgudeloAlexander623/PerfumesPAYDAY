import logging
import uuid
from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger(__name__)

ERROR_CODES = {
    400: "BAD_REQUEST",
    401: "UNAUTHORIZED",
    403: "FORBIDDEN",
    404: "NOT_FOUND",
    409: "CONFLICT",
    422: "BUSINESS_RULE_VIOLATION",
    429: "RATE_LIMITED",
    500: "INTERNAL_ERROR",
    503: "SERVICE_UNAVAILABLE",
}


def _error_body(
    request: Request,
    code: str,
    message: str,
    details: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    error: dict[str, Any] = {
        "code": code,
        "message": message,
        "requestId": getattr(request.state, "request_id", None) or str(uuid.uuid4()),
    }

    if details:
        error["details"] = details

    return {"error": error}


def register_error_handlers(app: FastAPI) -> None:
    """Aplica el envelope de error de ADR-0006 y propaga `x-request-id`."""

    @app.middleware("http")
    async def request_id_middleware(request: Request, call_next):
        incoming = request.headers.get("x-request-id", "").strip()
        request.state.request_id = incoming or str(uuid.uuid4())
        response = await call_next(request)
        response.headers["x-request-id"] = request.state.request_id
        return response

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(
        request: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        details = [
            {
                "field": ".".join(str(part) for part in error["loc"][1:]),
                "code": error["type"].upper(),
                "message": error["msg"],
            }
            for error in exc.errors()
        ]
        return JSONResponse(
            status_code=400,
            content=_error_body(
                request,
                "VALIDATION_ERROR",
                "Los datos enviados no son válidos.",
                details,
            ),
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_error_handler(
        request: Request,
        exc: StarletteHTTPException,
    ) -> JSONResponse:
        code = ERROR_CODES.get(exc.status_code, "ERROR")
        return JSONResponse(
            status_code=exc.status_code,
            content=_error_body(request, code, str(exc.detail)),
        )

    @app.exception_handler(Exception)
    async def unhandled_error_handler(
        request: Request,
        exc: Exception,
    ) -> JSONResponse:
        logger.exception("Error no controlado", exc_info=exc)
        return JSONResponse(
            status_code=500,
            content=_error_body(
                request,
                "INTERNAL_ERROR",
                "Error interno del servidor.",
            ),
        )