from flask import Blueprint, request
from marshmallow import ValidationError

from models import db, Exercise
from schemas import exercise_schema, exercises_schema

exercise_bp = Blueprint("exercises", __name__)

@exercise_bp.get("/exercises")
def get_exercises():

    exercises = Exercise.query.all()

    return exercises_schema.dump(exercises), 200

@exercise_bp.get("/exercises/<int:id>")
def get_exercise(id):

    exercise = Exercise.query.get(id)

    if exercise is None:

        return {"error": "Exercise not found"}, 404

    return exercise_schema.dump(exercise), 200

@exercise_bp.post("/exercises")
def create_exercise():

    try:

        data = exercise_schema.load(request.get_json())

        exercise = Exercise(**data)

        db.session.add(exercise)

        db.session.commit()

        return exercise_schema.dump(exercise), 201

    except ValidationError as err:

        return {"errors": err.messages}, 400

    except Exception as e:

        db.session.rollback()

        return {"error": str(e)}, 400

@exercise_bp.delete("/exercises/<int:id>")
def delete_exercise(id):

    exercise = Exercise.query.get(id)

    if exercise is None:

        return {"error": "Exercise not found"}, 404

    db.session.delete(exercise)

    db.session.commit()

    return {"message": "Exercise deleted"}, 200 