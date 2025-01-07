from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict

# Modèles Pydantic pour les requêtes et réponses
class BasalRate(BaseModel):
    hour: int
    rate: float

class ConfigRequest(BaseModel):
    basal_rates: Optional[List[BasalRate]] = None
    insulin_to_carb_ratio: Optional[float] = None
    insulin_sensitivity_factor: Optional[float] = None
    max_bolus: Optional[float] = None
    modes: Optional[Dict[str, Dict[str, float]]] = None

class DeliverInsulinRequest(BaseModel):
    type: str
    value: float  # Peut être des glucides (pour bolus alimentaire) ou une heure (pour basale)

class CGMRequest(BaseModel):
    glucose_level: float  # Mesure de glycémie

# Simulation des classes
class InsulinPump:
    def __init__(self, config):
        self.config = config

    def deliver_basal(self, hour):
        try:
            return self.config["basal_rates"][hour]
        except IndexError:
            raise HTTPException(status_code=400, detail="Heure invalide pour le taux basal")

    def calculate_meal_bolus(self, carbs):
        return carbs / self.config["insulin_to_carb_ratio"]

    def calculate_correction_bolus(self, glucose_level, target_glucose):
        if glucose_level <= target_glucose:
            return 0
        excess_glucose = glucose_level - target_glucose
        return excess_glucose / self.config["insulin_sensitivity_factor"]

    def configure(self, config: ConfigRequest):
        # Importer la classe PumpConfig uniquement lorsque nécessaire pour éviter l'importation circulaire
        from src.pump_config import PumpConfig

        # Créer une instance de PumpConfig et mettre à jour la configuration de la pompe
        if config.basal_rates:
            self.config["basal_rates"] = [br.rate for br in sorted(config.basal_rates, key=lambda x: x.hour)]
        if config.insulin_to_carb_ratio:
            self.config["insulin_to_carb_ratio"] = config.insulin_to_carb_ratio
        if config.insulin_sensitivity_factor:
            self.config["insulin_sensitivity_factor"] = config.insulin_sensitivity_factor
        if config.max_bolus:
            self.config["max_bolus"] = config.max_bolus
        if config.modes:
            self.config["modes"].update(config.modes)

# Configuration initiale
pump_config = {
    "basal_rates": [0.8] * 24,
    "insulin_to_carb_ratio": 10,
    "insulin_sensitivity_factor": 30,
    "max_bolus": 10,
    "modes": {}
}
pump = InsulinPump(config=pump_config)

# Création de l'application FastAPI
app = FastAPI()

@app.put("/pump/configure")
def configure_pump(config: ConfigRequest):
    pump.configure(config)
    return {"message": "Configuration mise à jour avec succès"}

@app.post("/insulin/deliver")
def deliver_insulin(request: DeliverInsulinRequest):
    if request.type == "basal":
        dose = pump.deliver_basal(hour=int(request.value))
        return {"basal_dose": dose}
    elif request.type == "bolus":
        dose = pump.calculate_meal_bolus(request.value)
        if dose > pump.config["max_bolus"]:
            raise HTTPException(status_code=400, detail="Bolus dépasse la limite maximale")
        return {"bolus_dose": dose}
    else:
        raise HTTPException(status_code=400, detail="Type d'insuline invalide")

@app.post("/cgm/correction")
def correction_bolus(cgm_request: CGMRequest):
    target_glucose = 100  # Par défaut
    correction_dose = pump.calculate_correction_bolus(cgm_request.glucose_level, target_glucose)
    if correction_dose > pump.config["max_bolus"]:
        raise HTTPException(status_code=400, detail="Bolus de correction dépasse la limite maximale")
    return {"correction_bolus": correction_dose}

@app.get("/pump/config")
def get_pump_config():
    return pump.config
