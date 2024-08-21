def test_get_connected_tables(client):
    response = client.get('/api/load_tables/conn123')
    assert response.status_code == 200
    assert response.json == {"Answer": [
        {
            'db_name': 'testDB', 
            'table_id': 1, 
            'connection_id': 'conn123', 
            'schema_name': 'testSchema', 
            'table_name': 'testTable', 
            'data_quality': '100.0000000000'}]
    }

def test_get_table_info(client):
    response = client.get('/api/get_table_info/1')
    assert response.status_code == 200
    assert response.json == {"Answer": {
        'db_name': 'testDB', 
        'table_id': 1, 
        'connection_id': 'conn123', 
        'schema_name': 'testSchema', 
        'table_name': 'testTable', 
        'data_quality': '100.0000000000'}
    }