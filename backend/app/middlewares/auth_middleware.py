"""Auth middleware – optional JWT validation on every request."""
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response


class AuthMiddleware(BaseHTTPMiddleware):
    """
    Lightweight middleware that attaches the bearer token (if present)
    to request.state for downstream use. Actual auth enforcement
    is done per-endpoint via FastAPI dependencies.
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            request.state.token = auth_header[len("Bearer "):]
        else:
            request.state.token = None
        return await call_next(request)
