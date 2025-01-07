from fastapi import FastAPI

app = FastAPI()

class Patient:
    def __init__(self, initial_glucose, carb_sensitivity, insulin_sensitivity):
        self.initial_glucose = initial_glucose
        self.glucose_level = initial_glucose
        self.carb_sensitivity = carb_sensitivity
        self.insulin_sensitivity = insulin_sensitivity

    def update_glucose_level(self, insulin, carbs):
        delta_glucose_carbs = carbs * self.carb_sensitivity
        delta_glucose_insulin = -insulin * self.insulin_sensitivity
        self.glucose_level += delta_glucose_carbs + delta_glucose_insulin
        print(f"Nouvelle glycémie : {self.glucose_level} mg/dL")

    def add_carbs(self, carbs):
        print(f"Ajout de {carbs} g de glucides.")
        self.update_glucose_level(0, carbs)
