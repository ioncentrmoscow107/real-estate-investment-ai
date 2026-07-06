from __future__ import annotations

from abc import ABC, abstractmethod

from app.services.acquisition.models import NormalizedListing, RawListing


class BaseSourceAdapter(ABC):
    source_name: str

    @abstractmethod
    def collect(self) -> list[RawListing]:
        """Collect raw listings from a public/API-compatible source."""

    @abstractmethod
    def normalize(self, raw_listing: RawListing) -> NormalizedListing:
        """Convert a source-specific payload into the unified listing schema."""

