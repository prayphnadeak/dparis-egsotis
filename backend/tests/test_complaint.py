"""Tests for complaint (pengaduan) endpoints."""


def test_submit_complaint(client):
    payload = {
        "name": "Andi Saputra",
        "phone": "08123456789",
        "category": "Wisata",
        "message": "Jalan menuju air terjun perlu diperbaiki."
    }
    r = client.post("/api/v1/complaints/", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data["name"] == "Andi Saputra"
    assert data["tracking_code"] is not None
    return data["tracking_code"]


def test_track_complaint(client):
    # Submit first
    payload = {"name": "Budi", "category": "Kuliner", "message": "Pengaduan test"}
    r = client.post("/api/v1/complaints/", json=payload)
    code = r.json()["tracking_code"]

    track_r = client.post("/api/v1/complaints/track", json={"tracking_code": code})
    assert track_r.status_code == 200
    assert track_r.json()["tracking_code"] == code


def test_track_invalid_code(client):
    r = client.post("/api/v1/complaints/track", json={"tracking_code": "INVALID-CODE"})
    assert r.status_code == 404


def test_list_complaints_admin_only(client):
    r = client.get("/api/v1/complaints/")
    assert r.status_code == 403


def test_list_complaints_as_admin(client, auth_headers):
    r = client.get("/api/v1/complaints/", headers=auth_headers)
    assert r.status_code == 200
    assert isinstance(r.json(), list)
