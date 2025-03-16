from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse
from typing import Iterator
import asyncio
import json

app = FastAPI(
    title="Simple MCP Server",
    description="Beginner-friendly MCP Server with SSE support",
    version="1.0.0"
)

# CORS for n8n
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://primary-production-35d4.up.railway.app",
        "http://localhost:5678",
        "http://localhost:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store active tools
AVAILABLE_TOOLS = {
    "firecrawl": {
        "name": "firecrawl",
        "description": "Extract content from websites",
        "parameters": {
            "url": "string",
            "max_pages": "integer",
            "same_domain": "boolean"
        }
    }
}

async def event_generator(request: Request) -> Iterator[str]:
    """Generate SSE events with available tools."""
    while True:
        # Check if client is still connected
        if await request.is_disconnected():
            break

        # Send available tools
        yield json.dumps({
            "type": "tools",
            "data": AVAILABLE_TOOLS
        })
        
        await asyncio.sleep(5)  # Update every 5 seconds

@app.get("/")
async def root():
    return {
        "message": "Welcome to Simple MCP Server",
        "status": "operational"
    }

@app.get("/sse")
async def sse(request: Request):
    """SSE endpoint for tool discovery."""
    return EventSourceResponse(event_generator(request))

@app.get("/tools")
async def list_tools():
    """List all available tools."""
    return AVAILABLE_TOOLS

# Import and include Firecrawl routes
from .routers import firecrawl
app.include_router(firecrawl.router) 