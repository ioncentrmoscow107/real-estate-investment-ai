from __future__ import annotations

from dataclasses import dataclass

from app.services.acquisition.models import NormalizedListing


ALLOWED_PROPERTY_TYPES = {
    "street_retail",
    "retail_premises",
    "free_use_commercial_premises",
    "free_use",
    "federal_tenant",
}


@dataclass(frozen=True, slots=True)
class FilterResult:
    accepted: bool
    reasons: tuple[str, ...] = ()


class ListingFilter:
    min_price_rub = 100_000_000
    max_price_rub = 400_000_000
    min_building_year = 2016

    def evaluate(self, listing: NormalizedListing) -> FilterResult:
        reasons: list[str] = []

        if listing.price_rub is None:
            reasons.append("missing_price")
        elif listing.price_rub < self.min_price_rub:
            reasons.append("price_below_min")
        elif listing.price_rub > self.max_price_rub:
            reasons.append("price_above_max")

        if listing.floor != 1:
            reasons.append("not_first_floor")

        if listing.building_year is None:
            reasons.append("missing_building_year")
        elif listing.building_year < self.min_building_year:
            reasons.append("building_too_old")

        if not self._is_allowed_property_type(listing):
            reasons.append("unsupported_property_type")

        return FilterResult(accepted=not reasons, reasons=tuple(reasons))

    def filter(self, listings: list[NormalizedListing]) -> list[NormalizedListing]:
        return [listing for listing in listings if self.evaluate(listing).accepted]

    def _is_allowed_property_type(self, listing: NormalizedListing) -> bool:
        if listing.has_federal_tenant:
            return True
        return (listing.property_type or "") in ALLOWED_PROPERTY_TYPES

