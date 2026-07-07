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
        "market_signal",
        "score_explanations",
        "photos",
        "building_context",
        "surroundings_context",
        "traffic_context",
        "competition_context",
        "nearby_sale_comparables",
        "sale_comparables_summary",
        "nearby_rental_rates",
        "rental_rates_summary",
        "district_market_trends",
        "residential_market_context",
        "market_support_summary",
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
        assert isinstance(property_item["photos"], list)
        assert isinstance(property_item["score_explanations"], dict)
        assert isinstance(property_item["building_context"], dict)
        assert isinstance(property_item["surroundings_context"], dict)
        assert isinstance(property_item["traffic_context"], dict)
        assert isinstance(property_item["competition_context"], dict)
        assert isinstance(property_item["nearby_sale_comparables"], list)
        assert isinstance(property_item["sale_comparables_summary"], dict)
        assert isinstance(property_item["nearby_rental_rates"], list)
        assert isinstance(property_item["rental_rates_summary"], dict)
        assert isinstance(property_item["district_market_trends"], dict)
        assert isinstance(property_item["residential_market_context"], dict)
        assert isinstance(property_item["market_support_summary"], dict)


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


def test_property_market_intelligence_blocks_are_present() -> None:
    response = get_sample_dashboard_properties()
    score_names = {
        "investment_score",
        "liquidity_score",
        "tenant_score",
        "building_score",
        "location_score",
        "risk_score",
        "fake_score",
        "data_quality_score",
    }

    for property_item in response["properties"]:
        assert property_item["photos"]
        assert any(photo["is_main"] for photo in property_item["photos"])

        assert score_names.issubset(property_item["score_explanations"].keys())
        for score_name in score_names:
            explanation = property_item["score_explanations"][score_name]
            assert set(explanation.keys()) == {"positive_factors", "negative_factors", "summary"}
            assert isinstance(explanation["positive_factors"], list)
            assert isinstance(explanation["negative_factors"], list)
            assert explanation["summary"]

        assert property_item["building_context"]["building_year"]
        assert "comments" in property_item["building_context"]
        assert property_item["surroundings_context"]["radius_m"] > 0
        assert "key_anchors" in property_item["surroundings_context"]
        assert property_item["traffic_context"]["pedestrian_traffic_level"]
        assert property_item["competition_context"]["competitor_categories"]
        assert property_item["nearby_sale_comparables"]
        assert property_item["sale_comparables_summary"]["conclusion"]
        assert property_item["nearby_rental_rates"]
        assert property_item["rental_rates_summary"]["conclusion"]
        assert property_item["district_market_trends"]["commercial_rent_trend"]["trend"]
        assert property_item["residential_market_context"]["resale_market"]["demand_level"]
        assert property_item["market_support_summary"]["support_level"]


def test_property_market_intelligence_contains_russian_market_text() -> None:
    response = get_sample_dashboard_properties()
    all_text = " ".join(
        " ".join(
            [
                property_item["market_signal"],
                property_item["market_support_summary"]["support_level"],
                property_item["market_support_summary"]["conclusion"],
                property_item["sale_comparables_summary"]["conclusion"],
                property_item["rental_rates_summary"]["conclusion"],
                property_item["building_context"]["comments"],
                property_item["surroundings_context"]["comments"],
                property_item["traffic_context"]["comments"],
                property_item["competition_context"]["comments"],
                property_item["residential_market_context"]["new_development"]["comments"],
                property_item["residential_market_context"]["resale_market"]["comments"],
            ]
        )
        for property_item in response["properties"]
    )

    assert "рынок поддерживает" in all_text
    assert "Продажи" not in all_text
    assert "аренда" in all_text.lower()
    assert "новые ЖК" in all_text
