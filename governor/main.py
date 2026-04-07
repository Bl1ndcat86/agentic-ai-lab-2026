from fastapi import FastAPI
# Absolute imports are safer for Cloud Run deployment
from governor.aam_engine import AAM_Engine
from governor.aam_config import PROFILES

app = FastAPI(title="GMD AAM Hub")

# Initialize the engine for Finance (or your preferred dept)
engine = AAM_Engine(PROFILES["FINANCE_DEPT"])

@app.get("/")
def health_check():
    return {"status": "online", "mechanism": "AAM-GMD"}

@app.post("/decide")
async def get_decision(task_id: str, value: float, criticality: float, uncertainty: float):
    # This executes your core AAM logic [cite: 93]
    decision, log = engine.decide(task_id, value, criticality, uncertainty)
    return {"decision": decision, "audit_trail": log}