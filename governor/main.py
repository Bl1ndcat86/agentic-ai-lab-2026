from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from governor.aam_engine import AAM_Engine
from governor.aam_config import PROFILES

app = FastAPI(title="GMD AAM Hub - PhD Dashboard")

class Transaction(BaseModel):
    task_id: str
    value: float
    criticality: float
    uncertainty: float
    reasoning: str # Accept the thinking from the Agent

engine = AAM_Engine(PROFILES["FINANCE_DEPT"])

@app.post("/decide", response_model=List[dict])
async def get_batch_decision(txns: List[Transaction]):
    audit_table = []
    for txn in txns:
        decision, log = engine.decide(txn.task_id, txn.value, txn.criticality, txn.uncertainty)
        
        # This structure tells Swagger how to build the "Table"
        audit_table.append({
            "ID": txn.task_id,
            "Lx_Level": decision,
            "Utility": round(log["utility_score"], 2),
            "Risk_Mitigated": "✅ YES" if "L4" not in decision else "🚀 NO",
            "Gemini_Reasoning": txn.reasoning,
            "Value": f"${txn.value:,.2f}"
        })
    return audit_table