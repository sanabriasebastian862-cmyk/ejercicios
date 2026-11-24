from contextlib import asynccontextmanager
from fastapi import FastAPI

from core.config import settings
from core.database import Base, engine
from models.mecanico import Mecanico  # noqa: F401
from models.orden import Orden  # noqa: F401
from models.repuesto import Repuesto  # noqa: F401
from routers import mecanicos, ordenes


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

app.include_router(ordenes.router)
app.include_router(mecanicos.router)