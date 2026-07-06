import json
from pathlib import Path
from tempfile import TemporaryDirectory

from app.services.acquisition.models import NormalizedListing
from app.services.acquisition.property_intelligence import PropertyIntelligenceService, SCORE_NAMES


def listing(**overrides):
    data = {
        "source": "cian",
        "source_listing_id": "pi-1",
        "source_url": "https://example.test/listing/pi-1",
        "title": "Street retail with tenant",
        "description": "Federal tenant, high power",
        "address": "Moscow, Tverskaya street, 10",
        "latitude": 55.7558,
        "longitude": 37.6173,
        "price_rub": 180_000_000,
        "area_sqm": 240,
        "price_per_sqm": 750_000,
        "floor": 1,
        "total_floors": 12,
        "building_year": 2021,
        "property_type": "street_retail",
        "tenant_name": "Ozon",
        "tenant_type": "federal",
        "has_federal_tenant": True,
        "electric_power_kw": 120,
        "electric_power_verified": True,
        "electric_power_can_be_increased": False,
        "repair_condition": "quality_repair",
        "photos": ["https://example.test/photo.jpg"],
        "seller_name": "Agency",
    }
    data.update(overrides)
    return NormalizedListing(**data)


def test_every_property_returns_complete_intelligence_object() -> None:
    intelligence = PropertyIntelligenceService().analyze(listing())

    for score_name in SCORE_NAMES:
        value = getattr(intelligence, score_name)
        assert 0 <= value <= 100
        assert score_name in intelligence.explanations
        assert intelligence.explanations[score_name].score == value
        assert intelligence.explanations[score_name].explanations

    assert intelligence.recommendation in {"BUY", "WATCH", "AVOID"}
    assert intelligence.short_summary
    assert intelligence.rules_version == "property_intelligence_v1"
    assert isinstance(intelligence.advantages, list)
    assert isinstance(intelligence.disadvantages, list)
    assert isinstance(intelligence.risks, list)
    assert isinstance(intelligence.missing_information, list)
    assert isinstance(intelligence.due_diligence_checklist, list)


def test_scores_are_deterministic() -> None:
    service = PropertyIntelligenceService()
    first = service.analyze(listing())
    second = service.analyze(listing())

    assert first == second


def test_strong_property_scores_buy_with_tenant_building_and_location_explanations() -> None:
    intelligence = PropertyIntelligenceService().analyze(listing())

    assert intelligence.recommendation == "BUY"
    assert intelligence.investment_score >= 75
    assert intelligence.tenant_score >= 80
    assert intelligence.building_score >= 70
    assert intelligence.location_score >= 55
    assert "Federal tenant improves income reliability." in intelligence.advantages
    assert intelligence.explanations["tenant_score"].applied_rules
    assert intelligence.explanations["building_score"].applied_rules
    assert intelligence.explanations["location_score"].applied_rules


def test_weak_property_generates_disadvantages_risks_missing_info_and_due_diligence() -> None:
    intelligence = PropertyIntelligenceService().analyze(
        listing(
            address=None,
            latitude=None,
            longitude=None,
            price_rub=450_000_000,
            price_per_sqm=180_000,
            floor=2,
            building_year=2014,
            tenant_name=None,
            tenant_type=None,
            has_federal_tenant=False,
            electric_power_kw=20,
            electric_power_can_be_increased=False,
            repair_condition="none",
            photos=[],
            seller_name=None,
            raw_payload={"exposure_days": 130},
        )
    )

    assert intelligence.recommendation == "AVOID"
    assert intelligence.risk_score >= 70
    assert intelligence.fake_score >= 50
    assert "address" in intelligence.missing_information
    assert "photos" in intelligence.missing_information
    assert "Property is not on the first floor." in intelligence.disadvantages
    assert "Suspiciously low price per sqm requires verification." in intelligence.risks
    assert "Check ownership, encumbrances, listing authenticity, and actual sale price." in intelligence.due_diligence_checklist


def test_rules_are_loaded_from_editable_file() -> None:
    custom_rules = {
        "version": "test_rules",
        "score_defaults": {score_name: 50 for score_name in SCORE_NAMES},
        "recommendation_thresholds": {
            "buy_min_investment_score": 75,
            "buy_max_risk_score": 45,
            "buy_max_fake_score": 35,
            "buy_min_data_quality_score": 70,
            "avoid_max_investment_score": 49,
            "avoid_min_risk_score": 70,
            "avoid_min_fake_score": 60,
            "avoid_max_data_quality_score": 44,
        },
        "rules": [
            {
                "id": "custom_federal_tenant_rule",
                "conditions": [{"field": "has_federal_tenant", "operator": "eq", "value": True}],
                "score_adjustments": {"tenant_score": 25},
                "advantages": ["Custom tenant rule fired."],
                "explanations": {"tenant_score": "Custom editable rule adjusted tenant score."},
            }
        ],
    }
    with TemporaryDirectory() as temp_dir:
        rules_path = Path(temp_dir) / "rules.json"
        rules_path.write_text(json.dumps(custom_rules), encoding="utf-8")
        intelligence = PropertyIntelligenceService(rules_path=rules_path).analyze(listing())

    assert intelligence.rules_version == "test_rules"
    assert intelligence.tenant_score == 75
    assert "Custom tenant rule fired." in intelligence.advantages
    assert "custom_federal_tenant_rule" in intelligence.explanations["tenant_score"].applied_rules
