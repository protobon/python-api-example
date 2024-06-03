from fastapi import APIRouter

from app.router.product import router as product

api_router = APIRouter(
    prefix="/api",
    responses={
        404: {"description": "Not found"},
        408: {"description": "Timeout"}
        }
    )

routers = [product]

for router in routers:
    api_router.include_router(router)
