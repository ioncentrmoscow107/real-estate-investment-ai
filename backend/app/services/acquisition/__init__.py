from app.services.acquisition.deduplication import BasicDeduplicationService, MatchResult
from app.services.acquisition.filtering import FilterResult, ListingFilter
from app.services.acquisition.models import NormalizedListing, RawListing
from app.services.acquisition.pipeline import DataAcquisitionPipeline
from app.services.acquisition.sources.base import BaseSourceAdapter
from app.services.acquisition.sources.cian import CianAdapter

__all__ = [
    "BaseSourceAdapter",
    "BasicDeduplicationService",
    "CianAdapter",
    "DataAcquisitionPipeline",
    "FilterResult",
    "ListingFilter",
    "MatchResult",
    "NormalizedListing",
    "RawListing",
]

