from datetime import date
import pytest

from models import Exercise
from models import Workout


def test_create_exercise():

    exercise = Exercise(
        name="Push Ups",
        category="Strength",
        equipment_needed=False
    )

    assert exercise.name == "Push Ups"


def test_invalid_workout_duration():

    with pytest.raises(ValueError):

        Workout(
            date=date.today(),
            duration_minutes=-10,
            notes="Bad workout"
        )


def test_invalid_exercise_name():

    with pytest.raises(ValueError):

        Exercise(
            name="A",
            category="Strength",
            equipment_needed=False
        )