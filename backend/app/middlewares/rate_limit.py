"""Rate limiting middleware directly without decorators."""
import time
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import settings

# In-memory store for rate limiting: { "ip": [timestamp1, timestamp2, ...] }
request_counts = {}

class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host if request.client else "unknown"
        
        now = time.time()
        window_start = now - 60  # 1 minute window
        
        # Clean up old requests
        if client_ip in request_counts:
            request_counts[client_ip] = [ts for ts in request_counts[client_ip] if ts > window_start]
        else:
            request_counts[client_ip] = []
            
        # Check limit
        if len(request_counts[client_ip]) >= settings.RATE_LIMIT_PER_MINUTE:
            return JSONResponse(
                status_code=429,
                content={
                    "success": False,
                    "message": f"Terlalu banyak permintaan. Batas: {settings.RATE_LIMIT_PER_MINUTE} per menit.",
                    "detail": "Rate limit exceeded"
                }
            )
            
        # Add current request timestamp
        request_counts[client_ip].append(now)
        
        response = await call_next(request)
        return response
