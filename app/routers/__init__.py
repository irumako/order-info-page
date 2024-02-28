from fastapi import APIRouter

from app.routers import orders

api_router = APIRouter()
api_router.include_router(orders.router, prefix="/orders", tags=["orders"])
