def test_wrong_endpoint(client):
    response = client.get('/api/not_existing_endpoint')
    assert response.status_code == 404
    assert response.json == {'message': 'Endpoint not found'}