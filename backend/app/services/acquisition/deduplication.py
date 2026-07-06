from __future__ import annotations

from dataclasses import dataclass

from app.services.acquisition.models import NormalizedListing


@dataclass(frozen=True, slots=True)
class MatchResult:
    listing: NormalizedListing
    matched_listing: NormalizedListing | None
    confidence: int
    reason: str


class BasicDeduplicationService:
    """Conservative deterministic matcher for early acquisition pipeline."""

    def find_match(
        self,
        candidate: NormalizedListing,
        existing: list[NormalizedListing],
    ) -> MatchResult:
        for listing in existing:
            if self._same_source_listing(candidate, listing):
                return MatchResult(candidate, listing, 100, "same_source_listing_id")

        best: tuple[int, NormalizedListing | None, str] = (0, None, "no_match")
        for listing in existing:
            confidence, reason = self._score(candidate, listing)
            if confidence > best[0]:
                best = (confidence, listing, reason)

        return MatchResult(candidate, best[1], best[0], best[2])

    def _same_source_listing(self, left: NormalizedListing, right: NormalizedListing) -> bool:
        return (
            left.source == right.source
            and left.source_listing_id is not None
            and left.source_listing_id == right.source_listing_id
        )

    def _score(self, left: NormalizedListing, right: NormalizedListing) -> tuple[int, str]:
        score = 0
        reasons: list[str] = []

        if left.normalized_address_key() and left.normalized_address_key() == right.normalized_address_key():
            score += 40
            reasons.append("same_address")

        if left.area_sqm and right.area_sqm:
            diff = abs(left.area_sqm - right.area_sqm) / max(left.area_sqm, right.area_sqm)
            if diff <= 0.03:
                score += 20
                reasons.append("similar_area")

        if left.floor is not None and left.floor == right.floor:
            score += 10
            reasons.append("same_floor")

        if left.price_rub and right.price_rub:
            diff = abs(left.price_rub - right.price_rub) / max(left.price_rub, right.price_rub)
            if diff <= 0.05:
                score += 10
                reasons.append("similar_price")

        if left.tenant_name and left.tenant_name == right.tenant_name:
            score += 10
            reasons.append("same_tenant")

        if left.seller_phone_hash and left.seller_phone_hash == right.seller_phone_hash:
            score += 10
            reasons.append("same_seller_phone")

        return min(score, 100), ",".join(reasons) or "no_match"

