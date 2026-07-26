import os
import sys
import tempfile
import pytest

# Allow importing from server/
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "server")
    )
)

from app import app
from models import db


@pytest.fixture
def client():

    db_fd, db_path = tempfile.mkstemp()

    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"

    with app.test_client() as client:

        with app.app_context():
            db.create_all()

        yield client

        with app.app_context():
            db.session.remove()
            db.drop_all()

    os.close(db_fd)
    os.unlink(db_path)