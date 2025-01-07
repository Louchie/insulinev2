from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict

# Modèles Pydantic
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
    value: float

class CGMRequest(BaseModel):
    glucose_level: float

class AlertRequest(BaseModel):
    glucose_level: float
    critical_limit: float

class ModeConfig(BaseModel):
    mode_name: str
    parameters: Dict[str, float]

# Simulation des classes
class InsulinPump:
    def __init__(self, config):
        self.config = config
        self.glucose_history = []  # Stocke les mesures de glycémie
        self.dose_history = []  # Stocke les doses administrées

    def deliver_basal(self, hour):
        if 0 <= hour < len(self.config["basal_rates"]):
            return self.config["basal_rates"][hour]
        raise HTTPException(status_code=400, detail="Heure invalide pour le taux basal")

    def calculate_meal_bolus(self, carbs):
        return carbs / self.config["insulin_to_carb_ratio"]

    def calculate_correction_bolus(self, glucose_level, target_glucose):
        if glucose_level <= target_glucose:
            return 0
        excess_glucose = glucose_level - target_glucose
        return excess_glucose / self.config["insulin_sensitivity_factor"]

    def configure(self, config: ConfigRequest):
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

    def measure_glucose(self, glucose_level):
        self.glucose_history.append(glucose_level)
        return glucose_level

    def get_glucose_history(self):
        return self.glucose_history

    def record_dose(self, dose, dose_type):
        self.dose_history.append({"dose": dose, "type": dose_type})

    def get_dose_history(self):
        return self.dose_history

# Configuration initiale
pump_config = {
    "basal_rates": [0.8] * 24,
    "insulin_to_carb_ratio": 10.0,
    "insulin_sensitivity_factor": 50.0,
    "max_bolus": 10.0,
    "modes": {
        "day": {"active": True, "start_time": "06:00", "end_time": "22:00", "basal_rate_modifier": 1.0},
        "night": {"active": True, "start_time": "22:00", "end_time": "06:00", "basal_rate_modifier": 0.8},
    }
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
        pump.record_dose(dose, "basal")
        return {"message": f"Insuline basale administrée : {dose} U", "basal_dose": dose}
    elif request.type == "bolus":
        dose = pump.calculate_meal_bolus(request.value)
        if dose > pump.config["max_bolus"]:
            raise HTTPException(status_code=400, detail="Bolus dépasse la limite maximale")
        pump.record_dose(dose, "bolus")
        return {"message": f"Bolus alimentaire administré : {dose} U", "bolus_dose": dose}
    else:
        raise HTTPException(status_code=400, detail="Type d'insuline invalide")

@app.post("/cgm/correction")
def correction_bolus(cgm_request: CGMRequest):
    target_glucose = 100.0
    correction_dose = pump.calculate_correction_bolus(cgm_request.glucose_level, target_glucose)
    if correction_dose > pump.config["max_bolus"]:
        raise HTTPException(status_code=400, detail="Bolus de correction dépasse la limite maximale")
    pump.record_dose(correction_dose, "correction")
    return {"message": f"Bolus de correction administré : {correction_dose} U", "correction_bolus": correction_dose}

@app.post("/cgm/measure")
def measure_glucose(cgm_request: CGMRequest):
    glucose = pump.measure_glucose(cgm_request.glucose_level)
    return {"message": f"Glycémie mesurée avec succès : {glucose} mg/dL", "measured_glucose": glucose}

@app.get("/cgm/history")
def get_glucose_history():
    history = pump.get_glucose_history()
    if not history:
        return {"message": "Aucun historique de glycémie disponible", "glucose_history": []}
    return {"message": "Historique de glycémie récupéré avec succès", "glucose_history": history}

@app.get("/pump/dose-history")
def get_dose_history():
    dose_history = pump.get_dose_history()
    if not dose_history:
        return {"message": "Aucun historique de dose disponible", "dose_history": []}
    return {"message": "Historique des doses récupéré avec succès", "dose_history": dose_history}

@app.post("/alerts")
def alert_user(alert_request: AlertRequest):
    if alert_request.glucose_level > alert_request.critical_limit:
        return {
            "message": f"Alerte critique : glycémie de {alert_request.glucose_level} mg/dL dépasse la limite critique ({alert_request.critical_limit} mg/dL)",
            "status": "critical"
        }
    return {"message": "Aucune alerte détectée", "status": "normal"}

@app.post("/pump/mode")
def configure_mode(mode_config: ModeConfig):
    pump.config["modes"][mode_config.mode_name] = mode_config.parameters
    return {"message": f"Mode '{mode_config.mode_name}' configuré avec succès"}

@app.get("/pump/config")
def get_pump_config():
    return {"message": "Configuration actuelle de la pompe récupérée", "config": pump.config}
