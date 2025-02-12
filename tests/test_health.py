def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200, response.text
    assert response.json() == {"status": "healthy"}


def test_detailed_health_check(client):
    response = client.get("/health/detailed")
    # Depending on your implementation the detailed check may return various keys.
    # Here we simply ensure we get a JSON response with status code 200.
    assert response.status_code == 200, response.text
    data = response.json()
    assert isinstance(data, dict)
