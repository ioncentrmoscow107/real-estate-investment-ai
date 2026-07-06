from app.services.acquisition.models import RawListing
from app.services.acquisition.sources.cian import CianAdapter


def test_cian_adapter_normalizes_sample_listing() -> None:
    adapter = CianAdapter()
    raw = RawListing(
        source="cian",
        source_listing_id="cian-1",
        source_url="https://www.cian.ru/sale/commercial/1/",
        raw_payload={
            "id": "cian-1",
            "title": "Продажа street retail",
            "description": "Арендатор ВкусВилл, мощность 50 кВт, возможно увеличение до 100 кВт",
            "address": "Москва, Тверская улица, 10",
            "price_rub": 180_000_000,
            "area_sqm": 200,
            "floor": 1,
            "total_floors": 12,
            "building_year": 2020,
            "property_type": "street_retail",
            "coordinates": {"lat": 55.0, "lng": 37.0},
            "photos": ["https://example.test/photo.jpg"],
        },
    )

    listing = adapter.normalize(raw)

    assert listing.source == "cian"
    assert listing.price_per_sqm == 900000
    assert listing.tenant_name == "ВкусВилл"
    assert listing.has_federal_tenant is True
    assert listing.electric_power_kw == 50
    assert listing.electric_power_increase_to_kw == 100

