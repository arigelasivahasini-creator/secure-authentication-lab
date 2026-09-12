import pytest
from app import app, users, login_attempts
from werkzeug.security import check_password_hash


@pytest.fixture
def client():
    app.config["TESTING"] = True
    login_attempts.clear()
    return app.test_client()


def test_password_is_hashed():
    assert users["admin"] != "StrongPassword123!"
    assert check_password_hash(users["admin"], "StrongPassword123!")


def test_valid_login(client):
    response = client.post(
        "/login",
        data={
            "username": "admin",
            "password": "StrongPassword123!"
        },
        follow_redirects=False
    )

    assert response.status_code == 302
    assert "/dashboard" in response.headers["Location"]


def test_invalid_login_uses_generic_error(client):
    response = client.post(
        "/login",
        data={
            "username": "admin",
            "password": "wrong-password"
        }
    )

    assert response.status_code == 200
    assert b"Invalid username or password." in response.data


def test_input_validation(client):
    response = client.post(
        "/login",
        data={
            "username": "",
            "password": ""
        }
    )

    assert b"Invalid username or password." in response.data


def test_rate_limiting(client):
    for _ in range(5):
        client.post(
            "/login",
            data={
                "username": "admin",
                "password": "wrong-password"
            }
        )

    response = client.post(
        "/login",
        data={
            "username": "admin",
            "password": "wrong-password"
        }
    )

    assert b"Login temporarily unavailable" in response.data


def test_session_and_logout(client):
    response = client.post(
        "/login",
        data={
            "username": "admin",
            "password": "StrongPassword123!"
        }
    )

    assert response.status_code == 302

    dashboard = client.get("/dashboard")
    assert dashboard.status_code == 200
    assert b"successfully authenticated" in dashboard.data

    logout = client.get("/logout")
    assert logout.status_code == 200

    protected = client.get("/dashboard")
    assert protected.status_code == 302
    assert "/login" in protected.headers["Location"]


def test_secure_session_configuration():
    assert app.config["SESSION_COOKIE_HTTPONLY"] is True
    assert app.config["SESSION_COOKIE_SAMESITE"] == "Lax"
    assert app.config["PERMANENT_SESSION_LIFETIME"].total_seconds() == 900
