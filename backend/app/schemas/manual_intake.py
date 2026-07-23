from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator


class ManualIntakeStatus(str, Enum):
    draft = "draft"
    queued = "queued"
    processing = "processing"
    analyzed = "analyzed"
    failed = "failed"


class ManualIntakeBatchCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=2000)
    urls: list[HttpUrl] = Field(min_length=1, max_length=100)
    linked_search_profile_id: str | None = Field(default=None, max_length=100)

    @field_validator("name")
    @classmethod
    def require_nonblank_name(cls, name: str) -> str:
        name = name.strip()
        if not name:
            raise ValueError("Batch name must not be blank")
        return name

    @field_validator("urls")
    @classmethod
    def require_unique_urls(cls, urls: list[HttpUrl]) -> list[HttpUrl]:
        normalized = [str(url) for url in urls]
        if len(normalized) != len(set(normalized)):
            raise ValueError("Duplicate URLs are not allowed in one intake batch")
        return urls


class ManualListingUrlRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    url: str
    source_detected: str
    status: ManualIntakeStatus
    error_message: str | None
    created_at: datetime
    updated_at: datetime


class ManualIntakeBatchRead(BaseModel):
    id: str
    name: str
    description: str | None
    status: ManualIntakeStatus
    source: str
    linked_search_profile_id: str | None
    created_at: datetime
    updated_at: datetime
    urls: list[ManualListingUrlRead]
    total_urls: int
    processed_count: int
    failed_count: int
    analyzed_count: int
