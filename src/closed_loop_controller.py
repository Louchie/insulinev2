class ClosedLoopController:
    def __init__(self, pump, cgm, target_glucose=100):
        self.pump = pump
        self.cgm = cgm
        self.target_glucose = target_glucose

    def adjust_basal_rate(self, current_glucose):
        # Ajuster la délivrance basale en fonction de la glycémie
        if current_glucose > self.target_glucose:
            bolus_correction = self.pump.calculate_correction_bolus(current_glucose, self.target_glucose)
            return bolus_correction
        return 0

    def control_loop(self, patient):
        # Boucle de contrôle pour ajuster les doses d'insuline
        glucose = self.cgm.measure_glucose(patient)
        adjustment = self.adjust_basal_rate(glucose)
        if adjustment > 0:
            patient.update_glucose_level(adjustment, 0)
