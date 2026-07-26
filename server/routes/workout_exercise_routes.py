from flask import Blueprint, request
from marshmallow import ValidationError

from models import db
from models import Workout
from models import Exercise
from models import WorkoutExercise

from schemas import workout_exercise_schema

workout_exercise_bp = Blueprint(
    "workout_exercises",
    __name__
)

@workout_exercise_bp.post(
    "/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises"
)
def add_exercise(workout_id, exercise_id):

    workout = Workout.query.get(workout_id)

    exercise = Exercise.query.get(exercise_id)

    if workout is None:

        return {"error": "Workout not found"}, 404

    if exercise is None:

        return {"error": "Exercise not found"}, 404

    try:

        data = workout_exercise_schema.load(
            request.get_json()
        )

        association = WorkoutExercise(

            workout_id=workout.id,

            exercise_id=exercise.id,

            reps=data.get("reps"),

            sets=data.get("sets"),

            duration_seconds=data.get(
                "duration_seconds"
            ),
        )

        db.session.add(association)

        db.session.commit()

        return workout_exercise_schema.dump(
            association
        ), 201

    except ValidationError as err:

        return {"errors": err.messages}, 400

    except Exception as e:

        db.session.rollback()

        return {"error": str(e)}, 400