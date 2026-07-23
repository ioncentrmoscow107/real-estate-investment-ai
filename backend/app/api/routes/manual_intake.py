from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.manual_intake import ManualIntakeBatch
from app.schemas.manual_intake import ManualIntakeBatchCreate, ManualIntakeBatchRead
from app.services.manual_intake import (
    build_manual_intake_response,
    create_manual_intake_batch,
)

router = APIRouter(prefix="/manual-intake/batches", tags=["manual-intake"])


@router.post("", response_model=ManualIntakeBatchRead, status_code=status.HTTP_201_CREATED)
def create_batch(
    payload: ManualIntakeBatchCreate,
    db: Session = Depends(get_db),
) -> ManualIntakeBatchRead:
    batch = create_manual_intake_batch(db, payload)
    return build_manual_intake_response(batch)


@router.get("", response_model=list[ManualIntakeBatchRead])
def list_batches(
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
) -> list[ManualIntakeBatchRead]:
    statement = (
        select(ManualIntakeBatch)
        .order_by(ManualIntakeBatch.created_at.desc())
        .limit(limit)
        .offset(offset)
    )
    return [
        build_manual_intake_response(batch)
        for batch in db.scalars(statement).unique().all()
    ]


@router.get("/{batch_id}", response_model=ManualIntakeBatchRead)
def get_batch(
    batch_id: str,
    db: Session = Depends(get_db),
) -> ManualIntakeBatchRead:
    batch = db.get(ManualIntakeBatch, batch_id)
    if batch is None:
        raise HTTPException(status_code=404, detail="Manual intake batch not found")
    return build_manual_intake_response(batch)
