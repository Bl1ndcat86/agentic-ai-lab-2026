import os
import logging
from typing import List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
import google.generativeai as genai

# --- 1. CONFIGURATION & LOGGING ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Agentic AI Lab - AAM/GMD Research",
    description="2026 Edition: High-speed reasoning for Autonomous Allocation Mechanisms."
)

# Load the Gemini API Key from your Cloud Run Environment Variables
# IMPORTANT: Ensure this key is from your 'Default Gemini Project' (the paid one)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    # Using the 2026 Stable Standard: gemini-2.5-flash
    model = genai.GenerativeModel(model_name='gemini-2.5-flash')
    logger.info("Gemini 2.5 Flash successfully configured on Paid Tier.")
else:
    logger.warning("GEMINI_API_KEY is missing! The 'Brain' is offline.")

# --- 2. MODELS ---
class ReasoningRequest(BaseModel):
    scenario: str
    context: str = "AAM/GMD Framework"

# --- 3. REST ENDPOINTS ---

@app.get("/")
async def health_check():
    """Verifies infrastructure and AI connectivity."""
    return {
        "status": "online",
        "model": "gemini-2.5-flash",
        "ai_enabled": bool(GEMINI_API_KEY),
        "research": "AAM & Governance as Mechanism Design"
    }

@app.post("/reason")
async def direct_reasoning(request: ReasoningRequest):
    """Directly test a PhD scenario via Swagger UI."""
    if not GEMINI_API_KEY:
        return {"error": "AI not enabled. Please check your API Key and Billing."}
        
    prompt = (
        f"Role: Governance Engine for an Autonomous Allocation Mechanism (AAM).\n"
        f"Context: {request.context}\n"
        f"Task: Analyze this resource conflict and provide an incentive-compatible decision.\n"
        f"Scenario: {request.scenario}"
    )
    
    try:
        response = model.generate_content(prompt)
        return {
            "status": "decision_rendered",
            "analysis": response.text
        }
    except Exception as e:
        logger.error(f"Reasoning Error: {e}")
        return {"error": str(e)}

# --- 4. WEBSOCKET ENDPOINTS ---

@app.websocket("/ws")
async def agent_socket(websocket: WebSocket):
    """Real-time streaming for multi-agent PhD simulations."""
    await websocket.accept()
    logger.info("WebSocket connection established.")
    
    try:
        while True:
            data = await websocket.receive_text()
            if GEMINI_API_KEY:
                prompt = f"Analyze this agentic state and provide a real-time GMD response: {data}"
                response = model.generate_content(prompt)
                await websocket.send_json({
                    "type": "agent_reasoning",
                    "content": response.text
                })
            else:
                await websocket.send_json({"type": "error", "content": "AI logic offline."})
                
    except WebSocketDisconnect:
        logger.info("Client disconnected.")
    except Exception as e:
        logger.error(f"WS Error: {e}")
        await websocket.send_json({"type": "error", "content": str(e)})