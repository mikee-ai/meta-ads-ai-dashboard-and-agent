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

# MCP Server URLs (using localhost since they're on the same VPS)
MASTER_SERVICE_URL = "http://localhost:8000"
IMAGE_SERVICE_URL = "http://localhost:8001"
PERFORMANCE_SERVICE_URL = "http://localhost:8003"
CAMPAIGN_SERVICE_URL = "http://localhost:8004"

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

@app.get("/api/services")
async def get_all_services():
    """Get status of all services."""
    return await get_all_services_status_data()

@app.get("/api/status")
async def get_status():
    """Get status of all services (alias for /api/services)."""
    return await get_all_services_status_data()

@app.post("/api/services/{service_name}/start")
async def start_service(service_name: str):
    """Start a specific service."""
    if service_name not in SERVICE_NAMES:
        raise HTTPException(status_code=404, detail=f"Service '{service_name}' not found")
    
    stdout, stderr, returncode = run_command([
        "docker-compose", "up", "-d", service_name
    ])
    
    await manager.broadcast(json.dumps({"type": "service_update", "service": service_name}))
    
    return {
        "success": returncode == 0,
        "service": service_name,
        "action": "start",
        "output": stdout,
        "error": stderr
    }

@app.post("/api/services/{service_name}/stop")
async def stop_service(service_name: str):
    """Stop a specific service."""
    if service_name not in SERVICE_NAMES:
        raise HTTPException(status_code=404, detail=f"Service '{service_name}' not found")
    
    stdout, stderr, returncode = run_command([
        "docker-compose", "stop", service_name
    ])
    
    await manager.broadcast(json.dumps({"type": "service_update", "service": service_name}))
    
    return {
        "success": returncode == 0,
        "service": service_name,
        "action": "stop",
        "output": stdout,
        "error": stderr
    }

@app.post("/api/services/{service_name}/restart")
async def restart_service(service_name: str):
    """Restart a specific service."""
    if service_name not in SERVICE_NAMES:
        raise HTTPException(status_code=404, detail=f"Service '{service_name}' not found")
    
    stdout, stderr, returncode = run_command([
        "docker-compose", "restart", service_name
    ])
    
    await manager.broadcast(json.dumps({"type": "service_update", "service": service_name}))
    
    return {
        "success": returncode == 0,
        "service": service_name,
        "action": "restart",
        "output": stdout,
        "error": stderr
    }

@app.get("/api/services/{service_name}/logs")
async def get_service_logs(service_name: str, lines: int = 100):
    """Get logs for a specific service."""
    if service_name not in SERVICE_NAMES:
        raise HTTPException(status_code=404, detail=f"Service '{service_name}' not found")
    
    stdout, stderr, returncode = run_command([
        "docker-compose", "logs", "--tail", str(lines), service_name
    ])
    
    return {
        "success": returncode == 0,
        "service": service_name,
        "logs": stdout,
        "error": stderr
    }

@app.post("/api/services/start-all")
async def start_all_services():
    """Start all services."""
    stdout, stderr, returncode = run_command([
        "docker-compose", "up", "-d"
    ])
    
    await manager.broadcast(json.dumps({"type": "service_update", "service": "all"}))
    
    return {
        "success": returncode == 0,
        "action": "start-all",
        "output": stdout,
        "error": stderr
    }

