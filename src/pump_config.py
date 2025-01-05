from fastapi import FastAPI

app = FastAPI()

class PumpConfig:
    def __init__(self, basal_rates, insulin_to_carb_ratio, insulin_sensitivity_factor, max_bolus, modes):
        self.basal_rates = basal_rates  # Liste des taux basaux par heure
        self.insulin_to_carb_ratio = insulin_to_carb_ratio  # Ratio insuline/glucides (ICR)
        self.insulin_sensitivity_factor = insulin_sensitivity_factor  # Facteur de sensibilité à l'insuline (ISF)
        self.max_bolus = max_bolus  # Dose maximale de bolus
        self.modes = modes  # Modes personnalisables (ex : jour/nuit)

    def validate(self):
        # Valider la configuration
        if not (0 < self.insulin_to_carb_ratio <= 20):
            raise ValueError("Ratio insuline/glucides invalide.")
        if not (0 < self.insulin_sensitivity_factor <= 100):
            raise ValueError("Facteur de sensibilité invalide.")
        if not (0 < self.max_bolus <= 10):  # Vérification de la dose maximale de bolus
            raise ValueError("Dose maximale de bolus invalide.")
        return True
