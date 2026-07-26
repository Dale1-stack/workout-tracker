from datetime import date


def test_home(client):

    response = client.get("/")

    assert response.status_code == 200


def test_get_workouts(client):

    response = client.get("/workouts")

    assert response.status_code == 200


def test_get_exercises(client):

    response = client.get("/exercises")

    assert response.status_code == 200


def test_create_workout(client):

    payload = {

        "date": str(date.today()),

        "duration_minutes": 45,

        "notes": "Morning workout"

    }

    response = client.post(
        "/workouts",
        json=payload
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["duration_minutes"] == 45


def test_create_exercise(client):

    payload = {

        "name": "Burpees",

        "category": "HIIT",

        "equipment_needed": False

    }

    response = client.post(
        "/exercises",
        json=payload
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["name"] == "Burpees"