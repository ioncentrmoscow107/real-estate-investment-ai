from fastapi.testclient import TestClient

from app.main import app


def test_dashboard_properties_endpoint_returns_sample_contract() -> None:
    with TestClient(app) as client:
        response = client.get("/api/v1/dashboard/properties")

    assert response.status_code == 200

    payload = response.json()
    assert set(payload) == {
        "summary",
        "properties",
        "manual_intake_batches",
        "search_profiles",
        "intake_funnels",
    }
    assert payload["summary"]["total_properties"] == len(payload["properties"])
    assert payload["summary"]["total_properties"] > 0
