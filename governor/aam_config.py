# Mechanism Design Parameters for different Agentic Contexts
PROFILES = {
    "FINANCE_DEPT": {
        "control_cost_coefficient": 0.15,  # Cc: Cost of human oversight
        "error_cost_multiplier": 5.0,      # Ce: Impact of a mistake
        "utility_threshold": 0.65          # Min utility for L4 autonomy
    },
    "PRODUCT_OPS": {
        "control_cost_coefficient": 0.05, 
        "error_cost_multiplier": 1.5,
        "utility_threshold": 0.40
    },
    "AI_RESEARCH_LAB": {
        "control_cost_coefficient": 0.02,
        "error_cost_multiplier": 1.0,
        "utility_threshold": 0.20
    }
}