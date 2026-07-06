from app.services.acquisition.extraction import (
    detect_tenant,
    extract_electric_power,
    extract_repair_condition,
)


def test_electric_power_examples() -> None:
    power = extract_electric_power("электрическая мощность 80 кВт")
    assert power.power_kw == 80
    assert power.verified is True

    power = extract_electric_power("мощность 50 кВт, возможно увеличение до 100 кВт")
    assert power.power_kw == 50
    assert power.can_be_increased is True
    assert power.increase_to_kw == 100

    power = extract_electric_power("выделенная мощность 120кВт")
    assert power.power_kw == 120


def test_repair_condition_examples() -> None:
    assert extract_repair_condition("без ремонта") == "no_repair"
    assert extract_repair_condition("shell&core") == "shell_core"
    assert extract_repair_condition("сделан качественный ремонт") == "quality_repair"
    assert extract_repair_condition("требуется ремонт") == "needs_repair"


def test_federal_tenant_detection_examples() -> None:
    for text, expected in [
        ("Пятерочка", "Пятерочка"),
        ("ВкусВилл", "ВкусВилл"),
        ("Магнит", "Магнит"),
        ("Ozon", "Ozon"),
        ("Wildberries", "Wildberries"),
        ("Аптека", "Аптека"),
    ]:
        tenant = detect_tenant(text)
        assert tenant.has_federal_tenant is True
        assert tenant.tenant_name == expected
        assert tenant.tenant_type == "federal"

