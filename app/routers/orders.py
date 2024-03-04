from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Request, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from repositories.sqlalchemy import SqlAlchemyRepository
from services.order import OrderService
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

import models
import schemas
from .deps import get_db
from config import settings

templates = Jinja2Templates(directory=str(Path(settings.BASE_DIR, settings.TEMPLATES_DIR)))

router = APIRouter(
    responses={404: {"description": "Not found"}},
)


@router.post("/")
async def create_order(order: schemas.Order,
                       db_session: Annotated[AsyncSession, Depends(get_db)]) -> JSONResponse:
    try:
        await OrderService(SqlAlchemyRepository(models.Order, db_session)).create(order)
    except IntegrityError:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content="DETAIL: Key (id) already exists.")

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder(order))


@router.get("/{order_id}", response_class=HTMLResponse)
async def get_order_information(request: Request, order_id: str,
                                db_session: Annotated[AsyncSession, Depends(get_db)]) -> templates.TemplateResponse:
    order = await OrderService(SqlAlchemyRepository(models.Order, db_session)).get(order_id)
    if not order:
        return templates.TemplateResponse(request=request, name="empty.html")

    return templates.TemplateResponse(
        request=request, name="order.html", context={
            "order": order,
        }
    )
