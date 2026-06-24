from dataclasses import dataclass
from decimal import Decimal
from typing import Protocol


@dataclass(frozen=True)
class RawListing:
    source: str
    external_id: str
    title: str
    url: str
    price_rub: Decimal
    floor: int
    building_year: int
    property_type: str
    address: str | None = None
    area_sqm: Decimal | None = None
    tenant: str | None = None


class ListingCollector(Protocol):
    source_name: str

    def collect(self) -> list[RawListing]:
        """Collect raw listings from the source."""


class ScrapingNotImplementedCollector:
    def __init__(self, source_name: str) -> None:
        self.source_name = source_name

    def collect(self) -> list[RawListing]:
        return []

