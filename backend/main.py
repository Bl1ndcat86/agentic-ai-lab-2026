import os
import logging
from datetime import datetime
from typing import List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai

# --- 1. CONFIGURATION & LOGGING ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="GMD Research Lab - Command Center",
    description="Refined Backend for AAM Governance Simulations."
)

# --- 2. CORS MIDDLEWARE ---
# This allows your index.html (running locally) to talk to Cloud Run.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 3. GLOBAL RESEARCH STATE ---
# This stores your decisions for the GET /history endpoint.
DECISION_HISTORY = []

# --- 4. AI BRAIN INITIALIZATION ---
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    # Using the 2026 GA Stable model for Paid Tier reliability
    model = genai.GenerativeModel(model_name='gemini-2.5-flash')
    logger.info("Gemini 2.5 Flash initialized on Paid Tier.")
else:
    logger.warning("GEMINI_API_KEY missing. Reasoning endpoints will return errors.")

# --- 5. DATA MODELS ---
class ReasoningRequest(BaseModel):
    scenario: str
    context: str = "AAM Conflict Simulation"

# --- 6. REST ENDPOINTS ---

@app.get("/")
async def health_check():
    """The 'Status Light' endpoint for the UI."""
    return {
        "status": "online",
        "timestamp": datetime.now().isoformat(),
        "ai_enabled": bool(GEMINI_API_KEY),
        "model": "gemini-2.5-flash"
    }

@app.get("/history")
async def get_history():
    """GET Endpoint: Retrieve the last 10 research scenarios and decisions."""
    return {
        "count": len(DECISION_HISTORY),
        "logs": DECISION_HISTORY[-10:] # Return most recent 10
    }

@app.post("/reason")
async def direct_reasoning(request: ReasoningRequest):
    """POST Endpoint: Process scenario and log the result to history."""
    if not GEMINI_API_KEY:
        return {"error": "AI Brain Offline. Check Billing/API Key."}
        
    prompt = (
        f"Role: Governance Engine for an Autonomous Allocation Mechanism (AAM).\n"
        f"Context: {request.context}\n"
        f"Scenario: {request.scenario}\n\n"
        f"Task: Provide a structured governance decision and incentive analysis."
    )
    
    try:
        response = model.generate_content(prompt)
        
        # Create a research log entry
        decision_entry = {
            "id": len(DECISION_HISTORY) + 1,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "scenario": request.scenario,
            "analysis": response.text
        }
        
        # Save to memory
        DECISION_HISTORY.append(decision_entry)
        
        return decision_entry
        
    except Exception as e:
        logger.error(f"Reasoning Error: {e}")
        return {"error": str(e)}

# --- 7. WEBSOCKET (Live Agent Streaming) ---

@app.websocket("/ws")
async def agent_socket(websocket: WebSocket):
    await websocket.accept()
    logger.info("Live Agent Stream Connected.")
    
    try:
        while True:
            data = await websocket.receive_text()
            if GEMINI_API_KEY:
                # Direct simulation of agent 'thought' stream
                response = model.generate_content(f"GMD Agent Response: {data}")
                await websocket.send_json({
                    "type": "stream_output",
                    "content": response.text,
                    "time": datetime.now().isoformat()
                })
    except WebSocketDisconnect:
        logger.info("Agent Disconnected.")