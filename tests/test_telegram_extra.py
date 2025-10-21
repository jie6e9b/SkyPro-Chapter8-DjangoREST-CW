import pytest


@pytest.mark.django_db
def test_link_requires_chat_id(auth_client):
    resp = auth_client.post("/api/telegram/link/", {}, format="json")
    assert resp.status_code == 400
    assert "chat_id" in resp.data
