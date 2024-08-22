import os
import pytest

from src import create_app
from src.config import SingletonDB
from src.models import DbConnections, ConnectedTables, QualityRules

@pytest.fixture(scope="function")
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
            schema_name='testSchema',
            table_name='testTable',
            data_quality=100
        )
        quality_rule = QualityRules(
            table_id=1,
            connection_id='conn123',
            quality_rule="No Empty Rule",
            column_name='testColumn',
            threshold=1.0
        )
    
        db_instance.session.add(connection)
        db_instance.session.add(table)
        db_instance.session.add(quality_rule)
        db_instance.session.commit()

        # Set the CSV folder path in the app config
        base_folder = os.path.dirname(os.path.abspath(__file__))

        app.config['file_folder'] = os.path.join(base_folder, 'test_data')
        app.config['properties_folder'] = os.path.join(base_folder, 'test_data')

        
        # Yield the app object for testing
        yield app
        
        # Teardown: Drop all tables after tests are done
        try:
            db_instance.drop_all()
            print("Databases are dropped")
        except Exception as e:
            print(f"Error dropping databases: {e}")

@pytest.fixture(scope="function")
def client(app):
    return app.test_client()