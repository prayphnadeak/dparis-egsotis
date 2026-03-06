"""Tests for authentication endpoints."""


def test_login_success(client, admin_user):
    r = client.post("/api/v1/auth/login", json={"username": "test_admin", "password": "TestAdmin@123"})
    assert r.status_code == 200
    data = r.json()
    assert "access_token" in data
    assert "refresh_token" in data


def test_login_wrong_password(client, admin_user):
    r = client.post("/api/v1/auth/login", json={"username": "test_admin", "password": "wrong"})
    assert r.status_code == 401


def test_login_unknown_user(client):
    r = client.post("/api/v1/auth/login", json={"username": "ghost", "password": "pass"})
    assert r.status_code == 401


def test_me_authenticated(client, auth_headers):
    r = client.get("/api/v1/auth/me", headers=auth_headers)
    assert r.status_code == 200
    assert r.json()["username"] == "test_admin"


def test_me_unauthenticated(client):
    r = client.get("/api/v1/auth/me")
    assert r.status_code == 403


def test_register(client):
    r = client.post("/api/v1/auth/register", json={
        "username": "newuser", "email": "new@test.id", "password": "Pass@1234"
    })
    assert r.status_code == 201
    assert r.json()["username"] == "newuser"
