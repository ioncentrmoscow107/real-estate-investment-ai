from decimal import Decimal

from app.services.collectors.base import RawListing
from app.services.collectors.filters import matches_investment_filters


def test_matches_required_investment_filters() -> None:
    listing = RawListing(
        source="cian",
        external_id="1",
        title="Retail unit",
        url="https://example.com/listing/1",
        price_rub=Decimal("150000000"),
        floor=1,
        building_year=2020,
        property_type="retail",
    )

    assert matches_investment_filters(listing) is True


def test_rejects_non_first_floor() -> None:
    listing = RawListing(
        source="avito",
        external_id="2",
        title="Second floor retail",
        url="https://example.com/listing/2",
        price_rub=Decimal("150000000"),
        floor=2,
        building_year=2020,
        property_type="retail",
    )

    assert matches_investment_filters(listing) is False

