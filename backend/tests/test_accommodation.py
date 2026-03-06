"""Tests for accommodation endpoints."""


def test_list_accommodations_empty(client):
    r = client.get("/api/v1/accommodations/")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_create_accommodation(client, auth_headers):
    payload = {
        "name": "HOTEL TEST", "category": "Hotel Non Bintang",
        "total_rooms": 10, "phone": "0811111111",
        "hot_water": True, "tv_cable": False, "bed": True,
        "free_wifi": True, "restaurant": False, "swimming_pool": False,
        "gym": False, "meeting_room": False
    }
    r = client.post("/api/v1/accommodations/", json=payload, headers=auth_headers)
    assert r.status_code == 201
    data = r.json()
    assert data["name"] == "HOTEL TEST"
    return data["id"]


def test_get_accommodation(client, auth_headers):
    # create first
    payload = {"name": "HOTEL GET", "category": "Homestay", "total_rooms": 3, "bed": True}
    create_r = client.post("/api/v1/accommodations/", json=payload, headers=auth_headers)
    acc_id = create_r.json()["id"]

    r = client.get(f"/api/v1/accommodations/{acc_id}")
    assert r.status_code == 200
    assert r.json()["id"] == acc_id


def test_get_accommodation_not_found(client):
    r = client.get("/api/v1/accommodations/99999")
    assert r.status_code == 404


def test_create_accommodation_unauthorized(client):
    r = client.post("/api/v1/accommodations/", json={"name": "X", "category": "Y", "total_rooms": 1, "bed": True})
    assert r.status_code == 403
