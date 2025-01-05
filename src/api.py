from fastapi import FastAPI
from src.cgm import CGM
from src.insulin_pump import InsulinPump
from src.patient import Patient

app = FastAPI()

# Exemple d'initialisation
cgm = CGM(measurement_interval=5)
pump_config = {
    "basal_rates": [0.8] * 24,
    "insulin_to_carb_ratio": 10,
    "insulin_sensitivity_factor": 30,
    "max_bolus": 10,
    "modes": {}
}
pump = InsulinPump(config=pump_config)
patient = Patient(initial_glucose=120, carb_sensitivity=5, insulin_sensitivity=30)

@app.get("/glucose/current")
def get_glucose():
    glucose = cgm.measure_glucose(patient)
    return {"current_glucose": glucose}

@app.post("/insulin/deliver")
def deliver_insulin(type: str, value: float):
    if type == "basal":
        dose = pump.deliver_basal(hour=int(value))
        return {"basal_dose": dose}
    elif type == "bolus":
        dose = pump.calculate_meal_bolus(value)
        return {"bolus_dose": dose}
    else:
        return {"error": "Invalid insulin type"}

@app.post("/patient/add_carbs")
def add_carbs(carbs: float):
    patient.add_carbs(carbs)
    return {"new_glucose_level": patient.glucose_level}
