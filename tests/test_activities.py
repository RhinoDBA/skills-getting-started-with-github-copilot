from copy import deepcopy


def test_root_redirects_to_activity_page(client, activities):
    original = deepcopy(activities)

    response = client.get("/", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"
    assert activities == original


def test_lists_activities_with_details_and_participants(client, activities):
    original = deepcopy(activities)

    response = client.get("/activities")

    assert response.status_code == 200
    assert response.json() == original
    assert activities == original


def test_lists_no_activities_when_empty(client, activities):
    activities.clear()

    response = client.get("/activities")

    assert response.status_code == 200
    assert response.json() == {}
    assert activities == {}
