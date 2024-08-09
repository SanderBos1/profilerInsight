# tests/conftest.py
import pytest
from src import create_app, db
from src.models import dbConnections

@pytest.fixture()
def app():

    # Create the app and configure it for testing
    app = create_app(config_name='test')
    with app.app_context():

        # Create all tables
        db.create_all()

        # Add test data
        new_connection = dbConnections(connection_id="test", host="localhost", port="5432", username="postgres", password="test", database="profilerDB", db_type="postgres")
        db.session.add(new_connection)
        db.session.commit()
    
    yield app

    # Teardown after all tests are complete
    with app.app_context():
        # Drop all tables
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()
