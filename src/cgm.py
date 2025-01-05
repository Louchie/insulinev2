from fastapi import FastAPI

app = FastAPI()

class CGM:
    def __init__(self, measurement_interval=5):
        self.measurement_interval = measurement_interval
        self.current_glucose = None

    def measure_glucose(self, patient):
        # Simuler une mesure de glycémie
        self.current_glucose = patient.glucose_level
        print(f"Glycémie mesurée : {self.current_glucose} mg/dL")
        return self.current_glucose
