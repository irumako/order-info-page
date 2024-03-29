from fastapi import APIRouter

from . import orders

api_router = APIRouter()
api_router.include_router(orders.router, prefix="/orders", tags=["orders"])
