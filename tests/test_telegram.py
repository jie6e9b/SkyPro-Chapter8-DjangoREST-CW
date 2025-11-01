import pytest


@pytest.mark.django_db
def test_link_and_unlink_chat_id(auth_client):
    # Link
    resp = auth_client.post("/api/telegram/link/", {"chat_id": "123456"}, format="json")
    assert resp.status_code == 200
    assert resp.data["chat_id"] == "123456"

    # Unlink
    resp2 = auth_client.delete("/api/telegram/unlink/")
    assert resp2.status_code == 204
