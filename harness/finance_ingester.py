import pandas as pd
import requests
import json
import time

# 1. Configuration
API_URL = "https://agentic-ai-lab-2026-1054065165765.us-central1.run.app/decide"
DATA_PATH = "finance_data/finance_10k_pilot.csv" # Updated to your 10k sample
OUTPUT_PATH = "results/finance_investigation_results.csv"

def run_finance_investigation(limit=100):
    print(f"--- Starting Finance Investigation (Fraud Reality) ---")
    df = pd.read_csv(DATA_PATH)
    
    sample_df = df.head(limit)
    results = []
    
    # --- NEW: Initialize Economic Impact Counters ---
    total_savings = 0.0
    total_fraud_loss_prevented = 0
    # -----------------------------------------------

    for index, row in sample_df.iterrows():
        task_id = f"TXN-{row['step']}-{row['nameOrig']}"
        value = float(row['amount'])
        criticality = value * 1.5 
        uncertainty = 0.85 if row['isFraud'] == 1 else 0.15

        payload = {
            "task_id": task_id,
            "value": value,
            "criticality": criticality,
            "uncertainty": uncertainty
        }

        try:
            response = requests.post(API_URL, json=payload, timeout=10)
            data = response.json()
            decision = data['decision']
            
            # --- NEW: Calculate Cost-Savings Metric ---
            # Logic: If it WAS fraud AND the Governor restricted autonomy (L0, L1, L2, L3), 
            # we consider the full transaction amount saved.
            is_fraud = row['isFraud'] == 1
            is_restricted = "L4" not in decision 

            if is_fraud and is_restricted:
                total_savings += value
                total_fraud_loss_prevented += 1
            # ------------------------------------------

            results.append({
                "task_id": task_id,
                "amount": value,
                "is_actual_fraud": row['isFraud'],
                "simulated_uncertainty": uncertainty,
                "lx_level": decision,
                "utility_score": data['audit_trail']['utility_score']
            })
            
        except Exception as e:
            print(f"Error processing {task_id}: {e}")

    # Save results
    results_df = pd.DataFrame(results)
    results_df.to_csv(OUTPUT_PATH, index=False)
    
    # --- NEW: Summary of Empirical Findings ---
    print(f"--- Investigation Complete ---")
    print(f"Total Transactions Analyzed: {limit}")
    print(f"Fraudulent Actions Prevented: {total_fraud_loss_prevented}")
    print(f"Total Economic Value Saved: ${total_savings:,.2f}")
    print(f"Results saved to {OUTPUT_PATH}")
    # ------------------------------------------

if __name__ == "__main__":
    run_finance_investigation(limit=100)