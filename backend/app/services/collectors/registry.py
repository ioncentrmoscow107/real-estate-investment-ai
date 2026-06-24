from app.services.collectors.base import ListingCollector, ScrapingNotImplementedCollector
from app.services.collectors.filters import matches_investment_filters


class CollectorRegistry:
    def __init__(self) -> None:
        self._collectors: list[ListingCollector] = [
            ScrapingNotImplementedCollector("cian"),
            ScrapingNotImplementedCollector("avito"),
            ScrapingNotImplementedCollector("domclick"),
            ScrapingNotImplementedCollector("yandex_realty"),
        ]

    def source_names(self) -> list[str]:
        return [collector.source_name for collector in self._collectors]

    def collect_all(self) -> dict[str, object]:
        total = 0
        accepted = 0
        by_source: dict[str, dict[str, int]] = {}

        for collector in self._collectors:
            listings = collector.collect()
            filtered = [listing for listing in listings if matches_investment_filters(listing)]
            total += len(listings)
            accepted += len(filtered)
            by_source[collector.source_name] = {
                "collected": len(listings),
                "accepted": len(filtered),
            }

        return {
            "total_collected": total,
            "total_accepted": accepted,
            "sources": by_source,
        }


collector_registry = CollectorRegistry()

