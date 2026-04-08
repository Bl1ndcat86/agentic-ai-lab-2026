# Configuración de Perfiles para el Mecanismo AAM
PROFILES = {
    "FINANCE_DEPT": {
        "Cc": 0.01,         # Costo de Control (Bajo para transacciones masivas)
        "Ce_factor": 1.5,    # Factor de error (Pérdida directa del monto)
        "threshold": 500     # Umbral de utilidad para otorgar Autonomía L4
    },
    "LEGAL_DEPT": {
        "Cc": 0.05, 
        "Ce_factor": 10.0,   # Riesgo legal es carísimo (10x el valor del contrato)
        "threshold": 2000
    },
    "HALUEVAL_DEPT": {
        "Cc": 0.01, 
        "Ce_factor": 5.0,    # Alucinaciones en IA tienen alto costo reputacional
        "threshold": 100
    },
    "INVENTORY_DEPT": { # Chocolate
        "Cc": 0.02, 
        "Ce_factor": 1.2,    # Riesgo de merma física
        "threshold": 50
    },
    "SUPPLY_DEPT": { # Cafetería
        "Cc": 0.02, 
        "Ce_factor": 2.5,    # Riesgo ético y de calidad del grano
        "threshold": 150
    }
}