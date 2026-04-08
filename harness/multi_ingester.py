import requests
import json
import pandas as pd
import os
from datetime import datetime

class MultiIngester:
    def __init__(self, base_url="http://127.0.0.1:8080"):
        self.base_url = base_url
        self.results_dir = "thesis_results"
        os.makedirs(self.results_dir, exist_ok=True)

    def run_experiment(self, escenario, file_path, batch_size=100):
        """
        Procesa un escenario específico (LEGAL, FINANCE, CAFE, CHOCOLATE)
        """
        print(f"🔬 Iniciando Experimento GMD: {escenario}")
        endpoint = f"{self.base_url}/decide/{escenario.lower()}"
        
        with open(file_path, 'r') as f:
            tasks = json.load(f)

        all_results = []
        
        for i in range(0, len(tasks), batch_size):
            batch = tasks[i:i + batch_size]
            print(f"🚀 Procesando lote {i//batch_size + 1} de {len(tasks)//batch_size + 1}...")
            
            try:
                response = requests.post(endpoint, json=batch, timeout=60)
                if response.status_code == 200:
                    all_results.extend(response.json())
                else:
                    print(f"❌ Error en lote: {response.status_code}")
            except Exception as e:
                print(f"⚠️ Fallo de conexión: {e}")

        # Guardar evidencia para el artículo correspondiente
        df = pd.DataFrame(all_results)
        filename = f"{self.results_dir}/{escenario}_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
        df.to_csv(filename, index=False)
        print(f"✅ Datos guardados en: {filename}\n")
        return df

# Ejemplo de ejecución para tus artículos:
# ingester = MultiIngester()
# ingester.run_experiment("FINANCE", "data/10k_transacciones.json")
# ingester.run_experiment("LEGAL", "data/contratos_cuad.json")