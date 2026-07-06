from app.services.acquisition.filtering import ListingFilter
from app.services.acquisition.models import NormalizedListing


def listing(**overrides):
    data = {
        "source": "cian",
        "source_listing_id": "1",
        "source_url": "https://example.test/listing/1",
        "price_rub": 150_000_000,
        "area_sqm": 180,
        "floor": 1,
        "building_year": 2019,
        "property_type": "street_retail",
    }
    data.update(overrides)
    return NormalizedListing(**data)


def test_accepts_matching_listing() -> None:
    result = ListingFilter().evaluate(listing())
    assert result.accepted is True
    assert result.reasons == ()


def test_excludes_price_outside_range() -> None:
    listing_filter = ListingFilter()
    assert "price_below_min" in listing_filter.evaluate(listing(price_rub=99_999_999)).reasons
    assert "price_above_max" in listing_filter.evaluate(listing(price_rub=400_000_001)).reasons


def test_excludes_non_first_floor() -> None:
    result = ListingFilter().evaluate(listing(floor=2))
    assert result.accepted is False
    assert "not_first_floor" in result.reasons


def test_excludes_old_building() -> None:
    result = ListingFilter().evaluate(listing(building_year=2015))
    assert result.accepted is False
    assert "building_too_old" in result.reasons


def test_accepts_federal_tenant_even_when_type_is_unknown() -> None:
    result = ListingFilter().evaluate(
        listing(property_type="unknown", has_federal_tenant=True, tenant_name="Ozon", tenant_type="federal")
    )
    assert result.accepted is True

