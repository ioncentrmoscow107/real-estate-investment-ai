from app.services.dashboard_samples import get_sample_dashboard_properties


def test_dashboard_sample_response_structure() -> None:
    response = get_sample_dashboard_properties()

    assert set(response.keys()) == {"summary", "properties"}
    assert response["summary"]["total_properties"] == len(response["properties"])
    assert response["summary"]["total_properties"] > 0
    assert 0 <= response["summary"]["average_investment_score"] <= 100
    assert set(response["summary"]["recommendations"].keys()) == {"BUY", "WATCH", "AVOID"}

    required_property_fields = {
        "id",
        "source",
        "source_url",
        "title",
        "address",
        "price_rub",
        "area_sqm",
        "price_per_sqm",
        "electric_power_kw",
        "electric_power_increase_to_kw",
        "repair_condition",
        "has_federal_tenant",
        "last_updated",
        "investment_score",
        "liquidity_score",
        "tenant_score",
        "building_score",
        "location_score",
        "risk_score",
        "fake_score",
        "data_quality_score",
        "recommendation",
        "advantages",
        "disadvantages",
        "risks",
        "missing_information",
        "due_diligence_checklist",
        "short_summary",
        "explanations",
    }

    for property_item in response["properties"]:
        assert required_property_fields.issubset(property_item.keys())
        assert property_item["recommendation"] in {"BUY", "WATCH", "AVOID"}
        for score_name in [
            "investment_score",
            "liquidity_score",
            "tenant_score",
            "building_score",
            "location_score",
            "risk_score",
            "fake_score",
            "data_quality_score",
        ]:
            assert 0 <= property_item[score_name] <= 100

        assert isinstance(property_item["advantages"], list)
        assert isinstance(property_item["disadvantages"], list)
        assert isinstance(property_item["risks"], list)
        assert isinstance(property_item["missing_information"], list)
        assert isinstance(property_item["due_diligence_checklist"], list)


def test_dashboard_samples_are_russian_investor_facing() -> None:
    response = get_sample_dashboard_properties()

    assert "average_risk_score" in response["summary"]
    assert response["summary"]["recommendations"]["BUY"] >= 1
    assert response["summary"]["recommendations"]["WATCH"] >= 1
    assert response["summary"]["recommendations"]["AVOID"] >= 1

    all_text = " ".join(
        " ".join(
            [
                property_item["title"],
                property_item["short_summary"],
                *property_item["advantages"],
                *property_item["disadvantages"],
                *property_item["risks"],
                *property_item["missing_information"],
                *property_item["due_diligence_checklist"],
            ]
        )
        for property_item in response["properties"]
    )

    assert "Федеральный арендатор" in all_text
    assert "Проверить выписку ЕГРН" in all_text
    assert "Не подтверждена электрическая мощность" in all_text
