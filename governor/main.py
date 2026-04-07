from fastapi import FastAPI
from .aam_engine import AAM_Engine
from .aam_config import PROFILES

app = FastAPI(title="GMD AAM Hub")
engine = AAM_Engine(PROFILES["FINANCE_DEPT"]) # Default profile

@app.post("/decide")
async def get_governance_decision(task_id: str, V: float, C: float, Um: float):
    # AAM assigns dynamic autonomy Lx based on uncertainty Um
    decision, log = engine.decide(task_id, V, C, Um)
    return {"level": decision, "audit_trail": log}