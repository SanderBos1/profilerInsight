# tests/conftest.py
import pytest
from src import create_app
from src.config import SingletonDB
from src.models import DbConnections

@pytest.fixture(scope='function')
def app():

    # Create the app and configure it for testing
    app = create_app(config_name='test')
    with app.app_context():

        # Create all tables
        db = SingletonDB.get_instance()
        db.create_all()

        # Add test data
        new_connection = DbConnections(connection_id="test", host="localhost", port="5432", username="postgres", password="test", database="profilerDB", db_type="postgres")
        db.session.add(new_connection)
        db.session.commit()

        # csv config:
        app.config['csv_folder'] = 'mock/path'
    
    yield app

    # Teardown after all tests are complete
    with app.app_context():
        # Drop all tables
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()
