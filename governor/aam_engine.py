def calculate_utility(self, escenario, task_data):
    # Parámetros Base
    V = task_data.get('value', 0)
    Pe = task_data.get('uncertainty', 0.95) # Inferencia de la IA
    Cc = 5.0 # Costo de control fijo
    
    # 1. ESCENARIO: LEGAL (Aversión Extrema)
    if escenario == "LEGAL":
        Ce = 50.0  # Tu parámetro de doctorado
    
    # 2. ESCENARIO: FINANCE (Fraude y Montos)
    elif escenario == "FINANCE":
        Ce = 20.0
        if V > 10000 or "fraude" in task_data.get('ai_analysis', '').lower():
            return "L1 - Alerta de Riesgo Financiero", 0

    # 3. ESCENARIO: CAFE (Inventario)
    elif escenario == "CAFE":
        Ce = 10.0
        stock = task_data.get('metadata', {}).get('stock', 2.0)
        if stock < 1.5:
            return "L4 - Reposición Crítica", V # Adaptabilidad detectada

    # 4. ESCENARIO: CHOCOLATE (Mayoreo)
    elif escenario == "CHOCOLATE":
        Ce = 15.0
        unidades = task_data.get('metadata', {}).get('unidades', 0)
        if unidades > 300:
            return "L1 - Pedido Masivo (Alerta)", V - Cc
        elif 22 <= unidades <= 193:
            return "L4 - Pedido Estándar (Aprobado)", V - Cc

    # Lógica General (AAM Standard)
    utility = V - Cc - (Pe * Ce)
    # ... resto de la lógica de niveles Lx ...