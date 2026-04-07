from fastapi import FastAPI
import os
# Change relative imports to absolute imports
from governor.aam_engine import AAM_Engine
from governor.aam_config import PROFILES

app = FastAPI(title="GMD AAM Hub")

# Initialize the engine
engine = AAM_Engine(PROFILES["FINANCE_DEPT"])

@app.get("/")
def health_check():
    return {"status": "online", "mechanism": "AAM-GMD"}

@app.post("/decide")
async def get_decision(task_id: str, value: float, criticality: float, uncertainty: float):
    decision, log = engine.decide(task_id, value, criticality, uncertainty)
    return {"decision": decision, "audit_trail": log}