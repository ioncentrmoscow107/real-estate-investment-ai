from app.services.dashboard_samples import get_sample_dashboard_properties


def test_dashboard_sample_response_structure() -> None:
    response = get_sample_dashboard_properties()

    assert set(response.keys()) == {
        "summary",
        "properties",
        "manual_intake_batches",
        "search_profiles",
        "intake_funnels",
    }
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
        "floor",
        "building_year",
        "property_type",
        "search_profile_ids",
        "district",
        "metro",
        "property_category",
        "deal_type",
        "tenant_exists",
        "rent_yield_percent",
        "market_support_level",
        "manual_overrides",
        "correction_history",
        "property_workflow_status",
        "property_workflow_status_label",
        "workflow_next_action",
        "requested_documents",
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
        assert isinstance(property_item["search_profile_ids"], list)
        assert property_item["deal_type"] in {"sale", "rent"}
        assert property_item["property_category"]
        assert property_item["property_workflow_status"]
        assert property_item["property_workflow_status_label"]
        assert property_item["workflow_next_action"]
        assert isinstance(property_item["manual_overrides"], dict)
        assert isinstance(property_item["correction_history"], list)
        assert isinstance(property_item["requested_documents"], list)


def test_property_workflow_and_manual_overrides_are_present() -> None:
    response = get_sample_dashboard_properties()
    properties = response["properties"]

    assert any(item["manual_overrides"] for item in properties)
    assert any(item["correction_history"] for item in properties)
    assert any(item["requested_documents"] for item in properties)

    override_keys = {
        "label",
        "original_value",
        "override_value",
        "source",
        "comment",
        "updated_at",
    }
    history_keys = {
        "field",
        "label",
        "old_value",
        "new_value",
        "source",
        "comment",
        "changed_at",
    }
    document_keys = {"title", "status", "status_label", "comment"}
    workflow_statuses = {
        "new",
        "interesting",
        "in_review",
        "documents_requested",
        "egrn_check",
        "negotiation",
        "price_negotiation",
        "rejected",
        "archived",
        "deal_pipeline",
    }
    document_statuses = {"received", "requested", "missing", "not_required"}

    properties_with_overrides = 0
    properties_with_documents = 0

    for property_item in properties:
        assert property_item["property_workflow_status"] in workflow_statuses

        if property_item["manual_overrides"]:
            properties_with_overrides += 1
            for override in property_item["manual_overrides"].values():
                assert override_keys == set(override.keys())

        if property_item["correction_history"]:
            for history_item in property_item["correction_history"]:
                assert history_keys == set(history_item.keys())

        if property_item["requested_documents"]:
            properties_with_documents += 1
            for document in property_item["requested_documents"]:
                assert document_keys == set(document.keys())
                assert document["status"] in document_statuses

    assert properties_with_overrides >= 2
    assert properties_with_documents >= 2


def test_search_profiles_and_intake_funnels_are_present() -> None:
    response = get_sample_dashboard_properties()
    profiles = response["search_profiles"]
    profile_names = {profile["name"] for profile in profiles}

    assert profile_names == {
        "Коммерция 100–400 млн",
        "Малые помещения до 30 млн",
        "Офисы 30–150 млн",
        "Помещения с арендаторами",
        "Пользовательский профиль",
    }

    required_filter_keys = {
        "price_min",
        "price_max",
        "price_per_sqm_min",
        "price_per_sqm_max",
        "area_min",
        "area_max",
        "floor_min",
        "floor_max",
        "first_floor_only",
        "location_query",
        "source",
        "property_category",
        "deal_type",
        "recommendation",
        "investment_score_min",
        "risk_max",
        "data_quality_min",
        "tenant_exists",
        "federal_tenant_only",
        "rent_yield_min",
        "electric_power_min",
        "building_year_min",
        "only_with_photos",
        "only_with_missing_information",
        "market_support_level",
    }

    for profile in profiles:
        assert required_filter_keys == set(profile["default_filters"].keys())
        assert profile["id"] in response["intake_funnels"]
        funnel = response["intake_funnels"][profile["id"]]
        assert funnel["active_profile_id"] == profile["id"]
        assert "source_breakdown" in funnel
        assert "location_breakdown" in funnel

    assert any("small-premises-under-30m" in item["search_profile_ids"] for item in response["properties"])
    assert any("offices-30-150m" in item["search_profile_ids"] for item in response["properties"])
    assert any("tenant-income" in item["search_profile_ids"] for item in response["properties"])


def test_manual_intake_batches_are_present() -> None:
    response = get_sample_dashboard_properties()
    batches = response["manual_intake_batches"]

    assert len(batches) == 2
    assert {batch["name"] for batch in batches} == {
        "Объекты СЗАО от инвестора",
        "Помещения до 30 млн",
    }

    required_batch_fields = {
        "id",
        "name",
        "description",
        "created_at",
        "status",
        "urls",
        "total_urls",
        "processed_count",
        "failed_count",
        "analyzed_count",
        "source",
        "linked_search_profile_id",
    }
    required_url_fields = {
        "id",
        "url",
        "source_detected",
        "status",
        "error_message",
        "created_at",
    }
    allowed_statuses = {"draft", "queued", "processing", "analyzed", "failed"}

    for batch in batches:
        assert required_batch_fields.issubset(batch.keys())
        assert batch["source"] == "manual"
        assert batch["status"] in allowed_statuses
        assert batch["total_urls"] == len(batch["urls"])
        assert 0 <= batch["analyzed_count"] <= batch["total_urls"]

        for url_item in batch["urls"]:
            assert required_url_fields.issubset(url_item.keys())
            assert url_item["url"].startswith("https://example.test/")
            assert url_item["status"] in allowed_statuses


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
