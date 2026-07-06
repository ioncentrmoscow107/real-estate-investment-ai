from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timezone

from app.services.acquisition.models import NormalizedListing
from app.services.acquisition.property_intelligence import PropertyIntelligenceService


RUSSIAN_SAMPLE_ANALYSIS = {
    "sample-buy-1": {
        "advantages": [
            "Федеральный арендатор снижает риск вакантности",
            "Дом введен после 2016 года",
            "Первый этаж и отдельный вход",
            "Электрическая мощность 120 кВт",
        ],
        "disadvantages": [
            "Нет подтверждения по индексации арендной ставки",
            "Нужно проверить структуру коммунальных платежей",
        ],
        "risks": [
            "Нет данных о сроке договора аренды",
            "Требуется проверка окупаемости",
        ],
        "missing_information": [
            "Срок договора аренды",
            "Индексация арендной ставки",
            "Фактическая коммунальная нагрузка",
        ],
        "due_diligence_checklist": [
            "Проверить выписку ЕГРН",
            "Проверить срок и условия договора аренды",
            "Проверить индексацию арендной ставки",
            "Подтвердить электрическую мощность документально",
            "Проверить фактический трафик",
        ],
        "short_summary": (
            "Сильный объект для покупки: новый дом, первый этаж, федеральный арендатор "
            "и высокая электрическая мощность. Перед сделкой нужно подтвердить договор аренды, "
            "индексацию и технические условия."
        ),
    },
    "sample-watch-1": {
        "advantages": [
            "Первый этаж в новом жилом массиве",
            "Возможность увеличения мощности до 120 кВт",
            "Цена за м² выглядит умеренной для локации",
        ],
        "disadvantages": [
            "Помещение без подтвержденного арендатора",
            "Состояние shell&core требует вложений",
            "Не подтверждена итоговая стоимость увеличения мощности",
        ],
        "risks": [
            "Не подтверждена электрическая мощность после увеличения",
            "Требуется проверка окупаемости",
            "Возможны дополнительные затраты на ремонт",
        ],
        "missing_information": [
            "Коммерческие условия потенциальной аренды",
            "Смета ремонта",
            "Документы по увеличению мощности",
        ],
        "due_diligence_checklist": [
            "Проверить назначение помещения",
            "Проверить возможность увеличения мощности",
            "Проверить состояние ремонта",
            "Проверить фактический трафик",
            "Проверить налоговую и коммунальную нагрузку",
        ],
        "short_summary": (
            "Интересный объект для дополнительного изучения: параметры подходят под MVP, "
            "но нет арендатора и нужны вложения в отделку. Решение зависит от подтверждения "
            "спроса, ремонта и мощности."
        ),
    },
    "sample-buy-2": {
        "advantages": [
            "Федеральный арендатор снижает риск вакантности",
            "Первый этаж и витринные окна",
            "Электрическая мощность 95 кВт",
            "Цена находится в целевом диапазоне",
        ],
        "disadvantages": [
            "Нужно проверить фактический покупательский трафик",
            "Нет подтверждения по арендным каникулам",
        ],
        "risks": [
            "Нет подтверждения по индексации аренды",
            "Возможна зависимость дохода от одного арендатора",
        ],
        "missing_information": [
            "Индексация аренды",
            "Срок обязательной части договора",
            "История арендных платежей",
        ],
        "due_diligence_checklist": [
            "Проверить выписку ЕГРН",
            "Проверить договор аренды и обеспечительный платеж",
            "Проверить индексацию арендной ставки",
            "Подтвердить электрическую мощность документально",
            "Проверить налоговую и коммунальную нагрузку",
        ],
        "short_summary": (
            "Объект выглядит пригодным для покупки после проверки аренды: первый этаж, "
            "федеральный арендатор и достаточная мощность поддерживают ликвидность."
        ),
    },
    "sample-avoid-1": {
        "advantages": [
            "Цена за м² ниже сопоставимых объектов",
        ],
        "disadvantages": [
            "Помещение без арендатора и требует ремонта",
            "Не первый этаж",
            "Здание старше целевого критерия",
            "Недостаточно данных для оценки ликвидности",
        ],
        "risks": [
            "Не подтверждена электрическая мощность",
            "Возможна завышенная итоговая стоимость с учетом ремонта",
            "Нет точного адреса и фотографий",
            "Долгая экспозиция может указывать на слабый спрос",
        ],
        "missing_information": [
            "Точный адрес",
            "Фотографии помещения",
            "Подтвержденная электрическая мощность",
            "Данные о продавце",
            "Текущий арендатор или план сдачи",
        ],
        "due_diligence_checklist": [
            "Запросить точный адрес и документы собственности",
            "Подтвердить электрическую мощность документально",
            "Проверить состояние ремонта",
            "Проверить фактический трафик",
            "Проверить налоговую и коммунальную нагрузку",
        ],
        "short_summary": (
            "Покупку не рекомендую: слишком много критичных пробелов в данных, объект не "
            "соответствует нескольким MVP-критериям и требует существенной проверки до переговоров."
        ),
    },
}


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
    average_risk = 0 if total == 0 else round(
        sum(item["risk_score"] for item in properties) / total,
        1,
    )

    return {
        "summary": {
            "total_properties": total,
            "average_investment_score": average_score,
            "average_risk_score": average_risk,
            "recommendations": recommendations,
        },
        "properties": properties,
    }


