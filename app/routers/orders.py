from pathlib import Path
from typing import Annotated

import aiofiles

from aiofiles.os import makedirs
from fastapi import APIRouter, Request, Depends, UploadFile, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from repositories.sqlalchemy import SqlAlchemyRepository
from services.order import OrderService
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

import models
import schemas
from .deps import PaginationParams, get_db
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
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content="detail: Key (id) already exists.")

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder(order))


@router.post("/uploadfiles/{order_id}")
async def create_upload_files(order_id: str, files: list[UploadFile],
                              db_session: Annotated[AsyncSession, Depends(get_db)]) -> JSONResponse:
    order = await OrderService(SqlAlchemyRepository(models.Order, db_session)).get(order_id)
    if not order:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content="detail: There is no order with this number.")

    for f in files:
        file_dir = f"{settings.BASE_DIR}/{settings.STATICFILES_DIR}/{order_id}"
        await makedirs(file_dir, exist_ok=True)

        async with aiofiles.open(f"{file_dir}/{f.filename}", 'wb') as out_file:
            content = await f.read()
            await out_file.write(content)

        order.__dict__['files'].append(f.filename)

    await OrderService(SqlAlchemyRepository(models.Order, db_session)).update(
        order_id, {'files': order.__dict__['files']})

    return JSONResponse(status_code=status.HTTP_200_OK, content="detail: Files have been saved successfully.")


@router.get("/{order_id}", response_class=HTMLResponse)
async def get_order_information(request: Request, order_id: str,
                                db_session: Annotated[AsyncSession, Depends(get_db)],
                                pagination: Annotated[PaginationParams, Depends(PaginationParams)]) -> templates.TemplateResponse:
    order = await OrderService(SqlAlchemyRepository(models.Order, db_session)).get(order_id)
    if not order:
        return templates.TemplateResponse(request=request, name="empty.html")

    total_pages = pagination.get_total_pages(len(order.products))
    current_page = pagination.get_current_page(total_pages)

    return templates.TemplateResponse(
        request=request, name="order.html", context={
            "order": order,
            "current_page": current_page,
            "total_pages": total_pages,
            "step": pagination.step
        }
    )
