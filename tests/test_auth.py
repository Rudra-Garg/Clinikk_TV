def test_register_user(client):
    user_data = {
        "email": "newuser@example.com",
        "password": "strongpassword123"
    }
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 200, response.text
    user = response.json()
    assert user["email"] == user_data["email"]
    assert "id" in user


def test_register_existing_user(client):
    user_data = {
        "email": "existinguser@example.com",
        "password": "password123"
    }
    # First registration attempt.
    response1 = client.post("/auth/register", json=user_data)
    assert response1.status_code == 200, response1.text
    # Second registration with the same email should fail.
    response2 = client.post("/auth/register", json=user_data)
    assert response2.status_code == 400, response2.text
    detail = response2.json().get("detail", "")
    assert detail == "Email already registered"


def test_login(client):
    # Register a user to later log in.
    user_data = {
        "email": "loginuser@example.com",
        "password": "mypassword"
    }
    register_response = client.post("/auth/register", json=user_data)
    assert register_response.status_code == 200, register_response.text

    login_data = {
        "email": user_data["email"],
        "password": user_data["password"]
    }
    response = client.post("/auth/token", json=login_data)
    assert response.status_code == 200, response.text
    token_data = response.json()
    assert "access_token" in token_data
    # Typically the token type is "bearer".
    assert token_data.get("token_type") == "bearer"