def _build_dashboard_property(listing: NormalizedListing) -> dict:
    intelligence = PropertyIntelligenceService().analyze(listing)
    russian_analysis = RUSSIAN_SAMPLE_ANALYSIS.get(listing.source_listing_id or "", {})
    return {
        "id": listing.source_listing_id,
        "source": listing.source,
        "source_url": listing.source_url,
        "title": listing.title,
        "address": listing.address,
        "price_rub": listing.price_rub,
        "area_sqm": listing.area_sqm,
        "price_per_sqm": listing.price_per_sqm,
        "electric_power_kw": listing.electric_power_kw,
        "electric_power_increase_to_kw": listing.electric_power_increase_to_kw,
        "repair_condition": listing.repair_condition,
        "has_federal_tenant": listing.has_federal_tenant,
        "last_updated": listing.last_seen_at.isoformat(),
        "investment_score": intelligence.investment_score,
        "liquidity_score": intelligence.liquidity_score,
        "tenant_score": intelligence.tenant_score,
        "building_score": intelligence.building_score,
        "location_score": intelligence.location_score,
        "risk_score": intelligence.risk_score,
        "fake_score": intelligence.fake_score,
        "data_quality_score": intelligence.data_quality_score,
        "recommendation": intelligence.recommendation,
        "advantages": russian_analysis.get("advantages", intelligence.advantages),
        "disadvantages": russian_analysis.get("disadvantages", intelligence.disadvantages),
        "risks": russian_analysis.get("risks", intelligence.risks),
        "missing_information": russian_analysis.get("missing_information", intelligence.missing_information),
        "due_diligence_checklist": russian_analysis.get(
            "due_diligence_checklist",
            intelligence.due_diligence_checklist,
        ),
        "short_summary": russian_analysis.get("short_summary", intelligence.short_summary),
        "explanations": {
            score_name: asdict(explanation)
            for score_name, explanation in intelligence.explanations.items()
        },
    }


def _sample_listings() -> list[NormalizedListing]:
    sample_updated_at = datetime(2026, 7, 6, 9, 30, tzinfo=timezone.utc)
    return [
        NormalizedListing(
            source="cian",
            source_listing_id="sample-buy-1",
            source_url="https://example.test/cian/sample-buy-1",
            title="Стрит-ритейл с Ozon в новом ЖК",
            address="Москва, Хорошевский район, ул. Авиаконструктора Микояна, 12",
            latitude=55.7904,
            longitude=37.5296,
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
            seller_name="Prime Retail Moscow",
            last_seen_at=sample_updated_at,
        ),
        NormalizedListing(
            source="cian",
            source_listing_id="sample-watch-1",
            source_url="https://example.test/cian/sample-watch-1",
            title="ПСН у метро в развивающемся жилом кластере",
            address="Москва, Ленинский проспект, 45",
            latitude=55.7060,
            longitude=37.5840,
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
            electric_power_increase_to_kw=120,
            repair_condition="shell_core",
            photos=["https://example.test/photo-2.jpg"],
            seller_name="City Retail Broker",
            raw_payload={"exposure_days": 54},
            last_seen_at=sample_updated_at,
        ),
        NormalizedListing(
            source="cian",
            source_listing_id="sample-buy-2",
            source_url="https://example.test/cian/sample-buy-2",
            title="Торговое помещение с ВкусВилл на первом этаже",
            address="Москва, район Фили-Давыдково, ул. Минская, 2Ж",
            latitude=55.7256,
            longitude=37.4987,
            price_rub=235_000_000,
            area_sqm=310,
            price_per_sqm=758_065,
            floor=1,
            total_floors=24,
            building_year=2020,
            property_type="retail_premises",
            tenant_name="ВкусВилл",
            tenant_type="federal",
            has_federal_tenant=True,
            electric_power_kw=95,
            electric_power_verified=True,
            repair_condition="quality_repair",
            photos=["https://example.test/photo-3.jpg"],
            seller_name="Инвест Ритейл",
            raw_payload={"exposure_days": 21},
            last_seen_at=sample_updated_at,
        ),
        NormalizedListing(
            source="cian",
            source_listing_id="sample-avoid-1",
            source_url="https://example.test/cian/sample-avoid-1",
            title="Коммерческое помещение с неполными данными",
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
            last_seen_at=sample_updated_at,
        ),
    ]
