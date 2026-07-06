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
        "investment_score",
        "liquidity_score",
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

