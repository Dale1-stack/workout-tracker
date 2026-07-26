from marshmallow import (
    Schema,
    fields,
    validates,
    ValidationError,
    validates_schema
)
from datetime import date


# =====================================
# WorkoutExercise Schema
# =====================================

class WorkoutExerciseSchema(Schema):

    id = fields.Int(dump_only=True)

    workout_id = fields.Int(required=True)

    exercise_id = fields.Int(required=True)

    reps = fields.Int(allow_none=True)

    sets = fields.Int(allow_none=True)

    duration_seconds = fields.Int(allow_none=True)

    @validates("reps")
    def validate_reps(self, value):

        if value is not None and value <= 0:
            raise ValidationError(
                "Reps must be greater than zero."
            )

    @validates("sets")
    def validate_sets(self, value):

        if value is not None and value <= 0:
            raise ValidationError(
                "Sets must be greater than zero."
            )

    @validates("duration_seconds")
    def validate_duration(self, value):

        if value is not None and value <= 0:
            raise ValidationError(
                "Duration must be greater than zero."
            )

    @validates_schema
    def validate_workout(self, data, **kwargs):

        if data.get("reps") is None and data.get("duration_seconds") is None:
            raise ValidationError(
                "Either reps or duration_seconds must be supplied."
            )


# =====================================
# Exercise Schema
# =====================================

class ExerciseSchema(Schema):

    id = fields.Int(dump_only=True)

    name = fields.Str(required=True)

    category = fields.Str(required=True)

    equipment_needed = fields.Bool(required=True)

    workouts = fields.List(
        fields.Nested(
            lambda: WorkoutSummarySchema()
        ),
        dump_only=True
    )

    @validates("name")
    def validate_name(self, value):

        if len(value.strip()) < 3:
            raise ValidationError(
                "Exercise name must contain at least 3 characters."
            )

    @validates("category")
    def validate_category(self, value):

        allowed = [
            "Strength",
            "Cardio",
            "Flexibility",
            "Balance",
            "HIIT",
            "Mobility"
        ]

        if value not in allowed:
            raise ValidationError(
                f"Category must be one of {allowed}"
            )


# =====================================
# Workout Summary Schema
# =====================================

class WorkoutSummarySchema(Schema):

    id = fields.Int()

    date = fields.Date()

    duration_minutes = fields.Int()


# =====================================
# Exercise Summary Schema
# =====================================

class ExerciseSummarySchema(Schema):

    id = fields.Int()

    name = fields.Str()

    category = fields.Str()

    equipment_needed = fields.Bool()


# =====================================
# Workout Schema
# =====================================

class WorkoutSchema(Schema):

    id = fields.Int(dump_only=True)

    date = fields.Date(required=True)

    duration_minutes = fields.Int(required=True)

    notes = fields.Str(allow_none=True)

    exercises = fields.List(
        fields.Nested(
            ExerciseSummarySchema
        ),
        dump_only=True
    )

    @validates("duration_minutes")
    def validate_duration(self, value):

        if value <= 0:
            raise ValidationError(
                "Workout duration must be greater than zero."
            )

    @validates("date")
    def validate_date(self, value):

        if value > date.today():
            raise ValidationError(
                "Workout date cannot be in the future."
            )


# =====================================
# Schema Instances
# =====================================

exercise_schema = ExerciseSchema()

exercises_schema = ExerciseSchema(many=True)

workout_schema = WorkoutSchema()

workouts_schema = WorkoutSchema(many=True)

workout_exercise_schema = WorkoutExerciseSchema()

workout_exercises_schema = WorkoutExerciseSchema(many=True)