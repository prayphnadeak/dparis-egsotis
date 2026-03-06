"""Tests for souvenir (oleh-oleh) endpoints."""


def test_list_souvenirs_empty(client):
    r = client.get("/api/v1/souvenirs/")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_create_souvenir(client, auth_headers):
    payload = {"name": "TOKO OLEH-OLEH TEST", "maps_link": "https://maps.google.com/?q=test"}
    r = client.post("/api/v1/souvenirs/", json=payload, headers=auth_headers)
    assert r.status_code == 201
    data = r.json()
    assert data["name"] == "TOKO OLEH-OLEH TEST"
    assert data["maps_link"] == "https://maps.google.com/?q=test"
    return data["id"]


def test_get_souvenir(client, auth_headers):
    # create first
    payload = {"name": "TOKO GET TEST", "maps_link": None}
    create_r = client.post("/api/v1/souvenirs/", json=payload, headers=auth_headers)
    shop_id = create_r.json()["id"]

    r = client.get(f"/api/v1/souvenirs/{shop_id}")
    assert r.status_code == 200
    assert r.json()["id"] == shop_id


def test_get_souvenir_not_found(client):
    r = client.get("/api/v1/souvenirs/99999")
    assert r.status_code == 404


def test_create_souvenir_unauthorized(client):
    r = client.post("/api/v1/souvenirs/", json={"name": "X"})
    assert r.status_code == 403
