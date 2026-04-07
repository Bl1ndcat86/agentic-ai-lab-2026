from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from governor.aam_engine import AAM_Engine
from governor.aam_config import PROFILES

app = FastAPI(title="GMD AAM Hub - Audit Edition")

class Transaction(BaseModel):
    task_id: str
    value: float
    criticality: float
    uncertainty: float

engine = AAM_Engine(PROFILES["FINANCE_DEPT"])

@app.post("/decide")
async def get_batch_decision(txns: List[Transaction]):
    audit_results = []
    total_savings = 0.0
    
    for txn in txns:
        decision, log = engine.decide(txn.task_id, txn.value, txn.criticality, txn.uncertainty)
        
        # Logic: If it's a "Fraud-like" risk and we restricted it, log 'Savings'
        if txn.uncertainty > 0.7 and "L4" not in decision:
            total_savings += txn.value
            
        audit_results.append({
            "ID": txn.task_id,
            "Autonomy_Level": decision,
            "Utility_Score": log["utility_score"],
            "Risk_Status": "Mitigated" if "L4" not in decision else "Autonomous"
        })
    
    # Return a summary 'Header' plus the 'Table'
    return {
        "summary": {
            "batch_size": len(txns),
            "est_risk_mitigated": f"${total_savings:,.2f}",
            "governance_mode": "Active"
        },
        "audit_table": audit_results
    }