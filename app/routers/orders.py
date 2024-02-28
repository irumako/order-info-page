from pathlib import Path
from typing import Annotated

from config import settings
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from deps import get_db

templates = Jinja2Templates(directory=str(Path(settings.BASE_DIR, settings.TEMPLATES_DIR)))

router = APIRouter(
    responses={404: {"description": "Not found"}},
)


@router.get("/{order_id}", response_class=HTMLResponse)
async def get_order_information(request: Request, order_id: UUID4,
                                db_session: Annotated[AsyncSession, Depends(get_db)]):
    return templates.TemplateResponse(
        request=request, name="order.html", context={
            "id": order_id,
        }
    )
