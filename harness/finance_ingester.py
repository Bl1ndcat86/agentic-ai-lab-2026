import pandas as pd
import requests
import google.generativeai as genai
import os
import json
import time

# --- 1. SETUP AGENT (GEMINI 3 FLASH) ---
# Get your key at: https://aistudio.google.com/
GEMINI_API_KEY = "AIzaSyBRJ1CsLVFpOn2v10d2S_7ouGdSzsSYD50" 
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-3-flash')

# --- 2. THE PRINCIPAL MANDATE (System Instructions) ---
# This defines the "Rules of the Game" for the Agent.
PRINCIPAL_MANDATE = """
You are a Financial Fraud Detection Agent operating within a GMD (Governance as Mechanism Design) framework.
Your Goal: Identify patterns of fraud in transaction logs.
Suspicious Patterns to flag:
- 'TRANSFER' followed by 'CASH_OUT' involving the same amount.
- Transactions where 'oldbalanceOrg' is equal to the 'amount' and 'newbalanceOrig' is 0.
- High-value payments from accounts with low historical activity.

ANALYSIS TASK:
Analyze the following transaction data: {data}

OUTPUT REQUIREMENT:
1. Provide a brief reasoning (1 sentence).
2. Output a final uncertainty score (Pe) between 0.0 (certain/safe) and 1.0 (highly uncertain/fraudulent).
Format: REASONING: [text] | UNCERTAINTY: [number]
"""

# --- 3. GOVERNOR CONFIGURATION ---
GOVERNOR_URL = "https://agentic-ai-lab-2026-1054065165765.us-central1.run.app/decide"
DATA_PATH = "finance_data/finance_10k_pilot.csv"

def run_investigation(limit=10):
    print(f"--- 🚀 Starting Agentic Investigation (n={limit}) ---")
    df = pd.read_csv(DATA_PATH).head(limit)
    batch_payload = []

    for index, row in df.iterrows():
        txn_data = row.to_dict()
        
        # A. AGENT REASONING (The Non-Deterministic Step)
        print(f"Agent analyzing TXN: {txn_data['nameOrig']}...")
        prompt = PRINCIPAL_MANDATE.format(data=json.dumps(txn_data))
        response = model.generate_content(prompt)
        
        # B. EXTRACT UNCERTAINTY (Stochastic Input for the Governor)
        try:
            # We split the Gemini response to find the numeric score
            raw_text = response.text
            uncertainty = float(raw_text.split("UNCERTAINTY:")[1].strip())
        except Exception:
            uncertainty = 0.5 # Default risk if reasoning is ambiguous
        
        # C. PREPARE BATCH FOR GOVERNOR
        batch_payload.append({
            "task_id": str(txn_data['nameOrig']),
            "value": float(txn_data['amount']),
            "criticality": float(txn_data['amount'] * 1.5), # Ce: Potential loss multiplier
            "uncertainty": uncertainty
        })

    # D. CALL THE GOVERNOR (The Deterministic Math Step)
    print(f"--- ⚖️ Sending Batch to Cloud Governor ---")
    try:
        gov_response = requests.post(GOVERNOR_URL, json=batch_payload)
        gov_data = gov_response.json()
        
        # E. DISPLAY THE AUDIT TABLE
        results_df = pd.DataFrame(gov_data)
        print("\n" + "="*50)
        print("PHD INVESTIGATION: GMD AUDIT LOG (FINANCE REALITY)")
        print("="*50)
        print(results_df[["Transaction_ID", "Autonomy_Lx", "Utility_Score", "Risk_Mitigated"]])
        print("="*50)
        
    except Exception as e:
        print(f"Governor Connection Error: {e}")

if __name__ == "__main__":
    run_investigation(limit=20) # Running 20 to see the Lx distribution