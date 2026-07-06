from __future__ import annotations

from dataclasses import dataclass
import re


@dataclass(frozen=True, slots=True)
class ElectricPowerExtraction:
    power_kw: float | None
    verified: bool
    can_be_increased: bool
    increase_to_kw: float | None
    source_text: str | None


@dataclass(frozen=True, slots=True)
class TenantDetection:
    tenant_name: str | None
    tenant_type: str | None
    has_federal_tenant: bool


FEDERAL_TENANTS: tuple[tuple[str, str], ...] = (
    ("пятерочка", "Пятерочка"),
    ("пятёрочка", "Пятерочка"),
    ("вкусвилл", "ВкусВилл"),
    ("магнит", "Магнит"),
    ("ozon", "Ozon"),
    ("озон", "Ozon"),
    ("wildberries", "Wildberries"),
    ("вайлдберриз", "Wildberries"),
    ("аптека", "Аптека"),
)


def extract_electric_power(text: str | None) -> ElectricPowerExtraction:
    if not text:
        return ElectricPowerExtraction(None, False, False, None, None)

    normalized = _normalize_text(text)
    power_matches = list(
        re.finditer(
            r"(?:электрическая\s+)?(?:выделенная\s+)?мощность\s*(\d+(?:[.,]\d+)?)\s*квт",
            normalized,
            flags=re.IGNORECASE,
        )
    )
    compact_matches = list(
        re.finditer(r"(\d+(?:[.,]\d+)?)\s*квт", normalized, flags=re.IGNORECASE)
    )
    primary_match = power_matches[0] if power_matches else (compact_matches[0] if compact_matches else None)
    primary_power = _to_float(primary_match.group(1)) if primary_match else None

    increase_match = re.search(
        r"(?:увеличени[ея]|увеличить|увеличение\s+до|возможно\s+увеличение\s+до)\D{0,30}(\d+(?:[.,]\d+)?)\s*квт",
        normalized,
        flags=re.IGNORECASE,
    )
    increase_to_kw = _to_float(increase_match.group(1)) if increase_match else None
    can_be_increased = bool(increase_match or re.search(r"возможн\w*\s+увеличени", normalized))

    source_text = None
    if primary_match:
        start = max(primary_match.start() - 35, 0)
        end = min(primary_match.end() + 55, len(text))
        source_text = text[start:end].strip()

    return ElectricPowerExtraction(
        power_kw=primary_power,
        verified=primary_power is not None,
        can_be_increased=can_be_increased,
        increase_to_kw=increase_to_kw,
        source_text=source_text,
    )


def extract_repair_condition(text: str | None) -> str | None:
    if not text:
        return None

    normalized = _normalize_text(text)
    if re.search(r"shell\s*&\s*core|shell\s+and\s+core|шелл\s*энд\s*кор", normalized):
        return "shell_core"
    if "без ремонта" in normalized:
        return "no_repair"
    if "требуется ремонт" in normalized or "нужен ремонт" in normalized:
        return "needs_repair"
    if "качественный ремонт" in normalized or "сделан ремонт" in normalized:
        return "quality_repair"
    if "ремонт" in normalized:
        return "has_repair"
    return None


def detect_tenant(text: str | None) -> TenantDetection:
    if not text:
        return TenantDetection(None, None, False)

    normalized = _normalize_text(text)
    for needle, canonical_name in FEDERAL_TENANTS:
        if needle in normalized:
            return TenantDetection(canonical_name, "federal", True)

    return TenantDetection(None, None, False)


def _normalize_text(text: str) -> str:
    return " ".join(text.lower().replace("ё", "е").split())


def _to_float(value: str | None) -> float | None:
    if value is None:
        return None
    return float(value.replace(",", "."))

