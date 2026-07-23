from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.collectors import router as collectors_router
from app.api.routes.dashboard import router as dashboard_router
from app.api.routes.health import router as health_router
from app.api.routes.listings import router as listings_router
from app.api.routes.manual_intake import router as manual_intake_router
from app.core.config import settings
from app.services.scheduler import scheduler_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler_service.start()
    yield
    scheduler_service.stop()


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(listings_router, prefix="/api/v1")
app.include_router(manual_intake_router, prefix="/api/v1")
app.include_router(collectors_router, prefix="/api/v1")
app.include_router(dashboard_router, prefix="/api/v1")
