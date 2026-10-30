from fastapi.testclient import TestClient
from main_api import app

# Create a fake client to talk to our app
client = TestClient(app)

def test_register_user():
    # Fake data to send
    payload = {
        "name": "PytestUser",
        "age": 99,
        "password": "testpassword123"
    }
    # Send a POST request to /register
    response = client.post("/register", json=payload)
    
    # Check that the API returned a 200 OK status
    assert response.status_code == 200
    assert "user_id" in response.json()

def test_login_user():
    # Send form data (not JSON) to /login
    login_data = {
        "username": "PytestUser",
        "password": "testpassword123"
    }
    response = client.post("/login", data=login_data)
    
    # Check that login worked and returned a token
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_wrong_password():
    login_data = {
        "username": "PytestUser",
        "password": "wrongpassword"
    }
    response = client.post("/login", data=login_data)
    
    # Check that it correctly rejects the wrong password
    assert response.status_code == 400