from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from models import db, Workout
from schemas import workout_schema, workouts_schema

workout_bp = Blueprint("workouts", __name__)

@workout_bp.get("/workouts")
def get_workouts():

    workouts = Workout.query.all()

    return jsonify(
        workouts_schema.dump(workouts)
    ), 200

@workout_bp.get("/workouts/<int:id>")
def get_workout(id):

    workout = Workout.query.get(id)

    if not workout:
        return {"error": "Workout not found"}, 404

    return workout_schema.dump(workout), 200

@workout_bp.post("/workouts")
def create_workout():

    json_data = request.get_json()

    try:

        data = workout_schema.load(json_data)

        workout = Workout(**data)

        db.session.add(workout)

        db.session.commit()

        return workout_schema.dump(workout), 201

    except ValidationError as err:

        return {"errors": err.messages}, 400

    except Exception as e:

        db.session.rollback()

        return {"error": str(e)}, 400


@workout_bp.delete("/workouts/<int:id>")
def delete_workout(id):

    workout = Workout.query.get(id)

    if not workout:

        return {"error": "Workout not found"}, 404

    db.session.delete(workout)

    db.session.commit()

    return {"message": "Workout deleted successfully"}, 200