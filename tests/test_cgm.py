# tests/test_cgm.py
import pytest
from src.cgm import CGM
from src.patient import Patient

def test_measure_glucose():
    # Créer un patient avec une glycémie initiale de 120 mg/dL
    patient = Patient(initial_glucose=120, carb_sensitivity=5, insulin_sensitivity=30)
    
    # Créer un CGM
    cgm = CGM(measurement_interval=5)
    
    # Mesurer la glycémie et vérifier qu'elle est correcte
    measured_glucose = cgm.measure_glucose(patient)
    assert measured_glucose == 120  # La glycémie mesurée doit correspondre à la glycémie initiale du patient
