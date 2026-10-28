import unittest
from copy import deepcopy
from unittest.mock import patch

from fastapi.testclient import TestClient

from src.app import activities, app


class UnregisterParticipantTests(unittest.TestCase):
    def setUp(self):
        self.activities = deepcopy(activities)
        patcher = patch("src.app.activities", self.activities)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.client = TestClient(app)
        self.addCleanup(self.client.close)

    def test_removes_only_the_selected_participant(self):
        other_activities = deepcopy(self.activities)
        response = self.client.delete(
            "/activities/Chess%20Club/participants",
            params={"email": "michael@mergington.edu"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "message": "Unregistered michael@mergington.edu from Chess Club"
        })
        other_activities["Chess Club"]["participants"].remove("michael@mergington.edu")
        self.assertEqual(self.client.get("/activities").json(), other_activities)

    def test_unknown_activity_returns_not_found_without_changes(self):
        original = deepcopy(self.activities)
        response = self.client.delete(
            "/activities/Unknown/participants",
            params={"email": "michael@mergington.edu"},
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Activity not found"})
        self.assertEqual(self.activities, original)

    def test_unknown_participant_returns_not_found_without_changes(self):
        original = deepcopy(self.activities)
        response = self.client.delete(
            "/activities/Chess%20Club/participants",
            params={"email": "missing@mergington.edu"},
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Participant not found"})
        self.assertEqual(self.activities, original)

    def test_email_is_required(self):
        original = deepcopy(self.activities)
        response = self.client.delete("/activities/Chess%20Club/participants")

        self.assertEqual(response.status_code, 422)
        self.assertEqual(self.activities, original)

    def test_can_remove_last_participant_and_sign_up_again(self):
        email = "student+art@mergington.edu"
        self.client.post("/activities/Art%20Club/signup", params={"email": email})
        response = self.client.delete(
            "/activities/Art%20Club/participants", params={"email": email}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.activities["Art Club"]["participants"], [])
        repeated = self.client.delete(
            "/activities/Art%20Club/participants", params={"email": email}
        )
        self.assertEqual(repeated.status_code, 404)
        signup = self.client.post(
            "/activities/Art%20Club/signup", params={"email": email}
        )
        self.assertEqual(signup.status_code, 200)
        self.assertEqual(self.activities["Art Club"]["participants"], [email])
