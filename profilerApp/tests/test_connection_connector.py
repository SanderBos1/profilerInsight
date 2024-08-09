def test_get_connected_tables(client):
    response = client.get('/api/get_connected_tables')
    assert response.status_code == 200
    assert response.json == {'Answer': []}

def test_ingest_connected_tables(client):
    response = client.get('/api/ingest_connected_tables')
    assert response.status_code == 200
    assert response.json == {'Message':"connection_loaded"}

def test_get_connections(client):
    response = client.get('/api/get_connections')
    assert response.status_code == 200
    assert response.json == {
    "Answer": [
        {
            "connection_id": "test",
            "database": "profilerDB",
            "db_type": "postgres",
            "host": "localhost",
            "port": "5432",
            "username": "postgres"
        }
    ]
}
    
def test_add_connection(client):
    response = client.post('/api/add_postgres_connection', json={"connection_id": "new_id", "host": "localhost", "port": "5432", "username": "postgres", "password": "test", "database": "profilerDB", "db_type": "postgres"})
    assert response.status_code == 200
    assert response.json == {"Message":"Connection Added Succesfully!"}

def test_add_existing_connection(client):
    response = client.post('/api/add_postgres_connection', json={"connection_id": "test", "host": "localhost", "port": "5432", "username": "postgres", "password": "test", "database": "profilerDB", "db_type": "postgres"})
    assert response.status_code == 500
    assert response.json == {"Error": "Connection_id already exists"}


def test_add_connection_wrong_schema(client):
    response = client.post('/api/add_postgres_connection', json={"connection_id": "test", "host": "localhost"})
    assert response.status_code == 400
    assert response.json == {"Error": "Missing Fields."}

def test_delete_connection_unkown(client):
    connection_id = 1
    response = client.delete(f'/api/delete_connection/{connection_id}')
    assert response.status_code == 404
    assert response.json == {'Error':"Connection not found"}

def test_delete_connection(client):
    connection_id = "test"
    response = client.delete(f'/api/delete_connection/{connection_id}')
    assert response.status_code == 200
    assert response.json == {'Message':"Connection deleted successfully!"}