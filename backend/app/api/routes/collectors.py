from fastapi import APIRouter

from app.services.collectors.registry import collector_registry
from app.services.scheduler import scheduler_service

router = APIRouter(prefix="/collectors", tags=["collectors"])


@router.get("/status")
def collector_status() -> dict[str, object]:
    return {
        "sources": collector_registry.source_names(),
        "scheduler_running": scheduler_service.is_running,
        "interval_minutes": scheduler_service.interval_minutes,
    }


@router.post("/run")
def run_collectors_once() -> dict[str, object]:
    result = scheduler_service.run_collection_once()
    return {"status": "completed", "result": result}

