from fastapi.testclient import TestClient
from src.api import app

client = TestClient(app)

def test_get_glucose():
    response = client.get("/glucose/current")
    assert response.status_code == 200
    assert "current_glucose" in response.json()

def test_deliver_insulin_basal():
    response = client.post("/insulin/deliver", json={"type": "basal", "value": 1})
    print(response.status_code)  # Affiche le code de statut
    print(response.json())  # Affiche le corps de la réponse
    # assert response.status_code == 200
    # assert "basal_dose" in response.json()
