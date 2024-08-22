def test_get_all_files(client):
    # Test the get_all_files endpoint
    response = client.get('/api/get_all_files')
    assert response.status_code == 200
    assert response.json == {
        "Answer": [
            "test_data.csv"
        ]
    }
