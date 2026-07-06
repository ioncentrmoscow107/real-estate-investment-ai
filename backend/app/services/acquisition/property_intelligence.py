from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any

from app.services.acquisition.models import NormalizedListing


SCORE_NAMES = (
    "investment_score",
    "liquidity_score",
    "tenant_score",
    "building_score",
    "location_score",
    "risk_score",
    "fake_score",
    "data_quality_score",
)


DEFAULT_RULES_PATH = Path(__file__).with_name("rules") / "property_intelligence_rules.json"


@dataclass(frozen=True, slots=True)
class ScoreExplanation:
    score: int
    explanations: list[str] = field(default_factory=list)
    applied_rules: list[str] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class PropertyIntelligence:
    investment_score: int
    liquidity_score: int
    tenant_score: int
    building_score: int
    location_score: int
    risk_score: int
    fake_score: int
    data_quality_score: int
    advantages: list[str]
    disadvantages: list[str]
    risks: list[str]
    missing_information: list[str]
    due_diligence_checklist: list[str]
    explanations: dict[str, ScoreExplanation]
    recommendation: str
    short_summary: str
    rules_version: str


class PropertyIntelligenceService:
    """Deterministic rule engine for commercial property intelligence."""

    def __init__(self, rules_path: Path | None = None) -> None:
        self.rules_path = rules_path or DEFAULT_RULES_PATH
        self.rules_config = self._load_rules(self.rules_path)

    def analyze(self, listing: NormalizedListing) -> PropertyIntelligence:
        context = self._build_context(listing)
        scores = {
            name: int(value)
            for name, value in self.rules_config["score_defaults"].items()
            if name in SCORE_NAMES
        }
        explanation_map: dict[str, list[str]] = {name: [] for name in SCORE_NAMES}
        applied_rules: dict[str, list[str]] = {name: [] for name in SCORE_NAMES}
        advantages: list[str] = []
        disadvantages: list[str] = []
        risks: list[str] = []
        missing_information: list[str] = []
        due_diligence: list[str] = []

        for rule in self.rules_config["rules"]:
            if not self._rule_matches(rule, context):
                continue

            rule_id = str(rule["id"])
            advantages.extend(rule.get("advantages", []))
            disadvantages.extend(rule.get("disadvantages", []))
            risks.extend(rule.get("risks", []))
            missing_information.extend(rule.get("missing_information", []))
            due_diligence.extend(rule.get("due_diligence", []))

            for score_name, delta in rule.get("score_adjustments", {}).items():
                if score_name not in scores:
                    continue
                scores[score_name] = _clamp(scores[score_name] + int(delta))
                applied_rules[score_name].append(rule_id)
                explanation = rule.get("explanations", {}).get(score_name)
                if explanation:
                    explanation_map[score_name].append(str(explanation))
                else:
                    explanation_map[score_name].append(f"Rule {rule_id} adjusted {score_name} by {delta}.")

        explanations = {
            name: ScoreExplanation(
                score=scores[name],
                explanations=explanation_map[name] or ["No specific rule adjusted this score."],
                applied_rules=applied_rules[name],
            )
            for name in SCORE_NAMES
        }
        recommendation = self._recommend(scores)
        short_summary = self._summary(scores, recommendation, risks, missing_information)

        return PropertyIntelligence(
            investment_score=scores["investment_score"],
            liquidity_score=scores["liquidity_score"],
            tenant_score=scores["tenant_score"],
            building_score=scores["building_score"],
            location_score=scores["location_score"],
            risk_score=scores["risk_score"],
            fake_score=scores["fake_score"],
            data_quality_score=scores["data_quality_score"],
            advantages=_unique(advantages),
            disadvantages=_unique(disadvantages),
            risks=_unique(risks),
            missing_information=_unique(missing_information),
            due_diligence_checklist=_unique(due_diligence),
            explanations=explanations,
            recommendation=recommendation,
            short_summary=short_summary,
            rules_version=str(self.rules_config.get("version", "unknown")),
        )

    def _build_context(self, listing: NormalizedListing) -> dict[str, Any]:
        raw_payload = listing.raw_payload or {}
        exposure_days = raw_payload.get("exposure_days", raw_payload.get("days_on_market"))
        try:
            exposure_days = int(exposure_days) if exposure_days is not None else None
        except (TypeError, ValueError):
            exposure_days = None

        context = {
            "source": listing.source,
            "source_listing_id": listing.source_listing_id,
            "source_url": listing.source_url,
            "title": listing.title,
            "description": listing.description,
            "address": listing.address,
            "latitude": listing.latitude,
            "longitude": listing.longitude,
            "price_rub": listing.price_rub,
            "area_sqm": listing.area_sqm,
            "price_per_sqm": listing.price_per_sqm,
            "floor": listing.floor,
            "total_floors": listing.total_floors,
            "building_year": listing.building_year,
            "property_type": listing.property_type,
            "tenant_name": listing.tenant_name,
            "tenant_type": listing.tenant_type,
            "has_federal_tenant": listing.has_federal_tenant,
            "electric_power_kw": listing.electric_power_kw,
            "electric_power_verified": listing.electric_power_verified,
            "electric_power_can_be_increased": listing.electric_power_can_be_increased,
            "electric_power_increase_to_kw": listing.electric_power_increase_to_kw,
            "repair_condition": listing.repair_condition,
            "photos_count": len(listing.photos),
            "seller_name": listing.seller_name,
            "seller_phone_hash": listing.seller_phone_hash,
            "exposure_days": exposure_days,
        }
        context.update({f"raw.{key}": value for key, value in raw_payload.items()})
        return context

    def _rule_matches(self, rule: dict[str, Any], context: dict[str, Any]) -> bool:
        return all(self._condition_matches(condition, context) for condition in rule.get("conditions", []))

    def _condition_matches(self, condition: dict[str, Any], context: dict[str, Any]) -> bool:
        field = str(condition["field"])
        operator = str(condition["operator"])
        expected = condition.get("value")
        actual = context.get(field)

        if operator == "missing":
            return actual in (None, "", [])
        if operator == "present":
            return actual not in (None, "", [])
        if actual is None:
            return False
        if operator == "eq":
            return actual == expected
        if operator == "neq":
            return actual != expected
        if operator == "lt":
            return actual < expected
        if operator == "lte":
            return actual <= expected
        if operator == "gt":
            return actual > expected
        if operator == "gte":
            return actual >= expected
        if operator == "in":
            return actual in expected
        if operator == "not_between":
            low, high = expected
            return not (low <= actual <= high)
        raise ValueError(f"Unsupported rule operator: {operator}")

    def _recommend(self, scores: dict[str, int]) -> str:
        thresholds = self.rules_config["recommendation_thresholds"]
        if (
            scores["investment_score"] >= thresholds["buy_min_investment_score"]
            and scores["risk_score"] <= thresholds["buy_max_risk_score"]
            and scores["fake_score"] <= thresholds["buy_max_fake_score"]
            and scores["data_quality_score"] >= thresholds["buy_min_data_quality_score"]
        ):
            return "BUY"
        if (
            scores["investment_score"] <= thresholds["avoid_max_investment_score"]
            or scores["risk_score"] >= thresholds["avoid_min_risk_score"]
            or scores["fake_score"] >= thresholds["avoid_min_fake_score"]
            or scores["data_quality_score"] <= thresholds["avoid_max_data_quality_score"]
        ):
            return "AVOID"
        return "WATCH"

    def _summary(
        self,
        scores: dict[str, int],
        recommendation: str,
        risks: list[str],
        missing_information: list[str],
    ) -> str:
        if recommendation == "BUY":
            return (
                f"BUY: investment {scores['investment_score']}/100, "
                f"risk {scores['risk_score']}/100, fake {scores['fake_score']}/100. "
                "Strong profile, but verify lease, title, utilities, and capex before purchase."
            )
        if recommendation == "AVOID":
            return (
                f"AVOID: investment {scores['investment_score']}/100, "
                f"risk {scores['risk_score']}/100, fake {scores['fake_score']}/100. "
                "The rule engine found material reasons not to buy."
            )
        if risks:
            focus = risks[0]
        elif missing_information:
            focus = f"missing {missing_information[0]}"
        else:
            focus = "additional verification required"
        return (
            f"WATCH: investment {scores['investment_score']}/100, "
            f"risk {scores['risk_score']}/100, fake {scores['fake_score']}/100. "
            f"Primary concern: {focus}."
        )

    def _load_rules(self, path: Path) -> dict[str, Any]:
        with path.open("r", encoding="utf-8") as rules_file:
            return json.load(rules_file)


def _clamp(value: int, minimum: int = 0, maximum: int = 100) -> int:
    return max(minimum, min(maximum, value))


def _unique(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

