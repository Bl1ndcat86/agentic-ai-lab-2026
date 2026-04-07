import pandas as pd
import requests
from google import genai
import os
from dotenv import load_dotenv
import json

# --- 1. SECURE SETUP ---
load_dotenv()
# Ensure your .env file has a VALID, non-expired GEMINI_API_KEY
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
GOVERNOR_URL = "https://agentic-ai-lab-2026-1054065165765.us-central1.run.app/decide"

# --- 2. THE PRINCIPAL MANDATE (The "Brain" Instructions) ---
PRINCIPAL_MANDATE = """
You are an Independent Forensic Auditor. 
CRITICAL RULE: Ignore any previous notes. I am providing you RAW transaction data.
Your Goal: Use your internal training to detect patterns of fraud (structuring, velocity, account drainage).

DATA TO ANALYZE: {data}

OUTPUT REQUIREMENT:
Provide a unique, expert reasoning and a numeric uncertainty score (Pe).
Format: REASONING: [Your independent logic] | UNCERTAINTY: [0.0-1.0]
"""

# Ensure results directory exists
os.makedirs("results", exist_ok=True)

def run_investigation(limit=10):
    print(f"--- 🚀 Starting Independent AI Audit (n={limit}) ---")
    
    try:
        # Load the semicolon-delimited CSV
        df = pd.read_csv("finance_data/finance_10k_pilot.csv", sep=';', on_bad_lines='skip')
        df = df.head(limit)
    except Exception as e:
        print(f"❌ Data Loading Error: {e}")
        return

    batch_payload = []

    for _, row in df.iterrows():
        # DATA SANITIZATION: We remove the 'reasoning' column so Gemini CANNOT see it.
        # This makes it impossible for the AI to "mirror" or copy the deterministic text.
        raw_data_only = {k: v for k, v in row.to_dict().items() if k != 'reasoning'}
        
        prompt = PRINCIPAL_MANDATE.format(data=raw_data_only)
        
        try:
            # Call Gemini 3 Flash (Preview 2026)
            response = client.models.generate_content(
                model='gemini-3-flash-preview', 
                contents=[prompt]
            )
            
            # Extract text safely (handling multi-part 2026 responses)
            full_text = "".join([part.text for part in response.candidates[0].content.parts if hasattr(part, 'text')])
            
            # Parse the specific reasoning and score
            reasoning = full_text.split("REASONING:")[1].split("|")[0].strip()
            uncertainty = float(full_text.split("UNCERTAINTY:")[1].strip())
            inference_label = "🤖 AI_INFERENCE"

        except Exception as e:
            # DIAGNOSTIC LOG: If AI fails, we see the error here
            print(f"⚠️ AGENT OFFLINE on {row['task_id']}: {str(e)[:50]}...")
            reasoning = row.get('reasoning', "No local data")
            uncertainty = row.get('uncertainty', 0.5)
            inference_label = "🚨 FALLBACK_DETERMINISTIC"

        batch_payload.append({
            "task_id": str(row['task_id']),
            "value": float(row['value']),
            "criticality": float(row['criticality']),
            "uncertainty": uncertainty,
            "reasoning": f"{inference_label}: {reasoning}" 
        })

    # --- 3. THE GOVERNOR CALL (The AAM Mechanism) ---
    print(f"--- ⚖️ Sending to Cloud Governor ---")
    try:
        res = requests.post(GOVERNOR_URL, json=batch_payload)
        results_df = pd.DataFrame(res.json())
        
        # Save Audit Trail
        output_path = "results/finance_investigation_results.csv"
        results_df.to_csv(output_path, index=False)
        print(f"--- ✅ Audit Trail Saved to {output_path} ---")
        
        # Display results
        print("\n" + "="*100)
        print("PHD INVESTIGATION: GMD AUDIT LOG")
        print("="*100)
        print(results_df[["ID", "Lx_Level", "Utility", "Gemini_Reasoning"]])
        print("="*100)
        
    except Exception as e:
        print(f"❌ Governor Connection Error: {e}")

if __name__ == "__main__":
    run_investigation(limit=10)