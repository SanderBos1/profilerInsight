import pytest
from src import create_app
from src.config import SingletonDB
from src.models import DbConnections, ConnectedTables

@pytest.fixture(scope='function')
def app():
    # Create the app and configure it for testing
    app = create_app(config_name='test')
    
    # Use the app context to set up the database and add test data
    with app.app_context():
        # Get the database instance and create all tables
        db_instance = SingletonDB.get_instance()
        db_instance.create_all()
        
        # Add test data to the database
        connection = DbConnections(
            connection_id='conn123', 
            server='testServer', 
            port=1234, 
            username='testUser', 
            password='test_password', 
            database='testDB',
            db_type='postgres'
        )
        table = ConnectedTables(
            db_name = 'testDB',
            table_id=1, 
            connection_id='conn123',
            schemaName='testSchema',
            tableName='testTable'
        )
    
        db_instance.session.add(connection)
        db_instance.session.add(table)
        db_instance.session.commit()

        # Set the CSV folder path in the app config
        app.config['csv_folder'] = 'mock/path'
        
        # Yield the app object for testing
        yield app
        
        # Teardown: Drop all tables after tests are done
        with app.app_context():
            # Drop all tables
            db_instance.drop_all()

@pytest.fixture()
def client(app):
    return app.test_client()