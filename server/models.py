from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import CheckConstraint
from datetime import date

db = SQLAlchemy()


# =====================================
# WorkoutExercise (Join Table)
# =====================================

class WorkoutExercise(db.Model):
    __tablename__ = "workout_exercises"

    id = db.Column(db.Integer, primary_key=True)

    workout_id = db.Column(
        db.Integer,
        db.ForeignKey("workouts.id", ondelete="CASCADE"),
        nullable=False
    )

    exercise_id = db.Column(
        db.Integer,
        db.ForeignKey("exercises.id", ondelete="CASCADE"),
        nullable=False
    )

    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    # Relationships
    workout = db.relationship(
        "Workout",
        back_populates="workout_exercises"
    )

    exercise = db.relationship(
        "Exercise",
        back_populates="workout_exercises"
    )

    # ---------- Table Constraints ----------
    __table_args__ = (

        CheckConstraint(
            "(reps IS NOT NULL) OR (duration_seconds IS NOT NULL)",
            name="exercise_requires_reps_or_duration"
        ),

        CheckConstraint(
            "(sets IS NULL) OR (sets > 0)",
            name="sets_positive"
        ),

        CheckConstraint(
            "(reps IS NULL) OR (reps > 0)",
            name="reps_positive"
        ),

        CheckConstraint(
            "(duration_seconds IS NULL) OR (duration_seconds > 0)",
            name="duration_positive"
        ),
    )

    # ---------- Model Validations ----------

    @validates("sets")
    def validate_sets(self, key, value):
        if value is not None and value <= 0:
            raise ValueError("Sets must be greater than zero.")
        return value

    @validates("reps")
    def validate_reps(self, key, value):
        if value is not None and value <= 0:
            raise ValueError("Reps must be greater than zero.")
        return value

    @validates("duration_seconds")
    def validate_duration(self, key, value):
        if value is not None and value <= 0:
            raise ValueError("Duration must be greater than zero.")
        return value


# =====================================
# Workout
# =====================================

class Workout(db.Model):
    __tablename__ = "workouts"

    id = db.Column(db.Integer, primary_key=True)

    date = db.Column(
        db.Date,
        nullable=False
    )

    duration_minutes = db.Column(
        db.Integer,
        nullable=False
    )

    notes = db.Column(db.Text)

    # Relationships

    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="workout",
        cascade="all, delete-orphan"
    )

    exercises = db.relationship(
        "Exercise",
        secondary="workout_exercises",
        back_populates="workouts",
        viewonly=True
    )

    # ---------- Table Constraints ----------

    __table_args__ = (

        CheckConstraint(
            "duration_minutes > 0",
            name="duration_positive"
        ),

    )

    # ---------- Model Validations ----------

    @validates("duration_minutes")
    def validate_duration(self, key, value):

        if value <= 0:
            raise ValueError(
                "Workout duration must be greater than zero."
            )

        return value

    @validates("date")
    def validate_date(self, key, value):

        if value > date.today():
            raise ValueError(
                "Workout date cannot be in the future."
            )

        return value


# =====================================
# Exercise
# =====================================

class Exercise(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(100),
        nullable=False,
        unique=True
    )

    category = db.Column(
        db.String(50),
        nullable=False
    )

    equipment_needed = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    # Relationships

    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="exercise",
        cascade="all, delete-orphan"
    )

    workouts = db.relationship(
        "Workout",
        secondary="workout_exercises",
        back_populates="exercises",
        viewonly=True
    )

    # ---------- Model Validations ----------

    @validates("name")
    def validate_name(self, key, value):

        if not value:
            raise ValueError("Exercise name is required.")

        if len(value.strip()) < 3:
            raise ValueError(
                "Exercise name must be at least 3 characters."
            )

        return value.strip().title()

    @validates("category")
    def validate_category(self, key, value):

        allowed = [
            "Strength",
            "Cardio",
            "Flexibility",
            "Balance",
            "HIIT",
            "Mobility"
        ]

        if value not in allowed:
            raise ValueError(
                f"Category must be one of {allowed}"
            )

        return value