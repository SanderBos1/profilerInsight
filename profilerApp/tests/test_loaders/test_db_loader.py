from src.loaders import db_loader

def test_db_loader_get_connection_info(app):

    """
    Test the get_connection_info method of the DbLoader class.
    
    The method should return the connection information for a table.
    """
    with app.app_context():

        new_loader = db_loader.DbLoader()
        connection_dict, table_info, password = new_loader.get_connection_info(1)

        expected_connection_dict = {
            "connection_id": 'conn123',
            "server": 'testServer',
            "port": 1234,
            "username": 'testUser',
            "database": 'testDB',
            "db_type": 'postgres',
            "extra_info": None
        }

        expected_table_info= {
            "db_name": "testDB",
            "table_id": 1,
            "connection_id": 'conn123',
            "schema_name": 'testSchema',
            "table_name": 'testTable',
            "data_quality": 100
        }
        
        assert connection_dict == expected_connection_dict
        assert password == 'test_password'
        assert table_info == expected_table_info

