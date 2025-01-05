import pytest
from src.patient import Patient

def test_update_glucose_level():
    patient = Patient(initial_glucose=120, carb_sensitivity=5, insulin_sensitivity=30)
    patient.update_glucose_level(insulin=1, carbs=50)
    assert patient.glucose_level == 340  # Test de la mise à jour de la glycémie
