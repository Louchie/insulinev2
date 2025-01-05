import pytest
from src.closed_loop_controller import ClosedLoopController
from src.insulin_pump import InsulinPump
from src.patient import Patient
from src.pump_config import PumpConfig
from src.cgm import CGM

def test_adjust_basal_rate():
    config = PumpConfig(basal_rates=[0.8] * 24, insulin_to_carb_ratio=10, insulin_sensitivity_factor=30, max_bolus=10, modes={})
    pump = InsulinPump(config)
    
    patient = Patient(initial_glucose=150, carb_sensitivity=5, insulin_sensitivity=30)
    cgm = CGM()
    
    controller = ClosedLoopController(pump, cgm, target_glucose=100)
    
    adjustment = controller.adjust_basal_rate(patient.glucose_level)

    # Utiliser une tolérance pour la comparaison
    assert abs(adjustment - 1.67) < 0.01  # Vérifie que la différence est inférieure à 0.01
