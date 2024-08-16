import pytest
from src import create_app
from src.config import SingletonDB

@pytest.fixture(scope='function')
def app():

    # Create the app and configure it for testing
    app = create_app(config_name='test')
    with app.app_context():

        # Create all tables
        db = SingletonDB.get_instance()
        db.create_all()

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