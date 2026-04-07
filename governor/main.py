from fastapi import FastAPI
from pydantic import BaseModel
from typing import List  # <--- Add this import
from governor.aam_engine import AAM_Engine
from governor.aam_config import PROFILES

app = FastAPI(title="GMD AAM Hub - Batch Edition")

class Transaction(BaseModel):
    task_id: str
    value: float
    criticality: float
    uncertainty: float

engine = AAM_Engine(PROFILES["FINANCE_DEPT"])

@app.get("/")
def health_check():
    return {"status": "online", "mode": "batch_enabled"}

# Updated to handle List[Transaction]
@app.post("/decide")
async def get_decision(txns: List[Transaction]):
    batch_results = []
    for txn in txns:
        decision, log = engine.decide(txn.task_id, txn.value, txn.criticality, txn.uncertainty)
        batch_results.append({
            "task_id": txn.task_id,
            "decision": decision,
            "audit_trail": log
        })
    return batch_results