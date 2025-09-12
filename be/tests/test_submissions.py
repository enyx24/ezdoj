from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_submission(client):
    response = client.post("/submissions/")
    assert response.status_code == 200
    assert "id" in response.json()
