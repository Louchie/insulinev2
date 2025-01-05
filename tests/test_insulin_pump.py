import pytest
from src.pump_config import PumpConfig  # Correctement importé
from src.insulin_pump import InsulinPump

def test_basal_insulin():
    config = PumpConfig(basal_rates=[0.8] * 24, insulin_to_carb_ratio=10, insulin_sensitivity_factor=30, max_bolus=10, modes={})
    pump = InsulinPump(config)
    assert pump.deliver_basal(0) == 0.8  # Taux basal à 00:00

def test_meal_bolus():
    config = PumpConfig(basal_rates=[0.8] * 24, insulin_to_carb_ratio=10, insulin_sensitivity_factor=30, max_bolus=10, modes={})
    pump = InsulinPump(config)
    assert pump.calculate_meal_bolus(60) == 6  # Calcul du bolus alimentaire

def test_correction_bolus():
    config = PumpConfig(basal_rates=[0.8] * 24, insulin_to_carb_ratio=10, insulin_sensitivity_factor=30, max_bolus=10, modes={})
    pump = InsulinPump(config)
    assert pump.calculate_correction_bolus(180, 120) == 2  # Bolus de correction

