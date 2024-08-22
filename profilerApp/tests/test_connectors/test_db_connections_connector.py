def test_get_connections(client):
    """
    Test the get_connections function.
    """
    response = client.get("/api/get_connections")
    assert response.status_code == 200
    assert response.json == { \
        "Answer": [{
            "connection_id": "conn123",
            "server": "testServer",
            "port": 1234,
            "username": "testUser",
            "database": "testDB",
            "db_type": "postgres",
        }]
    }

def test_add_connection(client):
    """
    Test the add_connection function.
    """
    response = client.post("/api/add_connection", json={
        "connection_id": "conn456",
        "server": "testServer",
        "port": 1234,
        "username": "testUser",
        "password": "test_password",
        "database": "testDB",
        "db_type": "postgres",
    })  
    assert response.status_code == 200
    assert response.json == {"Message":"Connection Added Succesfully!"}

def test_add_connection_existing(client):
    """
    Test the add_connection function.
    """
    response = client.post("/api/add_connection", json={
        "connection_id": "conn123",
        "server": "testServer",
        "port": 1234,
        "username": "testUser",
        "password": "test_password",
        "database": "testDB",
        "db_type": "postgres",
    })  
    assert response.status_code == 403
    assert response.json == {"Error": "Connection_id already exists"}


def test_add_connection_invalid(client):
    """
    Test the add_connection function.
    """
    response = client.post("/api/add_connection", json={
        "connection_id": "conn456",
        "server": "testServer",
        "port": 1234,
        "username": "testUser",
        "password": "test_password",
        "database": "testDB",
    })
    assert response.status_code == 400
    assert response.json == {"Error": "Incorrect Data"}

def delete_connection(client):
    """
    Test the delete_connection function.
    """
    response = client.delete("/api/delete_connection/conn123")
    assert response.status_code == 200
    assert response.json == {"Message":"Connection Deleted Succesfully!"}


def delete_wrong_connection(client):
    """
    Test the delete_connection function.
    """
    response = client.delete("/api/delete_connection/conn456")
    assert response.status_code == 403
    assert response.json == {"Error": "Connection_id does not exist"}