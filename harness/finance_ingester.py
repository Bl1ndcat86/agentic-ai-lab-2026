import pandas as pd
import requests
from google import genai # <--- NEW: Using the modern SDK
import os
from dotenv import load_dotenv
import json

# --- 1. SECURE SETUP ---
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# The new Client architecture is now the standard for 2026
client = genai.Client(api_key=GEMINI_API_KEY)

# --- 2. THE PRINCIPAL MANDATE ---
PRINCIPAL_MANDATE = """
You are a Financial Fraud Agent in a GMD system. 
Analyze this transaction: {data}
Provide your analysis in exactly this format:
REASONING: [1 sentence logic] | UNCERTAINTY: [0.0-1.0]
"""

GOVERNOR_URL = "https://agentic-ai-lab-2026-1054065165765.us-central1.run.app/decide"

def run_investigation(limit=5):
    print(f"--- 🚀 Starting Agentic Run (n={limit}) ---")
    
    try:
        df = pd.read_csv("finance_data/finance_10k_pilot.csv").head(limit)
    except FileNotFoundError:
        print("❌ Error: CSV file not found.")
        return

    batch_payload = []

    for _, row in df.iterrows():
        # Agent Thinking Step
        prompt = PRINCIPAL_MANDATE.format(data=row.to_dict())
        
        # Updated Model ID and generate_content call
        try:
            response = client.models.generate_content(
                model='gemini-3-flash-preview', # <--- FIXED: Added -preview suffix
                contents=prompt
            )
            
            full_text = response.text
            # Parsing logic
            reasoning = full_text.split("REASONING:")[1].split("|")[0].strip()
            uncertainty = float(full_text.split("UNCERTAINTY:")[1].strip())
            
        except Exception as e:
            print(f"⚠️ Agent error on TXN {row['nameOrig']}: {e}")
            reasoning = "Agent failed to reason or model not found."
            uncertainty = 0.5

        batch_payload.append({
            "task_id": str(row['nameOrig']),
            "value": float(row['amount']),
            "criticality": float(row['amount'] * 1.5),
            "uncertainty": uncertainty,
            "reasoning": reasoning 
        })

    # Call the Cloud Governor
    print(f"--- ⚖️ Sending Batch to Cloud Governor ---")
    try:
        res = requests.post(GOVERNOR_URL, json=batch_payload)
        res.raise_for_status()
        
        # Display the Audit Table
        print("\n" + "="*90)
        print("PHD AUDIT LOG: GMD FINANCE INVESTIGATION")
        print("="*90)
        results_df = pd.DataFrame(res.json())
        print(results_df[["ID", "Lx_Level", "Risk_Mitigated", "Gemini_Reasoning"]])
        print("="*90)
    except Exception as e:
        print(f"❌ Governor Error: {e}")

if __name__ == "__main__":
    run_investigation(limit=5)