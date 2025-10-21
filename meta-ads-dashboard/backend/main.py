from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import os
from typing import Dict, List
import logging
import asyncio
import json
from pydantic import BaseModel
import httpx

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Meta Ads AI Agent Management API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DOCKER_COMPOSE_DIR = "/root/meta-ads-master-agent"
SERVICE_NAMES = ["master", "image-generator", "performance-analyzer", "campaign-manager"]

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

def run_command(command: List[str], cwd: str = DOCKER_COMPOSE_DIR) -> tuple:
    """Execute a shell command and return output and error."""
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=408, detail="Command timed out")
    except Exception as e:
        logger.error(f"Command execution error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

def get_container_status(service_name: str) -> Dict:
    """Get the status of a specific Docker Compose service."""
    stdout, stderr, returncode = run_command([
        "docker-compose", "ps", "-q", service_name
    ])
    
    if not stdout.strip():
        return {"name": service_name, "status": "stopped", "container_id": None}
    
    container_id = stdout.strip()
    stdout, stderr, returncode = run_command([
        "docker", "inspect", "-f", "{{.State.Status}}", container_id
    ])
    
    status = stdout.strip()
    return {
        "name": service_name,
        "status": "running" if status == "running" else "stopped",
        "container_id": container_id
    }

async def get_all_services_status_data() -> Dict:
    """Helper to get status of all services without raising HTTPExceptions."""
    services = []
    for service_name in SERVICE_NAMES:
        service_status = get_container_status(service_name)
        services.append(service_status)
    return {
        "success": True,
        "services": services
    }

@app.get("/")
async def root():
    return {"message": "Meta Ads AI Agent Management API", "version": "1.0.0"}

@app.get("/api/status")
async def get_all_status():
    """Get status of all services."""
    try:
        return await get_all_services_status_data()
    except Exception as e:
        logger.error(f"Error getting status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/start-all")
async def start_all_services():
    """Start all services using docker-compose up -d."""
    try:
        stdout, stderr, returncode = run_command(["docker-compose", "up", "-d"])
        
        if returncode != 0:
            raise HTTPException(status_code=500, detail=f"Failed to start services: {stderr}")
        
        await manager.broadcast(json.dumps(await get_all_services_status_data())) # Broadcast update
        return {
            "success": True,
            "message": "All services started successfully",
            "output": stdout
        }
    except Exception as e:
        logger.error(f"Error starting services: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/stop-all")
async def stop_all_services():
    """Stop all services using docker-compose down."""
    try:
        stdout, stderr, returncode = run_command(["docker-compose", "down"])
        
        if returncode != 0:
            raise HTTPException(status_code=500, detail=f"Failed to stop services: {stderr}")
        
        await manager.broadcast(json.dumps(await get_all_services_status_data())) # Broadcast update
        return {
            "success": True,
            "message": "All services stopped successfully",
            "output": stdout
        }
    except Exception as e:
        logger.error(f"Error stopping services: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/start-service/{service_name}")
async def start_service(service_name: str):
    """Start a specific service."""
    if service_name not in SERVICE_NAMES:
        raise HTTPException(status_code=404, detail=f"Service \'{service_name}\' not found")
    
    try:
        stdout, stderr, returncode = run_command(["docker-compose", "up", "-d", service_name])
        
        if returncode != 0:
            raise HTTPException(status_code=500, detail=f"Failed to start service: {stderr}")
        
        await manager.broadcast(json.dumps(await get_all_services_status_data())) # Broadcast update
        return {
            "success": True,
            "message": f"Service \'{service_name}\' started successfully",
            "output": stdout
        }
    except Exception as e:
        logger.error(f"Error starting service {service_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/stop-service/{service_name}")
async def stop_service(service_name: str):
    """Stop a specific service."""
    if service_name not in SERVICE_NAMES:
        raise HTTPException(status_code=404, detail=f"Service \'{service_name}\' not found")
    
    try:
        stdout, stderr, returncode = run_command(["docker-compose", "stop", service_name])
        
        if returncode != 0:
            raise HTTPException(status_code=500, detail=f"Failed to stop service: {stderr}")
        
        await manager.broadcast(json.dumps(await get_all_services_status_data())) # Broadcast update
        return {
            "success": True,
            "message": f"Service \'{service_name}\' stopped successfully",
            "output": stdout
        }
    except Exception as e:
        logger.error(f"Error stopping service {service_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/restart-service/{service_name}")
async def restart_service(service_name: str):
    """Restart a specific service."""
    if service_name not in SERVICE_NAMES:
        raise HTTPException(status_code=404, detail=f"Service \'{service_name}\' not found")
    
    try:
        stdout, stderr, returncode = run_command(["docker-compose", "restart", service_name])
        
        if returncode != 0:
            raise HTTPException(status_code=500, detail=f"Failed to restart service: {stderr}")
        
        await manager.broadcast(json.dumps(await get_all_services_status_data())) # Broadcast update
        return {
            "success": True,
            "message": f"Service \'{service_name}\' restarted successfully",
            "output": stdout
        }
    except Exception as e:
        logger.error(f"Error restarting service {service_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/logs/{service_name}")
async def get_service_logs(service_name: str, lines: int = 100):
    """Get logs for a specific service."""
    if service_name not in SERVICE_NAMES:
        raise HTTPException(status_code=404, detail=f"Service \'{service_name}\' not found")
    
    try:
        stdout, stderr, returncode = run_command([
            "docker-compose", "logs", "--tail", str(lines), service_name
        ])
        
        return {
            "success": True,
            "service": service_name,
            "logs": stdout if stdout else stderr
        }
    except Exception as e:
        logger.error(f"Error getting logs for {service_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.websocket("/ws/status")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Send initial status immediately upon connection
            await websocket.send_json(await get_all_services_status_data())
            await asyncio.sleep(5) # Send updates every 5 seconds
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")

# Placeholder for OpenAI client (will be initialized with env var)
openai_client = None

# Define a Pydantic model for the ExecutionRequest, matching the Master Agent\'s API
class MasterExecutionRequest(BaseModel):
    ads_to_create: int
    daily_budget: float

# Base URL for the Master Agent service
MASTER_AGENT_URL = "http://localhost:8000" # Assuming master service is accessible locally from the dashboard backend

async def interact_with_meta_ads_agent(prompt: str):
    if "status" in prompt.lower():
        # Call the dashboard\'s own status endpoint
        status_data = await get_all_services_status_data()
        if status_data["success"]:
            running_services = [s["name"] for s in status_data["services"] if s["status"] == "running"]
            stopped_services = [s["name"] for s in status_data["services"] if s["status"] == "stopped"]
            response_text = f"Here is the current status of your Meta Ads AI Agent services:\nRunning: {', '.join(running_services) if running_services else 'None'}\nStopped: {', '.join(stopped_services) if stopped_services else 'None'}"
            return {"response": response_text}
        else:
            return {"response": "I could not retrieve the service status. Please check the backend logs."}
    elif "create ad" in prompt.lower():
        try:
            parts = prompt.lower().split()
            ads_to_create = 1
            daily_budget = 5.0 # Default budget

            if "create" in parts and "ads" in parts:
                for i, part in enumerate(parts):
                    if part == "create" and i + 1 < len(parts) and parts[i+1].isdigit():
                        ads_to_create = int(parts[i+1])
                    if part == "budget" and i + 1 < len(parts) and parts[i+1].replace(".", "", 1).isdigit():
                        daily_budget = float(parts[i+1])

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{MASTER_AGENT_URL}/execute",
                    json=MasterExecutionRequest(ads_to_create=ads_to_create, daily_budget=daily_budget).dict(),
                    timeout=300 # Extended timeout for agent execution
                )
                response.raise_for_status() # Raise an exception for HTTP errors
                result = response.json()

                if result.get("success"):
                    return {"response": f"Successfully initiated creation of {result["ads_created"]} ads with a total cost of ${result["total_cost"]:.2f}. Errors: {', '.join(result["errors"]) if result["errors"] else "None"}."}
                else:
                    return {"response": f"Failed to create ads: {', '.join(result["errors"]) if result["errors"] else "Unknown error."}"}
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error interacting with Master Agent: {e.response.text}")
            return {"response": f"Error communicating with the Master Agent: {e.response.status_code} - {e.response.text}"}
        except httpx.RequestError as e:
            logger.error(f"Network error interacting with Master Agent: {e}")
            return {"response": f"Network error while reaching Master Agent: {e}"}
        except Exception as e:
            logger.error(f"Error processing ad creation request: {str(e)}")
            return {"response": f"I encountered an error trying to create ads: {str(e)}. Please try again or refine your request."}
    elif "what are you" in prompt.lower() or "who are you" in prompt.lower() or "connect" in prompt.lower():
        return {"response": "I am the Meta Ads AI Agent Dashboard Assistant. I'm connected to:\n\n1. **Meta Ads Master Agent** (Port 8000) - Orchestrates ad creation and campaign management\n2. **Image Generator Service** (Port 8001) - Creates AI-powered ad creatives\n3. **Performance Analyzer** (Port 8003) - Monitors and analyzes campaign performance\n4. **Campaign Manager** (Port 8004) - Manages campaign configurations\n\nI can help you:\n- Check service status\n- Create ads (e.g., 'create 5 ads with budget 10.0')\n- Monitor agent performance\n- Manage your Meta Ads campaigns\n\nAll services are managed via Docker Compose and communicate with Meta's Ads API."}
    else:
        return {"response": f"I received your message: '{prompt}'. I\'m still learning how to process complex requests. Please try asking about:\n\n- Service status (e.g., 'what is the status?')\n- Ad creation (e.g., 'create 5 ads with budget 10.0')\n- My capabilities (e.g., 'what are you connected to?')"}

@app.post("/api/chat")
async def chat_with_agent(message: dict):
    user_message = message.get("message")
    if not user_message:
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    response = await interact_with_meta_ads_agent(user_message)
    return {"response": response["response"]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8889)




class DashboardSettings(BaseModel):
    openrouterApiKey: str = ""
    aiModel: str = "gpt-4.1-mini"
    kieApiKey: str = ""
    fbAccessToken: str = ""
    adAccountId: str = ""
    pageId: str = ""
    runInterval: str = ""
    adsPerRun: str = ""
    dailyBudget: str = ""

@app.post("/api/settings")
async def save_settings(settings: DashboardSettings):
    """Save dashboard settings to .env file."""
    try:
        env_file_path = os.path.join(DOCKER_COMPOSE_DIR, ".env")
        
        # Read existing .env content
        env_content = {}
        if os.path.exists(env_file_path):
            with open(env_file_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, value = line.split("=", 1)
                        env_content[key] = value
        
        # Update with new settings
        if settings.kieApiKey:
            env_content["KIE_API_KEY"] = settings.kieApiKey
        if settings.fbAccessToken:
            env_content["FB_ACCESS_TOKEN"] = settings.fbAccessToken
        if settings.adAccountId:
            env_content["AD_ACCOUNT_ID"] = settings.adAccountId
        if settings.pageId:
            env_content["PAGE_ID"] = settings.pageId
        if settings.runInterval:
            env_content["RUN_INTERVAL"] = settings.runInterval
        if settings.adsPerRun:
            env_content["ADS_PER_RUN"] = settings.adsPerRun
        if settings.dailyBudget:
            env_content["DAILY_BUDGET"] = settings.dailyBudget
        
        # Write back to .env file
        with open(env_file_path, "w") as f:
            for key, value in env_content.items():
                f.write(f"{key}={value}\n")
        
        return {
            "success": True,
            "message": "Settings saved successfully"
        }
    except Exception as e:
        logger.error(f"Error saving settings: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/settings")
async def get_settings():
    """Get current dashboard settings from .env file."""
    try:
        env_file_path = os.path.join(DOCKER_COMPOSE_DIR, ".env")
        settings = {}
        
        if os.path.exists(env_file_path):
            with open(env_file_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, value = line.split("=", 1)
                        if key == "KIE_API_KEY":
                            settings["kieApiKey"] = value
                        elif key == "FB_ACCESS_TOKEN":
                            settings["fbAccessToken"] = value
                        elif key == "AD_ACCOUNT_ID":
                            settings["adAccountId"] = value
                        elif key == "PAGE_ID":
                            settings["pageId"] = value
                        elif key == "RUN_INTERVAL":
                            settings["runInterval"] = value
                        elif key == "ADS_PER_RUN":
                            settings["adsPerRun"] = value
                        elif key == "DAILY_BUDGET":
                            settings["dailyBudget"] = value
        
        return {
            "success": True,
            "settings": settings
        }
    except Exception as e:
        logger.error(f"Error getting settings: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

