from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(slots=True)
class RawListing:
    source: str
    source_listing_id: str | None
    source_url: str
    raw_payload: dict[str, Any]
    collected_at: datetime = field(default_factory=utc_now)


@dataclass(slots=True)
class NormalizedListing:
    source: str
    source_listing_id: str | None
    source_url: str
    title: str | None = None
    description: str | None = None
    address: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    price_rub: int | None = None
    area_sqm: float | None = None
    price_per_sqm: float | None = None
    floor: int | None = None
    total_floors: int | None = None
    building_year: int | None = None
    property_type: str | None = None
    tenant_name: str | None = None
    tenant_type: str | None = None
    has_federal_tenant: bool = False
    electric_power_kw: float | None = None
    electric_power_verified: bool = False
    electric_power_can_be_increased: bool = False
    electric_power_increase_to_kw: float | None = None
    electric_power_source: str | None = None
    repair_condition: str | None = None
    vacant_property_fitout_comment: str | None = None
    photos: list[str] = field(default_factory=list)
    seller_name: str | None = None
    seller_phone_hash: str | None = None
    published_at: datetime | None = None
    first_seen_at: datetime = field(default_factory=utc_now)
    last_seen_at: datetime = field(default_factory=utc_now)
    raw_payload: dict[str, Any] = field(default_factory=dict)

    def normalized_address_key(self) -> str:
        return " ".join((self.address or "").lower().replace(",", " ").split())

