from openai import OpenAI

from app.core.config import settings
from app.schemas.listing import ListingRead


class ListingAnalyzer:
    def __init__(self) -> None:
        self._client = OpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None

    def is_enabled(self) -> bool:
        return self._client is not None

    def build_prompt(self, listing: ListingRead) -> str:
        return (
            "Analyze this commercial real estate listing for investment quality.\n"
            f"Title: {listing.title}\n"
            f"Price RUB: {listing.price_rub}\n"
            f"Floor: {listing.floor}\n"
            f"Building year: {listing.building_year}\n"
            f"Property type: {listing.property_type}\n"
            f"Tenant: {listing.tenant or 'unknown'}\n"
        )

    def analyze(self, listing: ListingRead) -> str:
        if self._client is None:
            return "AI analysis is disabled because OPENAI_API_KEY is not configured."

        response = self._client.responses.create(
            model=settings.openai_model,
            input=self.build_prompt(listing),
        )
        return response.output_text


listing_analyzer = ListingAnalyzer()

