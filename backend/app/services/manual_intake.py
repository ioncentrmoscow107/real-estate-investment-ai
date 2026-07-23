from urllib.parse import urlsplit
from uuid import uuid4

from sqlalchemy.orm import Session

from app.models.manual_intake import ManualIntakeBatch, ManualListingUrl
from app.schemas.manual_intake import ManualIntakeBatchCreate, ManualIntakeBatchRead

SUPPORTED_SOURCE_DOMAINS = {
    "cian": ("cian.ru",),
    "avito": ("avito.ru",),
    "domclick": ("domclick.ru",),
    "yandex_realty": ("realty.yandex.ru",),
}


def detect_listing_source(url: str) -> str | None:
    hostname = (urlsplit(url).hostname or "").lower().rstrip(".")
    for source, domains in SUPPORTED_SOURCE_DOMAINS.items():
        if any(hostname == domain or hostname.endswith(f".{domain}") for domain in domains):
            return source
    return None


def create_manual_intake_batch(
    db: Session,
    payload: ManualIntakeBatchCreate,
) -> ManualIntakeBatch:
    batch = ManualIntakeBatch(
        id=str(uuid4()),
        name=payload.name.strip(),
        description=payload.description,
        status="queued",
        source="manual",
        linked_search_profile_id=payload.linked_search_profile_id,
    )

    queued_count = 0
    for submitted_url in payload.urls:
        url = str(submitted_url)
        source = detect_listing_source(url)
        if source is None:
            status = "failed"
            error_message = "Unsupported listing source"
        else:
            status = "queued"
            error_message = None
            queued_count += 1

        batch.urls.append(
            ManualListingUrl(
                id=str(uuid4()),
                url=url,
                source_detected=source or "unknown",
                status=status,
                error_message=error_message,
            )
        )

    if queued_count == 0:
        batch.status = "failed"

    db.add(batch)
    db.commit()
    db.refresh(batch)
    return batch


def build_manual_intake_response(batch: ManualIntakeBatch) -> ManualIntakeBatchRead:
    failed_count = sum(url.status == "failed" for url in batch.urls)
    analyzed_count = sum(url.status == "analyzed" for url in batch.urls)
    processed_count = sum(url.status in {"analyzed", "failed"} for url in batch.urls)

    return ManualIntakeBatchRead(
        id=batch.id,
        name=batch.name,
        description=batch.description,
        status=batch.status,
        source=batch.source,
        linked_search_profile_id=batch.linked_search_profile_id,
        created_at=batch.created_at,
        updated_at=batch.updated_at,
        urls=batch.urls,
        total_urls=len(batch.urls),
        processed_count=processed_count,
        failed_count=failed_count,
        analyzed_count=analyzed_count,
    )
