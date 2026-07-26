from flask import Flask
from flask_migrate import Migrate

from config import Config
from models import db

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

# Import Blueprints
from routes.workout_routes import workout_bp
from routes.exercise_routes import exercise_bp
from routes.workout_exercise_routes import workout_exercise_bp

# Register Blueprints
app.register_blueprint(workout_bp)
app.register_blueprint(exercise_bp)
app.register_blueprint(workout_exercise_bp)


@app.route("/")
def home():
    return {
        "message": "Workout Tracker API",
        "version": "1.0"
    }


if __name__ == "__main__":
    app.run(port=5555, debug=True)