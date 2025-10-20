import pytest


@pytest.mark.django_db
def test_register_and_obtain_token(api_client):
    # Register
    resp = api_client.post(
        "/api/accounts/register/",
        {"username": "newuser", "password": "Str0ngPass!", "email": "u@example.com"},
        format="json",
    )
    assert resp.status_code == 201
    assert resp.data["username"] == "newuser"

    # Obtain JWT
    resp2 = api_client.post(
        "/api/accounts/token/obtain/",
        {"username": "newuser", "password": "Str0ngPass!"},
        format="json",
    )
    assert resp2.status_code == 200
    assert "access" in resp2.data and "refresh" in resp2.data
