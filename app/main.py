from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

import routers
from config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    debug=settings.DEBUG,
)
app.include_router(routers.orders.router)

app.mount("/static", StaticFiles(directory=str(Path(settings.BASE_DIR, settings.STATICFILES_DIR))), name="static")


@app.get("/")
async def root():
    return {"message": "Hello!"}
