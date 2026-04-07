from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from governor.aam_engine import AAM_Engine
from governor.aam_config import PROFILES

app = FastAPI(title="GMD AAM Hub - Audit Dashboard")

class Transaction(BaseModel):
    task_id: str
    value: float
    criticality: float
    uncertainty: float

# Initialize the Mechanism
engine = AAM_Engine(PROFILES["FINANCE_DEPT"])

@app.get("/")
def health_check():
    return {"status": "Active", "mechanism": "AAM-GMD"}

@app.post("/decide", response_model=List[dict])
async def get_batch_decision(txns: List[Transaction]):
    audit_table = []
    for txn in txns:
        decision, log = engine.decide(txn.task_id, txn.value, txn.criticality, txn.uncertainty)
        
        # Flatten the data for the Web UI table
        audit_table.append({
            "ID": txn.task_id,
            "Lx_Level": decision,
            "Utility": log["utility_score"],
            "Risk_Mitigated": "✅ YES" if "L4" not in decision else "🚀 NO",
            "Principal_Value": txn.value
        })
    return audit_table