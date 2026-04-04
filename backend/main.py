import os
import logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import google.generativeai as genai

# 1. Setup Logging (Essential for debugging in GCP)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Agentic AI Lab - AAM/GMD Research")

# 2. Securely Load Gemini API Key
# This is pulled from the Environment Variables you set in the Cloud Run console
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    logger.info("Gemini 1.5 Flash successfully configured.")
else:
    logger.warning("GEMINI_API_KEY is missing! The agent will run in 'Mock Mode'.")

@app.get("/")
async def root():
    """
    Health check endpoint. If you see this, your Cloud Run deployment 
    is successful and the container is listening on Port 8080.
    """
    return {
        "status": "online",
        "research_context": "Autonomous Allocation Mechanism (AAM)",
        "ai_enabled": bool(GEMINI_API_KEY),
        "message": "Welcome to the GMD Research Lab."
    }

@app.websocket("/ws")
async def agent_socket(websocket: WebSocket):
    """
    Real-time endpoint for Agentic logic. 
    This allows your PhD simulation to stream its 'reasoning' steps.
    """
    await websocket.accept()
    logger.info("WebSocket connection established.")
    
    try:
        while True:
            # Wait for a trigger from the frontend
            data = await websocket.receive_text()
            
            if GEMINI_API_KEY:
                # Actual PhD-level reasoning via Gemini
                prompt = f"Act as an AI Agent in a GMD system. Analyze this allocation request: {data}. Provide a 3-step strategy."
                response = model.generate_content(prompt)
                await websocket.send_json({
                    "type": "agent_reasoning",
                    "content": response.text
                })
            else:
                # Mock response if key is missing (prevents the whole lab from crashing)
                await websocket.send_json({
                    "type": "error",
                    "content": "AI logic offline: GEMINI_API_KEY not found in environment variables."
                })
                
    except WebSocketDisconnect:
        logger.info("Client disconnected from WebSocket.")
    except Exception as e:
        logger.error(f"Error in WebSocket: {e}")
        await websocket.send_json({"type": "error", "content": str(e)})