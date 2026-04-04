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
    title="Agentic AI Lab - Guillermo's AAM (autonomous alloca mechanism) and GMD (governance as mechanism design) PhD Research",
    description="This is the Backend for the Autonomous Allocation Mechanism and Governance as Mechanism Design"
)

# Load the Gemini API Key from Cloud Run Environment Variables
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(model_name='gemini-2.0-flash')
    logger.info("Gemini 1.5 Flash successfully configured.")
else:
    logger.warning("GEMINI_API_KEY is missing! Agent logic will be disabled.")

# --- 2. MODELS ---
class ReasoningRequest(BaseModel):
    scenario: str
    context: str = "General AAM (autonomous alloca mechanism) Governance"

# --- 3. REST ENDPOINTS ---

@app.get("/")
async def health_check():
    """
    Verifies the container is live and the AI 'Brain' is connected.
    """
    return {
        "status": "online",
        "research_context": "Autonomous Allocation Mechanism (AAM)",
        "ai_enabled": bool(GEMINI_API_KEY),
        "message": "Welcome to Memos AAM/GMD PhD Research Lab."
    }

@app.post("/reason")
async def direct_reasoning(request: ReasoningRequest):
    """
    Directly test an AAM decision logic via a single request.
    Use this in /docs for controlled PhD scenario testing.
    """
    if not GEMINI_API_KEY:
        return {"error": "AI not enabled. Please check your GEMINI_API_KEY."}
        
    prompt = (
        f"Role: Governance Engine for an Autonomous Allocation Mechanism (AAM).\n"
        f"Task: Analyze the following resource conflict and provide an incentive-compatible decision.\n"
        f"Context: {request.context}\n"
        f"Scenario: {request.scenario}\n\n"
        f"Decision Logic (Decision + Reasoning):"
    )
    
    try:
        response = model.generate_content(prompt)
        return {
            "status": "decision_rendered",
            "analysis": response.text
        }
    except Exception as e:
        logger.error(f"Gemini Error: {e}")
        return {"error": str(e)}

# --- 4. WEBSOCKET ENDPOINTS ---

@app.websocket("/ws")
async def agent_socket(websocket: WebSocket):
    """
    Real-time bidirectional communication for live agent simulations.
    """
    await websocket.accept()
    logger.info("WebSocket connection established.")
    
    try:
        while True:
            # Receive data from the client (e.g., frontend or test script)
            data = await websocket.receive_text()
            
            if GEMINI_API_KEY:
                # Process the agent's 'thought process'
                prompt = f"Analyze this agentic state in a GMD system and respond: {data}"
                response = model.generate_content(prompt)
                
                await websocket.send_json({
                    "type": "agent_reasoning",
                    "content": response.text
                })
            else:
                await websocket.send_json({
                    "type": "error",
                    "content": "AI logic offline: API key missing."
                })
                
    except WebSocketDisconnect:
        logger.info("Client disconnected from WebSocket.")
    except Exception as e:
        logger.error(f"WebSocket Error: {e}")
        await websocket.send_json({"type": "error", "content": str(e)})