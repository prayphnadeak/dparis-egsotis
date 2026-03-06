"""Tests for tourism endpoints."""


def test_list_tourism_empty(client):
    r = client.get("/api/v1/tourism/")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_create_and_get_tourism(client, auth_headers):
    payload = {"name": "AIR TERJUN TEST", "category": "Air Terjun", "description": "Test waterfall", "latitude": -4.01, "longitude": 103.25}
    create_r = client.post("/api/v1/tourism/", json=payload, headers=auth_headers)
    assert create_r.status_code == 201
    item_id = create_r.json()["id"]

    get_r = client.get(f"/api/v1/tourism/{item_id}")
    assert get_r.status_code == 200
    assert get_r.json()["name"] == "AIR TERJUN TEST"


def test_create_tourism_unauthorized(client):
    r = client.post("/api/v1/tourism/", json={"name": "X", "category": "Y"})
    assert r.status_code == 403
