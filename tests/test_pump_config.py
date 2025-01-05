import pytest
from src.pump_config import PumpConfig

def test_invalid_max_bolus():
    # Créer une configuration avec une dose maximale de bolus invalide
    config = PumpConfig(basal_rates=[0.8] * 24, insulin_to_carb_ratio=10, insulin_sensitivity_factor=30, max_bolus=15, modes={})

    # Vérifier que la validation échoue
    with pytest.raises(ValueError) as excinfo:
        config.validate()
    assert "Dose maximale de bolus invalide." in str(excinfo.value)
