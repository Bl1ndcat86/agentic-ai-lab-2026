from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from google import genai
import os
from governor.aam_engine import AAM_Engine
from governor.aam_config import PROFILES

app = FastAPI(title="GMD Judicial Council - PhD Dashboard")

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MANDATOS = {
    "financiero": "Auditor Forense. Detecta patrones de lavado y drenaje.",
    "legal": "Director Legal. Busca trampas de responsabilidad civil y cláusulas adversas.",
    "conocimiento": "Verificador de Datos. Detecta alucinaciones y deriva lógica.",
    "chocolate": "Controller de Inventario. Optimiza stock ante mermas y volatilidad.",
    "cafeteria": "Especialista en Suministros. Asegura ética en el grano y comercio justo."
}

PROFILE_MAP = {
    "financiero": "FINANCE_DEPT",
    "legal": "LEGAL_DEPT",
    "conocimiento": "HALUEVAL_DEPT",
    "chocolate": "INVENTORY_DEPT",
    "cafeteria": "SUPPLY_DEPT"
}

class Task(BaseModel):
    task_id: str
    value: float
    criticality: float
    metadata: Optional[dict] = None 

@app.post("/decide/{escenario}")
async def judicial_council(escenario: str, tasks: List[Task]):
    profile_key = PROFILE_MAP.get(escenario, "FINANCE_DEPT")
    engine = AAM_Engine(PROFILES.get(profile_key))
    mandato = MANDATOS.get(escenario, "Auditor General")
    
    audit_table = []
    
    for task in tasks:
        # --- PASO ESTOCÁSTICO: Inferencia de Gemini ---
        contexto = task.metadata if task.metadata else "No metadata"
        prompt = f"""
        Escenario: {escenario.upper()} | Mandato: {mandato}
        Analiza esta metadata: {contexto}
        Valor: ${task.value} | Criticidad: {task.criticality}
        
        Responde ESTRICTAMENTE en este formato:
        REASONING: [Tu análisis forense en 1 frase] | UNCERTAINTY: [0.0-1.0]
        """
        
        try:
            response = client.models.generate_content(model='gemini-3-flash-preview', contents=prompt)
            full_text = response.text
            ai_reasoning = full_text.split("REASONING:")[1].split("|")[0].strip()
            ai_uncertainty = float(full_text.split("UNCERTAINTY:")[1].strip())
        except:
            ai_reasoning = "Falla de Inferencia: El Gobernador asume riesgo máximo por seguridad."
            ai_uncertainty = 0.95

        # --- PASO DETERMINÍSTICO: El Mecanismo AAM ---
        decision, log = engine.decide(task.task_id, task.value, task.criticality, ai_uncertainty)
        
        audit_table.append({
            "ID": task.task_id,
            "Escenario": escenario.upper(),
            "Veredicto": decision,
            "Revision_Judicial": {
                "Analisis_IA": ai_reasoning,
                "Incertidumbre_IA": f"{ai_uncertainty:.2%}",
                "Utilidad_AAM": round(log["utility_score"], 2)
            },
            "Accion": "BLOQUEO" if "L0" in decision else "AUTONOMIA",
            "Impacto": f"${task.value:,.2f}"
        })
        
    return audit_table