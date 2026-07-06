from __future__ import annotations

from dataclasses import asdict

from app.services.acquisition.models import NormalizedListing
from app.services.acquisition.property_intelligence import PropertyIntelligenceService


def get_sample_dashboard_properties() -> dict:
    properties = [_build_dashboard_property(listing) for listing in _sample_listings()]
    recommendations = {"BUY": 0, "WATCH": 0, "AVOID": 0}
    for item in properties:
        recommendations[item["recommendation"]] += 1

    total = len(properties)
    average_score = 0 if total == 0 else round(
        sum(item["investment_score"] for item in properties) / total,
        1,
    )

    return {
        "summary": {
            "total_properties": total,
            "average_investment_score": average_score,
            "recommendations": recommendations,
        },
        "properties": properties,
    }


def _build_dashboard_property(listing: NormalizedListing) -> dict:
    intelligence = PropertyIntelligenceService().analyze(listing)
    return {
        "id": listing.source_listing_id,
        "source": listing.source,
        "source_url": listing.source_url,
        "title": listing.title,
        "address": listing.address,
        "price_rub": listing.price_rub,
        "area_sqm": listing.area_sqm,
        "price_per_sqm": listing.price_per_sqm,
        "investment_score": intelligence.investment_score,
        "liquidity_score": intelligence.liquidity_score,
        "risk_score": intelligence.risk_score,
        "fake_score": intelligence.fake_score,
        "data_quality_score": intelligence.data_quality_score,
        "recommendation": intelligence.recommendation,
        "advantages": intelligence.advantages,
        "disadvantages": intelligence.disadvantages,
        "risks": intelligence.risks,
        "missing_information": intelligence.missing_information,
        "due_diligence_checklist": intelligence.due_diligence_checklist,
        "short_summary": intelligence.short_summary,
        "explanations": {
            score_name: asdict(explanation)
            for score_name, explanation in intelligence.explanations.items()
        },
    }


def _sample_listings() -> list[NormalizedListing]:
    return [
        NormalizedListing(
            source="cian",
            source_listing_id="sample-buy-1",
            source_url="https://example.test/cian/sample-buy-1",
            title="Street retail with federal tenant",
            address="Moscow, Tverskaya street, 10",
            latitude=55.7558,
            longitude=37.6173,
            price_rub=180_000_000,
            area_sqm=240,
            price_per_sqm=750_000,
            floor=1,
            total_floors=12,
            building_year=2021,
            property_type="street_retail",
            tenant_name="Ozon",
            tenant_type="federal",
            has_federal_tenant=True,
            electric_power_kw=120,
            electric_power_verified=True,
            repair_condition="quality_repair",
            photos=["https://example.test/photo-1.jpg"],
            seller_name="Prime Retail Agency",
        ),
        NormalizedListing(
            source="cian",
            source_listing_id="sample-watch-1",
            source_url="https://example.test/cian/sample-watch-1",
            title="Vacant retail premises near metro",
            address="Moscow, Leninsky prospect, 45",
            latitude=55.706,
            longitude=37.584,
            price_rub=145_000_000,
            area_sqm=190,
            price_per_sqm=763_158,
            floor=1,
            total_floors=18,
            building_year=2018,
            property_type="retail_premises",
            electric_power_kw=45,
            electric_power_verified=True,
            electric_power_can_be_increased=True,
            repair_condition="shell_core",
            photos=["https://example.test/photo-2.jpg"],
            seller_name="City Broker",
            raw_payload={"exposure_days": 54},
        ),
        NormalizedListing(
            source="cian",
            source_listing_id="sample-avoid-1",
            source_url="https://example.test/cian/sample-avoid-1",
            title="Commercial premises with unclear data",
            address=None,
            price_rub=420_000_000,
            area_sqm=980,
            price_per_sqm=180_000,
            floor=2,
            building_year=2014,
            property_type="free_use",
            electric_power_kw=20,
            repair_condition="none",
            photos=[],
            raw_payload={"exposure_days": 130},
        ),
    ]

