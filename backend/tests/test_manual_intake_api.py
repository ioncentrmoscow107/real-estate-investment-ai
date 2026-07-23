import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.session import Base, get_db
from app.main import app
from app.services.manual_intake import detect_listing_source


@pytest.fixture
def client() -> TestClient:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    testing_session = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(engine)

    def override_get_db():
        db: Session = testing_session()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    test_client = TestClient(app)
    yield test_client
    test_client.close()
    app.dependency_overrides.clear()
    Base.metadata.drop_all(engine)
    engine.dispose()


def test_detect_listing_source_uses_hostname_boundaries() -> None:
    assert detect_listing_source("https://www.cian.ru/sale/commercial/123/") == "cian"
    assert detect_listing_source("https://m.avito.ru/moskva/kommercheskaya_nedvizhimost/123") == "avito"
    assert detect_listing_source("https://domclick.ru/card/sale__flat__123") == "domclick"
    assert detect_listing_source("https://realty.yandex.ru/offer/123/") == "yandex_realty"
    assert detect_listing_source("https://cian.ru.attacker.example/offer/123") is None
    assert detect_listing_source("https://example.test/cian/123") is None


def test_create_and_read_manual_intake_batch(client: TestClient) -> None:
    response = client.post(
        "/api/v1/manual-intake/batches",
        json={
            "name": "Проверка объектов СЗАО",
            "description": "URL, выбранные инвестором",
            "linked_search_profile_id": "commercial-100-400m",
            "urls": [
                "https://www.cian.ru/sale/commercial/123/",
                "https://www.avito.ru/moskva/kommercheskaya_nedvizhimost/456",
                "https://example.test/unsupported/789",
            ],
        },
    )

    assert response.status_code == 201
    batch = response.json()
    assert batch["status"] == "queued"
    assert batch["source"] == "manual"
    assert batch["total_urls"] == 3
    assert batch["processed_count"] == 1
    assert batch["failed_count"] == 1
    assert batch["analyzed_count"] == 0
    assert [item["source_detected"] for item in batch["urls"]] == [
        "cian",
        "avito",
        "unknown",
    ]
    assert [item["status"] for item in batch["urls"]] == [
        "queued",
        "queued",
        "failed",
    ]
    assert batch["urls"][2]["error_message"] == "Unsupported listing source"

    batch_id = batch["id"]
    detail_response = client.get(f"/api/v1/manual-intake/batches/{batch_id}")
    assert detail_response.status_code == 200
    assert detail_response.json() == batch

    list_response = client.get("/api/v1/manual-intake/batches")
    assert list_response.status_code == 200
    assert [item["id"] for item in list_response.json()] == [batch_id]


def test_batch_fails_when_every_source_is_unsupported(client: TestClient) -> None:
    response = client.post(
        "/api/v1/manual-intake/batches",
        json={
            "name": "Неподдерживаемые ссылки",
            "urls": [
                "https://example.test/listing/1",
                "https://cian.ru.attacker.example/listing/2",
            ],
        },
    )

    assert response.status_code == 201
    batch = response.json()
    assert batch["status"] == "failed"
    assert batch["processed_count"] == 2
    assert batch["failed_count"] == 2


def test_manual_intake_rejects_duplicate_urls(client: TestClient) -> None:
    response = client.post(
        "/api/v1/manual-intake/batches",
        json={
            "name": "Дубли",
            "urls": [
                "https://www.cian.ru/sale/commercial/123/",
                "https://www.cian.ru/sale/commercial/123/",
            ],
        },
    )

    assert response.status_code == 422


def test_manual_intake_returns_404_for_unknown_batch(client: TestClient) -> None:
    response = client.get("/api/v1/manual-intake/batches/missing")

    assert response.status_code == 404
    assert response.json()["detail"] == "Manual intake batch not found"
