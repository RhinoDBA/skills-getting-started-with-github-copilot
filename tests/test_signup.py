from copy import deepcopy

import pytest


@pytest.mark.parametrize(
    "email",
    ["new@mergington.edu", "student+chess@mergington.edu", "student&chess@mergington.edu"],
)
def test_signup_adds_only_the_requested_participant(client, activities, email):
    expected = deepcopy(activities)
    expected["Chess Club"]["participants"].append(email)

    response = client.post("/activities/Chess%20Club/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for Chess Club"}
    assert client.get("/activities").json() == expected
    assert activities == expected


@pytest.mark.parametrize(
    ("activity", "email", "status", "detail"),
    [
        ("Chess%20Club", "michael@mergington.edu", 400, "Student already signed up"),
        ("Unknown", "new@mergington.edu", 404, "Activity not found"),
    ],
)
def test_rejected_signup_leaves_activities_unchanged(
    client, activities, activity, email, status, detail
):
    original = deepcopy(activities)

    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    assert response.status_code == status
    assert response.json() == {"detail": detail}
    assert client.get("/activities").json() == original
    assert activities == original


def test_signup_requires_email(client, activities):
    original = deepcopy(activities)

    response = client.post("/activities/Chess%20Club/signup")

    assert response.status_code == 422
    errors = response.json()["detail"]
    assert len(errors) == 1
    assert errors[0]["loc"] == ["query", "email"]
    assert errors[0]["type"] == "missing"
    assert client.get("/activities").json() == original
    assert activities == original
