import pytest


@pytest.mark.django_db
def test_create_and_list_own_habits(auth_client):
    payload = {
        "place": "home",
        "time": "10:00:00",
        "action": "read book",
        "is_pleasant": False,
        "periodicity": 1,
        "reward": "tea",
        "duration_seconds": 60,
        "is_public": False,
    }
    resp = auth_client.post("/api/habits/", payload, format="json")
    assert resp.status_code in (200, 201)
    habit_id = resp.data["id"]

    # list must contain this habit
    resp_list = auth_client.get("/api/habits/")
    assert resp_list.status_code == 200
    results = resp_list.data.get("results", resp_list.data)
    assert any(h["id"] == habit_id for h in results)


@pytest.mark.django_db
def test_cannot_access_others_habit(auth_client, auth_client2):
    # user2 creates habit
    payload = {
        "place": "office",
        "time": "08:00:00",
        "action": "walk",
        "is_pleasant": False,
        "periodicity": 1,
        "reward": "coffee",
        "duration_seconds": 60,
        "is_public": False,
    }
    resp_create = auth_client2.post("/api/habits/", payload, format="json")
    habit_id = resp_create.data["id"]

    # user1 tries to retrieve user2's habit -> 404 (queryset filtered to own)
    resp_get = auth_client.get(f"/api/habits/{habit_id}/")
    assert resp_get.status_code in (403, 404)


@pytest.mark.django_db
def test_public_list_contains_only_public(api_client, auth_client):
    # create private and public
    base = {
        "place": "park",
        "time": "07:00:00",
        "action": "run",
        "is_pleasant": False,
        "periodicity": 1,
        "reward": "juice",
        "duration_seconds": 60,
    }
    auth_client.post("/api/habits/", {**base, "is_public": False}, format="json")
    auth_client.post("/api/habits/", {**base, "is_public": True, "action": "yoga"}, format="json")

    resp_public = api_client.get("/api/habits/public/")
    assert resp_public.status_code == 200
    results = resp_public.data.get("results", resp_public.data)
    assert all(item["is_public"] for item in results)


@pytest.mark.django_db
def test_business_rules_validation(auth_client):
    # pleasant habit cannot have reward or related_habit
    payload = {
        "place": "home",
        "time": "12:00:00",
        "action": "bath",
        "is_pleasant": True,
        "periodicity": 1,
        "reward": "chocolate",
        "duration_seconds": 60,
        "is_public": False,
    }
    resp = auth_client.post("/api/habits/", payload, format="json")
    assert resp.status_code == 400

    # duration must be <= 120
    payload2 = {
        "place": "home",
        "time": "12:00:00",
        "action": "meditate",
        "is_pleasant": False,
        "periodicity": 1,
        "reward": "",
        "duration_seconds": 121,
        "is_public": False,
    }
    resp2 = auth_client.post("/api/habits/", payload2, format="json")
    assert resp2.status_code == 400
