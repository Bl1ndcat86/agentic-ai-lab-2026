import pandas as pd
import requests
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json

# --- 1. SECURE SETUP ---
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-3-flash')

# --- 2. THE PRINCIPAL MANDATE ---
# This is where you tell the Agent how to behave
PRINCIPAL_MANDATE = """
You are a Financial Fraud Agent in a GMD system. 
Analyze this transaction: {data}
Provide your analysis in exactly this format:
REASONING: [1 sentence logic] | UNCERTAINTY: [0.0-1.0]
"""

GOVERNOR_URL = "https://agentic-ai-lab-2026-1054065165765.us-central1.run.app/decide"

def run_investigation(limit=10):
    print(f"--- 🚀 Starting Agentic Run (n={limit}) ---")
    df = pd.read_csv("finance_data/finance_10k_pilot.csv").head(limit)
    batch_payload = []

    for _, row in df.iterrows():
        # Agent Thinking Step
        prompt = PRINCIPAL_MANDATE.format(data=row.to_dict())
        response = model.generate_content(prompt)
        
        try:
            # Parsing Gemini's response
            reasoning = response.text.split("REASONING:")[1].split("|")[0].strip()
            uncertainty = float(response.text.split("UNCERTAINTY:")[1].strip())
        except:
            reasoning = "Format error in Agent response."
            uncertainty = 0.5

        batch_payload.append({
            "task_id": str(row['nameOrig']),
            "value": float(row['amount']),
            "criticality": float(row['amount'] * 1.5),
            "uncertainty": uncertainty,
            "reasoning": reasoning # This "thinking" is sent to the Governor
        })

    # Call the Cloud Governor
    print(f"--- ⚖️ Sending to Cloud Governor ---")
    res = requests.post(GOVERNOR_URL, json=batch_payload)
    
    # Display results as a table in your terminal
    print("\n" + "="*80)
    print("PHD AUDIT LOG: FINANCE REALITY")
    print("="*80)
    print(pd.DataFrame(res.json())[["ID", "Lx_Level", "Risk_Mitigated", "Gemini_Reasoning"]])

if __name__ == "__main__":
    run_investigation(limit=5)