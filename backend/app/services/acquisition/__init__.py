from app.services.acquisition.deduplication import BasicDeduplicationService, MatchResult
from app.services.acquisition.filtering import FilterResult, ListingFilter
from app.services.acquisition.models import NormalizedListing, RawListing
from app.services.acquisition.pipeline import DataAcquisitionPipeline
from app.services.acquisition.property_intelligence import (
    PropertyIntelligence,
    PropertyIntelligenceService,
    ScoreExplanation,
)
from app.services.acquisition.scoring import InvestmentAnalysis, InvestmentScoringService
from app.services.acquisition.sources.base import BaseSourceAdapter
from app.services.acquisition.sources.cian import CianAdapter

__all__ = [
    "BaseSourceAdapter",
    "BasicDeduplicationService",
    "CianAdapter",
    "DataAcquisitionPipeline",
    "FilterResult",
    "InvestmentAnalysis",
    "InvestmentScoringService",
    "ListingFilter",
    "MatchResult",
    "NormalizedListing",
    "PropertyIntelligence",
    "PropertyIntelligenceService",
    "RawListing",
    "ScoreExplanation",
]
