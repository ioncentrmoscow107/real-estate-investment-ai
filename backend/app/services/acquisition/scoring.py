from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone

from app.services.acquisition.models import NormalizedListing


@dataclass(frozen=True, slots=True)
class InvestmentAnalysis:
    investment_score: int
    liquidity_score: int
    risk_score: int
    fake_score: int
    data_quality_score: int
    advantages: list[str] = field(default_factory=list)
    disadvantages: list[str] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)
    recommendation: str = "WATCH"
    short_summary: str = ""


class InvestmentScoringService:
    """Rule-based skeptical investment scoring for normalized listings."""

    min_price_rub = 100_000_000
    max_price_rub = 400_000_000
    min_building_year = 2016
    suspicious_low_price_per_sqm = 250_000
    good_power_kw = 80
    minimum_usable_power_kw = 50
    long_exposure_days = 90

    def analyze(self, listing: NormalizedListing) -> InvestmentAnalysis:
        advantages: list[str] = []
        disadvantages: list[str] = []
        risks: list[str] = []

        data_quality_score = self._data_quality_score(listing, disadvantages, risks)
        liquidity_score = self._liquidity_score(listing, advantages, disadvantages, risks)
        fake_score = self._fake_score(listing, risks)
        risk_score = self._risk_score(listing, risks)
        price_score = self._price_score(listing, advantages, disadvantages, risks)
        building_score = self._building_score(listing, advantages, disadvantages, risks)
        tenant_score = self._tenant_score(listing, advantages, disadvantages, risks)
        power_score = self._power_score(listing, advantages, disadvantages, risks)
        repair_score = self._repair_score(listing, advantages, disadvantages, risks)

        investment_score = round(
            price_score * 0.20
            + building_score * 0.12
            + tenant_score * 0.18
            + power_score * 0.14
            + repair_score * 0.10
            + liquidity_score * 0.14
            + data_quality_score * 0.12
            - risk_score * 0.18
            - fake_score * 0.12
        )
        investment_score = _clamp(investment_score)
        recommendation = self._recommend(investment_score, risk_score, fake_score, data_quality_score)
        short_summary = self._summary(recommendation, investment_score, risk_score, fake_score, risks)

        return InvestmentAnalysis(
            investment_score=investment_score,
            liquidity_score=liquidity_score,
            risk_score=risk_score,
            fake_score=fake_score,
            data_quality_score=data_quality_score,
            advantages=_unique(advantages),
            disadvantages=_unique(disadvantages),
            risks=_unique(risks),
            recommendation=recommendation,
            short_summary=short_summary,
        )

    def _data_quality_score(
        self,
        listing: NormalizedListing,
        disadvantages: list[str],
        risks: list[str],
    ) -> int:
        score = 100
        required_fields = [
            ("price_rub", listing.price_rub, "нет цены"),
            ("area_sqm", listing.area_sqm, "нет площади"),
            ("price_per_sqm", listing.price_per_sqm, "нет цены за м2"),
            ("address", listing.address, "нет точного адреса"),
            ("floor", listing.floor, "нет этажа"),
            ("building_year", listing.building_year, "нет года постройки"),
            ("property_type", listing.property_type, "нет типа помещения"),
        ]
        for _, value, message in required_fields:
            if value in (None, ""):
                score -= 9
                disadvantages.append(message)
                risks.append(f"missing data: {message}")

        if listing.electric_power_kw is None:
            score -= 12
            disadvantages.append("не указана электрическая мощность")
            risks.append("непонятно, хватит ли мощности для арендатора")

        if not listing.photos:
            score -= 6
            disadvantages.append("нет фотографий в нормализованных данных")

        return _clamp(score)

    def _liquidity_score(
        self,
        listing: NormalizedListing,
        advantages: list[str],
        disadvantages: list[str],
        risks: list[str],
    ) -> int:
        score = 45
        if listing.floor == 1:
            score += 18
            advantages.append("первый этаж повышает ликвидность")
        else:
            score -= 20
            disadvantages.append("объект не на первом этаже")
            risks.append("ликвидность ниже из-за этажа")

        if listing.has_federal_tenant:
            score += 18
            advantages.append("федеральный арендатор снижает риск простоя")

        if listing.price_rub and self.min_price_rub <= listing.price_rub <= self.max_price_rub:
            score += 8
        else:
            score -= 12
            disadvantages.append("цена вне целевого диапазона MVP")

        if listing.area_sqm:
            if 80 <= listing.area_sqm <= 450:
                score += 8
                advantages.append("площадь находится в ликвидном диапазоне")
            elif listing.area_sqm > 700:
                score -= 10
                risks.append("крупная площадь может сужать круг покупателей и арендаторов")

        if self._exposure_days(listing) and self._exposure_days(listing) >= self.long_exposure_days:
            score -= 15
            risks.append("долгая экспозиция может указывать на слабый спрос или завышенную цену")

        return _clamp(score)

    def _fake_score(self, listing: NormalizedListing, risks: list[str]) -> int:
        score = 8
        if not listing.address:
            score += 18
        if not listing.photos:
            score += 10
        if listing.price_per_sqm and listing.price_per_sqm < self.suspicious_low_price_per_sqm:
            score += 28
            risks.append("подозрительно низкая цена за м2 требует проверки")
        if listing.electric_power_kw is None:
            score += 8
        if not listing.seller_name and not listing.seller_phone_hash:
            score += 8
        if listing.has_federal_tenant:
            score -= 5
        return _clamp(score)

    def _risk_score(self, listing: NormalizedListing, risks: list[str]) -> int:
        score = 20
        if listing.floor != 1:
            score += 18
        if listing.building_year is None or listing.building_year < self.min_building_year:
            score += 14
        if listing.electric_power_kw is None:
            score += 14
        elif listing.electric_power_kw < self.minimum_usable_power_kw and not listing.electric_power_can_be_increased:
            score += 12
            risks.append("электрическая мощность может быть недостаточной")
        if listing.repair_condition in {"no_repair", "needs_repair", "shell_core"}:
            score += 12
            risks.append("потребуются вложения в ремонт или fit-out")
        if not listing.has_federal_tenant:
            score += 10
            risks.append("нет подтвержденного федерального арендатора")
        if self._exposure_days(listing) and self._exposure_days(listing) >= self.long_exposure_days:
            score += 12
        return _clamp(score)

    def _price_score(
        self,
        listing: NormalizedListing,
        advantages: list[str],
        disadvantages: list[str],
        risks: list[str],
    ) -> int:
        if listing.price_per_sqm is None:
            return 45
        if listing.price_per_sqm < self.suspicious_low_price_per_sqm:
            risks.append("цена за м2 выглядит слишком низкой для качественного street retail")
            return 35
        if listing.price_per_sqm <= 550_000:
            advantages.append("цена за м2 выглядит умеренной")
            return 82
        if listing.price_per_sqm <= 850_000:
            return 68
        disadvantages.append("высокая цена за м2")
        return 42

    def _building_score(
        self,
        listing: NormalizedListing,
        advantages: list[str],
        disadvantages: list[str],
        risks: list[str],
    ) -> int:
        if listing.building_year is None:
            return 45
        if listing.building_year >= self.min_building_year:
            advantages.append("здание введено в 2016 году или позже")
            return 85
        disadvantages.append("здание старше целевого критерия")
        risks.append("старое здание может потребовать дополнительных проверок")
        return 38

    def _tenant_score(
        self,
        listing: NormalizedListing,
        advantages: list[str],
        disadvantages: list[str],
        risks: list[str],
    ) -> int:
        if listing.has_federal_tenant:
            advantages.append("есть федеральный арендатор")
            return 92
        if listing.tenant_name:
            disadvantages.append("арендатор не подтвержден как федеральный")
            return 58
        disadvantages.append("нет данных об арендаторе")
        risks.append("риск простоя или слабого арендатора")
        return 38

    def _power_score(
        self,
        listing: NormalizedListing,
        advantages: list[str],
        disadvantages: list[str],
        risks: list[str],
    ) -> int:
        if listing.electric_power_kw is None:
            return 35
        if listing.electric_power_kw >= self.good_power_kw:
            advantages.append("высокая электрическая мощность")
            return 88
        if listing.electric_power_kw >= self.minimum_usable_power_kw:
            return 68
        if listing.electric_power_can_be_increased:
            advantages.append("мощность можно увеличить")
            return 62
        disadvantages.append("низкая электрическая мощность")
        risks.append("мощность может ограничить пул арендаторов")
        return 35

    def _repair_score(
        self,
        listing: NormalizedListing,
        advantages: list[str],
        disadvantages: list[str],
        risks: list[str],
    ) -> int:
        if listing.repair_condition in {"quality_repair", "has_repair"}:
            advantages.append("помещение с ремонтом")
            return 78
        if listing.repair_condition in {"no_repair", "needs_repair", "shell_core"}:
            disadvantages.append("требуются вложения в ремонт")
            return 36
        risks.append("состояние ремонта не подтверждено")
        return 52

    def _recommend(
        self,
        investment_score: int,
        risk_score: int,
        fake_score: int,
        data_quality_score: int,
    ) -> str:
        if investment_score >= 75 and risk_score <= 45 and fake_score <= 35 and data_quality_score >= 70:
            return "BUY"
        if investment_score < 50 or risk_score >= 70 or fake_score >= 60 or data_quality_score < 45:
            return "AVOID"
        return "WATCH"

    def _summary(
        self,
        recommendation: str,
        investment_score: int,
        risk_score: int,
        fake_score: int,
        risks: list[str],
    ) -> str:
        if recommendation == "BUY":
            return (
                f"BUY: score {investment_score}/100, risks {risk_score}/100, fake {fake_score}/100. "
                "Объект выглядит сильным, но ключевые допущения нужно подтвердить документами."
            )
        if recommendation == "AVOID":
            return (
                f"AVOID: score {investment_score}/100, risks {risk_score}/100, fake {fake_score}/100. "
                "Скептическая проверка выявила слишком много причин не покупать."
            )
        main_risk = risks[0] if risks else "нужна дополнительная проверка данных"
        return (
            f"WATCH: score {investment_score}/100, risks {risk_score}/100, fake {fake_score}/100. "
            f"Главный вопрос: {main_risk}."
        )

    def _exposure_days(self, listing: NormalizedListing) -> int | None:
        for key in ("exposure_days", "days_on_market"):
            value = listing.raw_payload.get(key)
            if value is not None:
                try:
                    return int(value)
                except (TypeError, ValueError):
                    return None

        if listing.published_at is None:
            return None
        published_at = listing.published_at
        if published_at.tzinfo is None:
            published_at = published_at.replace(tzinfo=timezone.utc)
        return max((datetime.now(timezone.utc) - published_at).days, 0)


def _clamp(value: int | float, minimum: int = 0, maximum: int = 100) -> int:
    return max(minimum, min(maximum, int(round(value))))


def _unique(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

