class AAM_Engine:
    def __init__(self, profile):
        self.Cc = profile["Cc"]
        self.Ce_factor = profile["Ce_factor"]
        self.threshold = profile["threshold"]

    def decide(self, task_id, value, criticality, uncertainty):
        # Cc: Costo de Control
        # Ce: Costo del Error (Criticidad * Factor del perfil)
        # Pe: Incertidumbre (Proporcionada por Gemini)
        
        Ce = criticality * self.Ce_factor
        utility = value - self.Cc - (uncertainty * Ce)
        
        if utility > self.threshold:
            decision = "L4 - Audited Autonomy (Full Execution)"
        elif utility > 0:
            decision = "L1 - Human-in-the-loop (Review Required)"
        else:
            decision = "L0 - No Autonomy (Task Rejected/Hard Block)"
            
        return decision, {"utility_score": utility, "Pe": uncertainty}