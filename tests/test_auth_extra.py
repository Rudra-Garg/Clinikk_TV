def test_login_incorrect_password(client):
    # Register a user first.
    user_data = {
        "email": "failuser@example.com",
        "password": "correctpassword"
    }
    register_response = client.post("/auth/register", json=user_data)
    assert register_response.status_code == 200, register_response.text

    # Attempt login with an incorrect password.
    login_data = {
        "email": "failuser@example.com",
        "password": "wrongpassword"
    }
    login_response = client.post("/auth/token", json=login_data)
    assert login_response.status_code == 401, login_response.text
    assert "Incorrect email or password" in login_response.json().get("detail", "")


def test_register_missing_field(client):
    # Try registering without the password field.
    incomplete_data = {
        "email": "incomplete@example.com"
    }
    response = client.post("/auth/register", json=incomplete_data)
    # Expect a 422 Unprocessable Entity due to missing required fields.
    assert response.status_code == 422
