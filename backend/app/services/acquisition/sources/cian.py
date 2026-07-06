from __future__ import annotations

from typing import Any

from app.services.acquisition.extraction import (
    detect_tenant,
    extract_electric_power,
    extract_repair_condition,
)
from app.services.acquisition.models import NormalizedListing, RawListing
from app.services.acquisition.sources.base import BaseSourceAdapter


class CianAdapter(BaseSourceAdapter):
    """Safe CIAN adapter stub.

    This class intentionally does not implement production scraping, anti-bot
    bypassing, login bypassing, or captcha bypassing. The future production
    implementation must use public pages/import/API-compatible access where
    allowed by CIAN terms and robots.txt.
    """

    source_name = "cian"

    def collect(self) -> list[RawListing]:
        # TODO: Add compliant CIAN collection.
        # Allowed direction:
        # - public pages/import/API-compatible access where permitted;
        # - robots.txt and terms-of-service checks before collection;
        # - rate limits and clear user agent identification if applicable.
        #
        # Explicitly out of scope:
        # - anti-bot bypassing;
        # - captcha bypassing;
        # - login/session bypassing.
        return []

    def normalize(self, raw_listing: RawListing) -> NormalizedListing:
        payload = raw_listing.raw_payload
        description = _text(payload.get("description"))
        title = _text(payload.get("title"))
        text = f"{title or ''}\n{description or ''}"

        power = extract_electric_power(text)
        tenant = detect_tenant(text)

        price_rub = _int_or_none(payload.get("price_rub") or payload.get("price"))
        area_sqm = _float_or_none(payload.get("area_sqm") or payload.get("area"))
        price_per_sqm = round(price_rub / area_sqm, 2) if price_rub and area_sqm else None
        coordinates = payload.get("coordinates") or {}

        return NormalizedListing(
            source=self.source_name,
            source_listing_id=_text(payload.get("id") or raw_listing.source_listing_id),
            source_url=raw_listing.source_url,
            title=title,
            description=description,
            address=_text(payload.get("address")),
            latitude=_float_or_none(coordinates.get("lat") or payload.get("latitude")),
            longitude=_float_or_none(coordinates.get("lng") or payload.get("longitude")),
            price_rub=price_rub,
            area_sqm=area_sqm,
            price_per_sqm=price_per_sqm,
            floor=_int_or_none(payload.get("floor")),
            total_floors=_int_or_none(payload.get("total_floors")),
            building_year=_int_or_none(payload.get("building_year")),
            property_type=_text(payload.get("property_type")),
            tenant_name=tenant.tenant_name,
            tenant_type=tenant.tenant_type,
            has_federal_tenant=tenant.has_federal_tenant,
            electric_power_kw=power.power_kw,
            electric_power_verified=power.verified,
            electric_power_can_be_increased=power.can_be_increased,
            electric_power_increase_to_kw=power.increase_to_kw,
            electric_power_source=power.source_text,
            repair_condition=extract_repair_condition(text),
            vacant_property_fitout_comment=_text(payload.get("fitout_comment")),
            photos=[str(photo) for photo in payload.get("photos", [])],
            seller_name=_text(payload.get("seller_name")),
            seller_phone_hash=_text(payload.get("seller_phone_hash")),
            published_at=payload.get("published_at"),
            raw_payload=payload,
        )


def _text(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _int_or_none(value: Any) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(float(str(value).replace(" ", "").replace(",", ".")))
    except (TypeError, ValueError):
        return None


def _float_or_none(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(str(value).replace(" ", "").replace(",", "."))
    except (TypeError, ValueError):
        return None

