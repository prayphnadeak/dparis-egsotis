"""Tests for culinary endpoints."""


def test_list_culinary(client):
    r = client.get("/api/v1/culinary/")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_create_and_get_culinary(client, auth_headers):
    payload = {"name": "CAFE TEST", "category": "Cafe", "opening_hours": "09.00-22.00", "phone": "08199999999"}
    r = client.post("/api/v1/culinary/", json=payload, headers=auth_headers)
    assert r.status_code == 201
    item_id = r.json()["id"]

    get_r = client.get(f"/api/v1/culinary/{item_id}")
    assert get_r.status_code == 200
    assert get_r.json()["name"] == "CAFE TEST"


def test_culinary_search(client, auth_headers):
    payload = {"name": "KEDAI SEARCHABLE", "category": "Kedai"}
    client.post("/api/v1/culinary/", json=payload, headers=auth_headers)
    r = client.get("/api/v1/culinary/?q=SEARCHABLE")
    assert r.status_code == 200
