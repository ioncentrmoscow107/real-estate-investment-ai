from fastapi import APIRouter

from app.services.dashboard_samples import get_sample_dashboard_properties

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/properties")
def dashboard_properties() -> dict:
    return get_sample_dashboard_properties()

