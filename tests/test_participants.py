from copy import deepcopy


def test_removes_only_the_selected_participant(client, activities):
    expected = deepcopy(activities)
    expected["Chess Club"]["participants"].remove("michael@mergington.edu")

    response = client.delete(
        "/activities/Chess%20Club/participants",
        params={"email": "michael@mergington.edu"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Unregistered michael@mergington.edu from Chess Club"
    }
    assert client.get("/activities").json() == expected
    assert activities == expected


def test_unknown_activity_returns_not_found_without_changes(client, activities):
    original = deepcopy(activities)

    response = client.delete(
        "/activities/Unknown/participants",
        params={"email": "michael@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}
    assert client.get("/activities").json() == original
    assert activities == original


def test_unknown_participant_returns_not_found_without_changes(client, activities):
    original = deepcopy(activities)

    response = client.delete(
        "/activities/Chess%20Club/participants",
        params={"email": "missing@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Participant not found"}
    assert client.get("/activities").json() == original
    assert activities == original


def test_unregister_requires_email(client, activities):
    original = deepcopy(activities)

    response = client.delete("/activities/Chess%20Club/participants")

    assert response.status_code == 422
    errors = response.json()["detail"]
    assert len(errors) == 1
    assert errors[0]["loc"] == ["query", "email"]
    assert errors[0]["type"] == "missing"
    assert client.get("/activities").json() == original
    assert activities == original


def test_can_remove_last_participant_and_sign_up_again(client, activities):
    original = deepcopy(activities)
    email = "student+art@mergington.edu"
    signup = client.post("/activities/Art%20Club/signup", params={"email": email})
    assert signup.status_code == 200

    response = client.delete(
        "/activities/Art%20Club/participants", params={"email": email}
    )

    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from Art Club"}
    assert activities == original
    assert client.get("/activities").json() == original

    repeated = client.delete(
        "/activities/Art%20Club/participants", params={"email": email}
    )
    assert repeated.status_code == 404
    assert repeated.json() == {"detail": "Participant not found"}
    assert activities == original
    assert client.get("/activities").json() == original

    signup = client.post("/activities/Art%20Club/signup", params={"email": email})
    expected = deepcopy(original)
    expected["Art Club"]["participants"].append(email)
    assert signup.status_code == 200
    assert signup.json() == {"message": f"Signed up {email} for Art Club"}
    assert activities == expected
    assert client.get("/activities").json() == expected
