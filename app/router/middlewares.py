from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.cache.base import Cache


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        req_count = await Cache.get_req_count(client_ip)
        if req_count and int(req_count) >= Cache.max_req:
            return Response(content="Too Many Requests", status_code=429)

        await Cache.increase_req_count(client_ip, req_count)

        response = await call_next(request)
        return response
