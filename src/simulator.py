from fastapi import FastAPI

app = FastAPI()

class Simulator:
    def __init__(self, patient, pump, cgm, controller, duration=24):
        self.patient = patient
        self.pump = pump
        self.cgm = cgm
        self.controller = controller
        self.duration = duration

    def run_simulation(self):
        for hour in range(self.duration):
            print(f"---- Heure : {hour}:00 ----")
            basal = self.pump.deliver_basal(hour % 24)
            self.patient.update_glucose_level(basal, 0)
            self.controller.control_loop(self.patient)

    def log_data(self):
        # Enregistrer les données de simulation
        pass
