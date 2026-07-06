from __future__ import annotations

from app.services.acquisition.filtering import ListingFilter
from app.services.acquisition.models import NormalizedListing
from app.services.acquisition.sources.base import BaseSourceAdapter


class DataAcquisitionPipeline:
    """Collector -> RawListing -> Normalizer -> Filter foundation."""

    def __init__(self, adapters: list[BaseSourceAdapter], listing_filter: ListingFilter | None = None) -> None:
        self.adapters = adapters
        self.listing_filter = listing_filter or ListingFilter()

    def run_once(self) -> list[NormalizedListing]:
        normalized: list[NormalizedListing] = []
        for adapter in self.adapters:
            for raw_listing in adapter.collect():
                normalized.append(adapter.normalize(raw_listing))
        return self.listing_filter.filter(normalized)

