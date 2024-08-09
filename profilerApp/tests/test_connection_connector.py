def test_get_connected_tables(client):
    """
    Test the API endpoint for retrieving connected tables.

    This test sends a GET request to the '/api/get_connected_tables' endpoint
    and asserts that the response status code is 200 and the response JSON
    contains an empty list under the key 'Answer'.
    """
    response = client.get('/api/get_connected_tables')
    assert response.status_code == 200
    assert response.json == {'Answer': []}

def test_ingest_connected_tables(client):
    """
    Test the API endpoint for ingesting connected tables.

    This test sends a GET request to the '/api/ingest_connected_tables' endpoint
    and asserts that the response status code is 200 and the response JSON
    contains a message indicating that the connection was loaded.
    """
    response = client.get('/api/ingest_connected_tables')
    assert response.status_code == 200
    assert response.json == {'Message': "connection_loaded"}

def test_get_connections(client):
    """
    Test the API endpoint for retrieving connections.

    This test sends a GET request to the '/api/get_connections' endpoint
    and asserts that the response status code is 200 and the response JSON
    contains a list of connections with the expected fields.
    """
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
    """
    Test the API endpoint for adding a new PostgreSQL connection.

    This test sends a POST request to the '/api/add_postgres_connection' endpoint
    with a JSON payload for a new connection. It asserts that the response status
    code is 200 and the response JSON contains a message indicating successful addition.
    """
    response = client.post('/api/add_postgres_connection', json={
        "connection_id": "new_id",
        "host": "localhost",
        "port": "5432",
        "username": "postgres",
        "password": "test",
        "database": "profilerDB",
        "db_type": "postgres"
    })
    assert response.status_code == 200
    assert response.json == {"Message":"Connection Added Succesfully!"}

def test_add_existing_connection(client):
    """
    Test the API endpoint for attempting to add an existing PostgreSQL connection.

    This test sends a POST request to the '/api/add_postgres_connection' endpoint
    with a JSON payload for a connection that already exists. It asserts that the
    response status code is 500 and the response JSON contains an error message
    indicating that the connection_id already exists.
    """
    response = client.post('/api/add_postgres_connection', json={
        "connection_id": "test",
        "host": "localhost",
        "port": "5432",
        "username": "postgres",
        "password": "test",
        "database": "profilerDB",
        "db_type": "postgres"
    })
    assert response.status_code == 500
    assert response.json == {"Error": "Connection_id already exists"}

def test_add_connection_wrong_schema(client):
    """
    Test the API endpoint for adding a PostgreSQL connection with incorrect schema.

    This test sends a POST request to the '/api/add_postgres_connection' endpoint
    with a JSON payload that is missing required fields. It asserts that the response
    status code is 400 and the response JSON contains an error message indicating
    missing fields.
    """
    response = client.post('/api/add_postgres_connection', json={
        "connection_id": "test",
        "host": "localhost"
    })
    assert response.status_code == 400
    assert response.json == {"Error": "Incorrect Data"}

def test_add_connection_empty_data(client):
    """
    Test the API endpoint for adding a PostgreSQL connection with empty values

    This test sends a POST request to the '/api/add_postgres_connection' endpoint
    with a JSON payload that has empty data. It asserts that the response
    status code is 400 and the response JSON contains an error message indicating
    that something was wrong with the input
    """
    response = client.post('/api/add_postgres_connection', json={
        "connection_id": "",
        "host": "",
        "port": "",
        "username": "",
        "password": "",
        "database": "",
        "db_type": ""
    })
    assert response.status_code == 400
    assert response.json == {"Error": "Incorrect Data"}

def test_delete_connection_unknown(client):
    """
    Test the API endpoint for deleting a connection that does not exist.

    This test sends a DELETE request to the '/api/delete_connection/{connection_id}' endpoint
    with a connection_id that is not in the system. It asserts that the response status
    code is 404 and the response JSON contains an error message indicating that the
    connection was not found.
    """
    connection_id = 1
    response = client.delete(f'/api/delete_connection/{connection_id}')
    assert response.status_code == 404
    assert response.json == {'Error': "Connection not found"}

def test_delete_connection(client):
    """
    Test the API endpoint for successfully deleting an existing connection.

    This test sends a DELETE request to the '/api/delete_connection/{connection_id}' endpoint
    with a valid connection_id. It asserts that the response status code is 200 and
    the response JSON contains a message indicating that the connection was deleted successfully.
    """
    connection_id = "test"
    response = client.delete(f'/api/delete_connection/{connection_id}')
    assert response.status_code == 200
    assert response.json == {'Message': "Connection deleted successfully!"}
