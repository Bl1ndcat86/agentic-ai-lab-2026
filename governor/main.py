from fastapi import FastAPI
from pydantic import BaseModel
from governor.aam_engine import AAM_Engine
from governor.aam_config import PROFILES

app = FastAPI(title="GMD AAM Hub")

# 1. Define the Transaction Model (This creates the 'Request Body' in Swagger)
class Transaction(BaseModel):
    task_id: str
    value: float
    criticality: float
    uncertainty: float

engine = AAM_Engine(PROFILES["FINANCE_DEPT"])

@app.get("/")
def health_check():
    return {"status": "online", "mechanism": "AAM-GMD"}

@app.post("/decide")
async def get_decision(txn: Transaction):
    # Pass the data from the txn object to the engine
    decision, log = engine.decide(txn.task_id, txn.value, txn.criticality, txn.uncertainty)
    return {"decision": decision, "audit_trail": log}