@app.post("/api/services/stop-all")
async def stop_all_services():
    """Stop all services."""
    stdout, stderr, returncode = run_command([
        "docker-compose", "stop"
    ])
    
    await manager.broadcast(json.dumps({"type": "service_update", "service": "all"}))
    
    return {
        "success": returncode == 0,
        "action": "stop-all",
        "output": stdout,
        "error": stderr
    }

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates."""
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# MCP Tool Definitions
MCP_TOOLS = [
    {
        "name": "create_ads",
        "description": "Create new Meta ads with AI-generated images and copy. Orchestrates the complete ad creation workflow including hook selection, image generation, and campaign creation.",
        "parameters": {
            "type": "object",
            "properties": {
                "ads_to_create": {
                    "type": "integer",
                    "description": "Number of ads to create (1-10)",
                    "default": 1
                },
                "daily_budget": {
                    "type": "integer",
                    "description": "Daily budget in cents (e.g., 500 = $5.00)",
                    "default": 500
                }
            }
        }
    },
    {
        "name": "check_service_health",
        "description": "Check the health status of all Meta Ads microservices",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "get_recent_ads_count",
        "description": "Get the count of ads created in a specific time period",
        "parameters": {
            "type": "object",
            "properties": {
                "hours": {
                    "type": "integer",
                    "description": "Number of hours to look back",
                    "default": 4
                }
            }
        }
    }
]

async def call_mcp_tool(tool_name: str, arguments: dict) -> str:
    """Call an MCP tool and return the result"""
    try:
        if tool_name == "create_ads":
            ads_to_create = arguments.get("ads_to_create", 1)
            daily_budget = arguments.get("daily_budget", 500)
            
            async with httpx.AsyncClient(timeout=600.0) as client:
                response = await client.post(
                    f"{MASTER_SERVICE_URL}/execute",
                    json={
                        "ads_to_create": ads_to_create,
                        "daily_budget": daily_budget
                    }
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return json.dumps(result, indent=2)
                else:
                    return f"Error creating ads: {response.status_code} - {response.text}"
        
        elif tool_name == "check_service_health":
            health_status = {}
            services = {
                "master": f"{MASTER_SERVICE_URL}/health",
                "image-generator": f"{IMAGE_SERVICE_URL}/health",
                "performance-analyzer": f"{PERFORMANCE_SERVICE_URL}/health",
                "campaign-manager": f"{CAMPAIGN_SERVICE_URL}/health"
            }
            
            async with httpx.AsyncClient(timeout=5.0) as client:
                for service_name, health_url in services.items():
                    try:
                        response = await client.get(health_url)
                        health_status[service_name] = {
                            "status": "healthy" if response.status_code == 200 else "unhealthy",
                            "status_code": response.status_code
                        }
                    except Exception as e:
                        health_status[service_name] = {
                            "status": "unreachable",
                            "error": str(e)
                        }
            
            return json.dumps(health_status, indent=2)
        
        elif tool_name == "get_recent_ads_count":
            hours = arguments.get("hours", 4)
            # This would query logs or database for recent ads
            # For now, return a simulated count based on logs
            try:
                stdout, stderr, returncode = run_command([
                    "docker-compose", "logs", "--since", f"{hours}h", "master"
                ])
                
                # Count occurrences of "Ad created" or similar patterns in logs
                import re
                ad_created_pattern = r"(Ad created|ads_created|Creating Ad)"
                matches = re.findall(ad_created_pattern, stdout, re.IGNORECASE)
                count = len(matches)
                
                return json.dumps({
                    "hours": hours,
                    "ads_created": count,
                    "message": f"Found {count} ads created in the last {hours} hours based on log analysis"
                }, indent=2)
            except Exception as e:
                return json.dumps({
                    "error": str(e),
                    "message": "Could not retrieve ad count from logs"
                }, indent=2)
        
        else:
            return f"Unknown tool: {tool_name}"
            
    except Exception as e:
        logger.error(f"Error calling MCP tool {tool_name}: {str(e)}")
        return f"Error: {str(e)}"

async def chat_with_ai_agent(user_message: str, api_key: str, model: str) -> str:
    """Chat with AI agent that has access to MCP tools"""
    try:
        from openai import OpenAI
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )
        
        # Get current service status for context
        status_data = await get_all_services_status_data()
        running_services = [s["name"] for s in status_data["services"] if s["status"] == "running"]
        stopped_services = [s["name"] for s in status_data["services"] if s["status"] == "stopped"]
        
        # Build system prompt with MCP tools
        tools_description = "\n".join([
            f"- {tool['name']}: {tool['description']}"
            for tool in MCP_TOOLS
        ])
        
        system_prompt = f"""You are the Meta Ads AI Agent Dashboard Assistant with access to powerful tools through the Model Context Protocol (MCP).

Current System Status:
- Running Services: {', '.join(running_services) if running_services else 'None'}
- Stopped Services: {', '.join(stopped_services) if stopped_services else 'None'}

You are connected to:
1. Meta Ads Master Agent (Port 8000) - Orchestrates ad creation and campaign management
2. Image Generator Service (Port 8001) - Creates AI-powered ad creatives
3. Performance Analyzer (Port 8003) - Monitors and analyzes campaign performance
4. Campaign Manager (Port 8004) - Manages campaign configurations

Available MCP Tools:
{tools_description}

When a user asks you to perform actions like creating ads, checking health, or getting statistics, you should use the appropriate tool by responding with a JSON object in this format:
{{"tool": "tool_name", "arguments": {{"param": "value"}}}}

For example:
- To create 5 ads: {{"tool": "create_ads", "arguments": {{"ads_to_create": 5, "daily_budget": 1000}}}}
- To check health: {{"tool": "check_service_health", "arguments": {{}}}}
- To get recent ads count: {{"tool": "get_recent_ads_count", "arguments": {{"hours": 4}}}}

If you use a tool, respond ONLY with the JSON tool call. Otherwise, respond conversationally."""
        
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
        )
        
        ai_response = completion.choices[0].message.content
        
        # Check if AI wants to use a tool
        try:
            if ai_response.strip().startswith("{") and "tool" in ai_response:
                tool_call = json.loads(ai_response)
                tool_name = tool_call.get("tool")
                tool_args = tool_call.get("arguments", {})
                
                logger.info(f"AI agent calling tool: {tool_name} with args: {tool_args}")
                
                # Execute the tool
                tool_result = await call_mcp_tool(tool_name, tool_args)
                
                # Send result back to AI for interpretation
                completion2 = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_message},
                        {"role": "assistant", "content": ai_response},
                        {"role": "user", "content": f"Tool result:\n{tool_result}\n\nPlease interpret this result and provide a user-friendly response."}
                    ]
                )
                
                return completion2.choices[0].message.content
        except json.JSONDecodeError:
            pass  # Not a tool call, return the response as-is
        
        return ai_response
        
    except Exception as e:
        logger.error(f"Error in AI agent chat: {str(e)}")
        raise

@app.post("/api/chat")
async def chat_with_agent(message: dict):
    user_message = message.get("message")
    api_key = message.get("apiKey", "")
    model = message.get("model", "gpt-4.1-mini")
    
    if not user_message:
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    # Use AI agent with MCP tools if API key is provided
    if api_key:
        try:
            response = await chat_with_ai_agent(user_message, api_key, model)
            return {"response": response}
        except Exception as e:
            logger.error(f"Error using AI agent: {str(e)}")
            return {"response": f"Error: {str(e)}"}
    
    # Fallback to basic responses
    return {"response": "Please configure your OpenRouter API key in Settings to enable AI-powered chat with MCP tool access."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8889)

