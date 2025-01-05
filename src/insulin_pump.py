from fastapi import FastAPI

app = FastAPI()

class InsulinPump:
    def __init__(self, config):
        self.config = config
        self.alarms = []

    def deliver_basal(self, hour):
        # Administration de l'insuline basale pour une heure donnée
        basal_rate = self.config.basal_rates[hour]
        print(f"Insuline basale délivrée : {basal_rate} U à l'heure {hour}")
        return basal_rate

    def calculate_meal_bolus(self, carbs):
        # Calcul du bolus alimentaire
        bolus = carbs / self.config.insulin_to_carb_ratio
        bolus = min(bolus, self.config.max_bolus)  # Limiter le bolus au maximum autorisé
        print(f"Bolus alimentaire calculé : {bolus} U pour {carbs} g de glucides")
        return bolus

    def calculate_correction_bolus(self, current_glucose, target_glucose):
        # Calcul du bolus de correction
        if current_glucose > target_glucose:
            correction_bolus = (current_glucose - target_glucose) / self.config.insulin_sensitivity_factor
            correction_bolus = min(correction_bolus, self.config.max_bolus)
            print(f"Bolus de correction : {correction_bolus} U pour ramener la glycémie à {target_glucose} mg/dL")
            return correction_bolus
        return 0

    def apply_configuration(self, new_config):
        # Appliquer une nouvelle configuration
        self.config = new_config
