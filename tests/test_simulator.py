import pytest
from src.simulator import Simulator
from src.insulin_pump import InsulinPump
from src.patient import Patient
from src.cgm import CGM
from src.closed_loop_controller import ClosedLoopController
from src.pump_config import PumpConfig

def test_simulation():
    config = PumpConfig(basal_rates=[0.8] * 24, insulin_to_carb_ratio=10, insulin_sensitivity_factor=30, max_bolus=10, modes={})
    pump = InsulinPump(config)
    patient = Patient(initial_glucose=120, carb_sensitivity=5, insulin_sensitivity=30)
    cgm = CGM(measurement_interval=5)
    controller = ClosedLoopController(pump, cgm, target_glucose=100)
    simulator = Simulator(patient, pump, cgm, controller, duration=24)
    simulator.run_simulation()
    assert True  # Simulation se termine sans erreurs
