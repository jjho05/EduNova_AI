import pytest

def test_register_user(client):
    response = client.post(
        "/api/auth/register",
        json={
            "email": "test_user@test.com",
            "password": "testpassword123",
            "first_name": "Test",
            "last_name": "User",
            "role": "student"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["email"] == "test_user@test.com"

def test_login_user(client):
    # Ensure user exists (registered in previous test using module scope)
    response = client.post(
        "/api/auth/login",
        data={
            "username": "test_user@test.com",
            "password": "testpassword123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
