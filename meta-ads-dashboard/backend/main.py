from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import os
from typing import Dict, List
import logging

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

@app.get("/")
async def root():
    return {"message": "Meta Ads AI Agent Management API", "version": "1.0.0"}

@app.get("/api/status")
async def get_all_status():
    """Get status of all services."""
    try:
        services = []
        for service_name in SERVICE_NAMES:
            service_status = get_container_status(service_name)
            services.append(service_status)
        
        return {
            "success": True,
            "services": services
        }
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
        raise HTTPException(status_code=404, detail=f"Service '{service_name}' not found")
    
    try:
        stdout, stderr, returncode = run_command(["docker-compose", "up", "-d", service_name])
        
        if returncode != 0:
            raise HTTPException(status_code=500, detail=f"Failed to start service: {stderr}")
        
        return {
            "success": True,
            "message": f"Service '{service_name}' started successfully",
            "output": stdout
        }
    except Exception as e:
        logger.error(f"Error starting service {service_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/stop-service/{service_name}")
async def stop_service(service_name: str):
    """Stop a specific service."""
    if service_name not in SERVICE_NAMES:
        raise HTTPException(status_code=404, detail=f"Service '{service_name}' not found")
    
    try:
        stdout, stderr, returncode = run_command(["docker-compose", "stop", service_name])
        
        if returncode != 0:
            raise HTTPException(status_code=500, detail=f"Failed to stop service: {stderr}")
        
        return {
            "success": True,
            "message": f"Service '{service_name}' stopped successfully",
            "output": stdout
        }
    except Exception as e:
        logger.error(f"Error stopping service {service_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/restart-service/{service_name}")
async def restart_service(service_name: str):
    """Restart a specific service."""
    if service_name not in SERVICE_NAMES:
        raise HTTPException(status_code=404, detail=f"Service '{service_name}' not found")
    
    try:
        stdout, stderr, returncode = run_command(["docker-compose", "restart", service_name])
        
        if returncode != 0:
            raise HTTPException(status_code=500, detail=f"Failed to restart service: {stderr}")
        
        return {
            "success": True,
            "message": f"Service '{service_name}' restarted successfully",
            "output": stdout
        }
    except Exception as e:
        logger.error(f"Error restarting service {service_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/logs/{service_name}")
async def get_service_logs(service_name: str, lines: int = 100):
    """Get logs for a specific service."""
    if service_name not in SERVICE_NAMES:
        raise HTTPException(status_code=404, detail=f"Service '{service_name}' not found")
    
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8889)


# Imports for AI Chat
from openai import OpenAI

# Placeholder for OpenAI client (will be initialized with env var)
openai_client = None

# Function to interact with Meta Ads Master Agent
async def interact_with_meta_ads_agent(prompt: str):
    # This is a placeholder. Actual interaction logic would go here.
    # It might involve calling the master service API (e.g., port 8000)
    # or other specific agent APIs based on the prompt.
    # For now, we\'ll simulate a response.
    if "status" in prompt.lower():
        return {"response": "The Meta Ads Master Agent is currently running. All services are operational."}
    elif "create ad" in prompt.lower():
        return {"response": "I can create an ad. What are the ad specifications?"}
    else:
        return {"response": f"I received your message: ‘{prompt}’. I\'m still learning how to process complex requests. Please try asking about service status or ad creation."}

@app.post("/api/chat")
async def chat_with_agent(message: dict):
    user_message = message.get("message")
    if not user_message:
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    # Use OpenAI for more advanced natural language understanding if configured
    # For now, we\'ll use a simple rule-based interaction
    response = await interact_with_meta_ads_agent(user_message)
    return {"response": response["response"]}

