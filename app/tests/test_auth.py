from fastapi.testclient import TestClient
from app.main import app

# Create a virtual client to simulate HTTP network requests
client = TestClient(app)

def test_read_root():
    """Confirms that the home page entrypoint welcome route works smoothly."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"

def test_user_registration_flow():
    """Validates that a new user profile registers correctly."""
    # Simulate filling out the form elements on the dashboard
    payload = {
        "username": "test_runner_99",
        "password": "SecurePassword123"
    }
    response = client.post("/auth/register", data=payload)
    
    assert response.status_code == 200
    assert "successfully registered" in response.json()["message"]
