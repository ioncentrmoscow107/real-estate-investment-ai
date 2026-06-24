from app.core.config import settings
from app.services.collectors.base import RawListing


def matches_investment_filters(listing: RawListing) -> bool:
    return (
        settings.min_price_rub <= listing.price_rub <= settings.max_price_rub
        and listing.floor == settings.allowed_floor
        and listing.building_year >= settings.min_building_year
        and listing.property_type in settings.property_types
    )

