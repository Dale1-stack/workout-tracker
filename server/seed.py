#!/usr/bin/env python3

from datetime import date

from app import app
from models import db, Workout, Exercise, WorkoutExercise


with app.app_context():

    print("Deleting existing data...")

    # Delete join table first (foreign keys)
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()

    db.session.commit()

    print("Creating exercises...")

    pushups = Exercise(
        name="Push Ups",
        category="Strength",
        equipment_needed=False
    )

    squats = Exercise(
        name="Squats",
        category="Strength",
        equipment_needed=False
    )

    plank = Exercise(
        name="Plank",
        category="Balance",
        equipment_needed=False
    )

    running = Exercise(
        name="Running",
        category="Cardio",
        equipment_needed=False
    )

    jumping_jacks = Exercise(
        name="Jumping Jacks",
        category="HIIT",
        equipment_needed=False
    )

    yoga = Exercise(
        name="Yoga Stretch",
        category="Flexibility",
        equipment_needed=False
    )

    db.session.add_all([
        pushups,
        squats,
        plank,
        running,
        jumping_jacks,
        yoga
    ])

    db.session.commit()

    print("Exercises created.")

    print("Creating workouts...")

    workout1 = Workout(
        date=date(2026, 7, 20),
        duration_minutes=45,
        notes="Upper body strength session."
    )

    workout2 = Workout(
        date=date(2026, 7, 22),
        duration_minutes=60,
        notes="Cardio and endurance."
    )

    workout3 = Workout(
        date=date(2026, 7, 24),
        duration_minutes=40,
        notes="Full body conditioning."
    )

    db.session.add_all([
        workout1,
        workout2,
        workout3
    ])

    db.session.commit()

    print("Workouts created.")

    print("Creating workout exercises...")

    workout_exercises = [

        WorkoutExercise(
            workout_id=workout1.id,
            exercise_id=pushups.id,
            reps=15,
            sets=4
        ),

        WorkoutExercise(
            workout_id=workout1.id,
            exercise_id=squats.id,
            reps=20,
            sets=4
        ),

        WorkoutExercise(
            workout_id=workout1.id,
            exercise_id=plank.id,
            duration_seconds=60,
            sets=3
        ),

        WorkoutExercise(
            workout_id=workout2.id,
            exercise_id=running.id,
            duration_seconds=1800,
            sets=1
        ),

        WorkoutExercise(
            workout_id=workout2.id,
            exercise_id=jumping_jacks.id,
            reps=30,
            sets=5
        ),

        WorkoutExercise(
            workout_id=workout3.id,
            exercise_id=pushups.id,
            reps=12,
            sets=3
        ),

        WorkoutExercise(
            workout_id=workout3.id,
            exercise_id=running.id,
            duration_seconds=900,
            sets=1
        ),

        WorkoutExercise(
            workout_id=workout3.id,
            exercise_id=yoga.id,
            duration_seconds=600,
            sets=1
        )

    ]

    db.session.add_all(workout_exercises)

    db.session.commit()

    print("Workout exercises created.")

    print("----------------------------------")
    print("Database seeded successfully!")
    print(f"Exercises: {Exercise.query.count()}")
    print(f"Workouts: {Workout.query.count()}")
    print(f"Workout Exercises: {WorkoutExercise.query.count()}")
    print("----------------------------------")