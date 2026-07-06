from app.services.acquisition.models import NormalizedListing
from app.services.acquisition.scoring import InvestmentScoringService


def listing(**overrides):
    data = {
        "source": "cian",
        "source_listing_id": "1",
        "source_url": "https://example.test/listing/1",
        "title": "Street retail",
        "description": "Federal tenant",
        "address": "Москва, Тверская улица, 10",
        "price_rub": 180_000_000,
        "area_sqm": 240,
        "price_per_sqm": 750_000,
        "floor": 1,
        "total_floors": 12,
        "building_year": 2020,
        "property_type": "street_retail",
        "tenant_name": "ВкусВилл",
        "tenant_type": "federal",
        "has_federal_tenant": True,
        "electric_power_kw": 120,
        "electric_power_verified": True,
        "repair_condition": "quality_repair",
        "photos": ["https://example.test/photo.jpg"],
        "seller_name": "Agency",
    }
    data.update(overrides)
    return NormalizedListing(**data)


def test_strong_object_with_federal_tenant_and_high_power() -> None:
    analysis = InvestmentScoringService().analyze(listing())

    assert analysis.recommendation == "BUY"
    assert analysis.investment_score >= 75
    assert analysis.liquidity_score >= 80
    assert analysis.risk_score <= 45
    assert "есть федеральный арендатор" in analysis.advantages
    assert "высокая электрическая мощность" in analysis.advantages


def test_vacant_object_without_repair_is_watch_or_avoid() -> None:
    analysis = InvestmentScoringService().analyze(
        listing(
            tenant_name=None,
            tenant_type=None,
            has_federal_tenant=False,
            repair_condition="no_repair",
            electric_power_kw=45,
            electric_power_verified=True,
        )
    )

    assert analysis.recommendation in {"WATCH", "AVOID"}
    assert analysis.risk_score >= 50
    assert "требуются вложения в ремонт" in analysis.disadvantages
    assert "нет подтвержденного федерального арендатора" in analysis.risks


def test_missing_electric_power_penalizes_quality_and_risk() -> None:
    analysis = InvestmentScoringService().analyze(listing(electric_power_kw=None, electric_power_verified=False))

    assert analysis.data_quality_score < 100
    assert analysis.risk_score >= 30
    assert "не указана электрическая мощность" in analysis.disadvantages
    assert "непонятно, хватит ли мощности для арендатора" in analysis.risks


def test_suspiciously_low_price_increases_fake_score() -> None:
    analysis = InvestmentScoringService().analyze(
        listing(price_rub=40_000_000, area_sqm=240, price_per_sqm=166_666)
    )

    assert analysis.fake_score >= 30
    assert analysis.recommendation != "BUY"
    assert "подозрительно низкая цена за м2 требует проверки" in analysis.risks


def test_object_outside_ideal_criteria_is_avoid() -> None:
    analysis = InvestmentScoringService().analyze(
        listing(
            price_rub=450_000_000,
            floor=2,
            building_year=2014,
            has_federal_tenant=False,
            tenant_name=None,
            tenant_type=None,
            electric_power_kw=30,
            repair_condition="needs_repair",
            raw_payload={"exposure_days": 140},
        )
    )

    assert analysis.recommendation == "AVOID"
    assert analysis.risk_score >= 70
    assert "объект не на первом этаже" in analysis.disadvantages
    assert "старое здание может потребовать дополнительных проверок" in analysis.risks

