import pandas as pd
import json
import requests

URL_BASE = "https://agentic-ai-lab-2026-1054065165765.us-central1.run.app/decide"

def run_scenario(escenario, file_path):
    print(f"--- 🚀 Ejecutando Escenario: {escenario.upper()} ---")
    payload = []

    if escenario == "legal":
        df = pd.read_csv(file_path)
        for i, row in df.head(5).iterrows():
            payload.append({
                "task_id": f"LAW-{i}", "value": 15000.0, "criticality": 4000.0,
                "metadata": {"clausula": str(row.iloc[1])}
            })

    elif escenario == "conocimiento":
        with open(file_path, 'r') as f:
            data = json.load(f)
            for i, item in enumerate(data[:5]):
                payload.append({
                    "task_id": f"HALU-{i}", "value": 1.0, "criticality": 500.0,
                    "metadata": {"pregunta": item['question'], "respuesta": item['answer']}
                })

    elif escenario == "cafeteria":
        df = pd.read_csv(file_path)
        for i, row in df.head(5).iterrows():
            payload.append({
                "task_id": f"COFFEE-{i}", "value": float(row.get('money', 5.0)), "criticality": 80.0,
                "metadata": {"producto": row.get('coffee_name', 'Desconocido')}
            })

    try:
        res = requests.post(f"{URL_BASE}/{escenario}", json=payload)
        print(json.dumps(res.json(), indent=2))
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    # Ejemplo:
    run_scenario("legal", "data/master_clauses.csv")