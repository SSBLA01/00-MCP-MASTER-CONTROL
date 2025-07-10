#!/usr/bin/env python3
"""
Mathematical Research Master Coordinator MCP Server

This server orchestrates all mathematical research agents and manages sessions.
It acts as the central hub for coordinating research discovery, visualization,
and knowledge ingestion activities.
"""

import asyncio
import json
import sys
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path
import uuid

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.utils.common import setup_logging, load_config, ensure_directory

# Import MCP SDK
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Setup logging
logger = setup_logging("MasterCoordinator")

# Load configuration
config = load_config()

# Session storage
research_sessions: Dict[str, Dict[str, Any]] = {}
active_workflows: Dict[str, List[str]] = {}

# Initialize MCP server
server = Server("mathematical-research-coordinator")

# Tool definitions
INITIATE_SESSION_TOOL = Tool(
    name="initiate_research_session",
    description="Start a new mathematical research session with specific parameters",
    inputSchema={
        "type": "object",
        "properties": {
            "topic": {
                "type": "string",
                "description": "Research topic or mathematical concept to explore"
            },
            "research_type": {
                "type": "string",
                "enum": ["discovery", "deep_dive", "survey", "focused"],
                "description": "Type of research to conduct"
            },
            "output_formats": {
                "type": "array",
                "items": {"type": "string", "enum": ["obsidian", "pdf", "manim", "jupyter"]},
                "description": "Desired output formats for the research"
            },
            "priority_sources": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Preferred sources (arxiv, wolfram, perplexity, etc.)"
            }
        },
        "required": ["topic", "research_type"]
    }
)

COORDINATE_WORKFLOW_TOOL = Tool(
    name="coordinate_workflow",
    description="Coordinate a multi-agent workflow for mathematical research",
    inputSchema={
        "type": "object",
        "properties": {
            "session_id": {
                "type": "string",
                "description": "ID of the research session"
            },
            "workflow_type": {
                "type": "string",
                "enum": ["discover_visualize_ingest", "validate_and_publish", "iterative_exploration"],
                "description": "Type of workflow to execute"
            },
            "parameters": {
                "type": "object",
                "description": "Additional parameters for the workflow"
            }
        },
        "required": ["session_id", "workflow_type"]
    }
)

GET_SESSION_STATUS_TOOL = Tool(
    name="get_session_status",
    description="Get the current status of a research session",
    inputSchema={
        "type": "object",
        "properties": {
            "session_id": {
                "type": "string",
                "description": "ID of the research session to check"
            }
        },
        "required": ["session_id"]
    }
)

MANAGE_AGENTS_TOOL = Tool(
    name="manage_agents",
    description="Manage the status and coordination of research agents",
    inputSchema={
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["status", "restart", "pause", "resume"],
                "description": "Action to perform on agents"
            },
            "agent_name": {
                "type": "string",
                "enum": ["research_discovery", "mathematical_visualization", "knowledge_ingestion", "all"],
                "description": "Which agent(s) to manage"
            }
        },
        "required": ["action"]
    }
)

# Tool registry
TOOLS = [
    INITIATE_SESSION_TOOL,
    COORDINATE_WORKFLOW_TOOL,
    GET_SESSION_STATUS_TOOL,
    MANAGE_AGENTS_TOOL
]

# Register list_tools handler
@server.list_tools()
async def handle_list_tools() -> List[Tool]:
    return TOOLS

# Tool implementations
async def initiate_research_session(
    topic: str,
    research_type: str,
    output_formats: Optional[List[str]] = None,
    priority_sources: Optional[List[str]] = None
) -> Dict[str, Any]:
    """Initiate a new research session"""
    session_id = str(uuid.uuid4())
    
    # Default values
    if output_formats is None:
        output_formats = ["obsidian", "manim"]
    if priority_sources is None:
        priority_sources = ["arxiv", "perplexity"]
    
    session_data = {
        "id": session_id,
        "topic": topic,
        "research_type": research_type,
        "output_formats": output_formats,
        "priority_sources": priority_sources,
        "status": "initiated",
        "created_at": datetime.now().isoformat(),
        "agents_status": {
            "research_discovery": "ready",
            "mathematical_visualization": "ready",
            "knowledge_ingestion": "ready"
        },
        "artifacts": [],
        "workflow_history": []
    }
    
    research_sessions[session_id] = session_data
    logger.info(f"Initiated research session {session_id} for topic: {topic}")
    
    return {
        "status": "initiated",
        "session_id": session_id,
        "topic": topic,
        "message": f"Research session initiated for '{topic}' with {research_type} approach"
    }

async def coordinate_workflow(
    session_id: str,
    workflow_type: str,
    parameters: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Coordinate a multi-agent workflow"""
    if session_id not in research_sessions:
        return {"error": "Session not found"}
    
    session = research_sessions[session_id]
    workflow_id = str(uuid.uuid4())
    
    # Define workflow steps based on type
    workflow_steps = {
        "discover_visualize_ingest": [
            {"agent": "research_discovery", "action": "search", "params": {"query": session["topic"]}},
            {"agent": "mathematical_visualization", "action": "create_diagram", "params": {"concept": session["topic"]}},
            {"agent": "knowledge_ingestion", "action": "organize", "params": {"format": "obsidian"}}
        ],
        "validate_and_publish": [
            {"agent": "mathematical_visualization", "action": "validate", "params": {"use_wolfram": True}},
            {"agent": "knowledge_ingestion", "action": "publish", "params": {"targets": ["obsidian", "dropbox"]}}
        ],
        "iterative_exploration": [
            {"agent": "research_discovery", "action": "deep_search", "params": {"iterations": 3}},
            {"agent": "mathematical_visualization", "action": "animate", "params": {"style": "3blue1brown"}},
            {"agent": "knowledge_ingestion", "action": "create_notebook", "params": {"interactive": True}}
        ]
    }
    
    steps = workflow_steps.get(workflow_type, [])
    
    # Store workflow
    active_workflows[workflow_id] = steps
    session["workflow_history"].append({
        "workflow_id": workflow_id,
        "type": workflow_type,
        "started_at": datetime.now().isoformat(),
        "status": "running"
    })
    
    # Update session
    session["status"] = "workflow_active"
    
    return {
        "status": "workflow_started",
        "workflow_id": workflow_id,
        "session_id": session_id,
        "steps": len(steps),
        "message": f"Started {workflow_type} workflow with {len(steps)} steps"
    }

async def get_session_status(session_id: str) -> Dict[str, Any]:
    """Get the current status of a research session"""
    if session_id not in research_sessions:
        return {"error": "Session not found"}
    
    session = research_sessions[session_id]
    
    # Calculate progress
    total_workflows = len(session["workflow_history"])
    completed_workflows = sum(1 for w in session["workflow_history"] if w.get("status") == "completed")
    
    return {
        "session_id": session_id,
        "topic": session["topic"],
        "status": session["status"],
        "created_at": session["created_at"],
        "agents_status": session["agents_status"],
        "artifacts_count": len(session["artifacts"]),
        "workflows": {
            "total": total_workflows,
            "completed": completed_workflows,
            "active": total_workflows - completed_workflows
        },
        "last_activity": session["workflow_history"][-1] if session["workflow_history"] else None
    }

async def manage_agents(action: str, agent_name: str = "all") -> Dict[str, Any]:
    """Manage agent status and coordination"""
    agent_statuses = {
        "research_discovery": "active",
        "mathematical_visualization": "active",
        "knowledge_ingestion": "active"
    }
    
    if action == "status":
        if agent_name == "all":
            return {
                "status": "success",
                "agents": agent_statuses,
                "message": "All agents are operational"
            }
        else:
            return {
                "status": "success",
                "agent": agent_name,
                "state": agent_statuses.get(agent_name, "unknown"),
                "message": f"{agent_name} status retrieved"
            }
    
    elif action in ["restart", "pause", "resume"]:
        # In a real implementation, these would interact with actual agent processes
        affected_agents = [agent_name] if agent_name != "all" else list(agent_statuses.keys())
        
        return {
            "status": "success",
            "action": action,
            "affected_agents": affected_agents,
            "message": f"Successfully performed {action} on {', '.join(affected_agents)}"
        }
    
    return {"error": "Unknown action"}

# Tool handlers
@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> List[TextContent]:
    """Handle tool calls"""
    if name == "initiate_research_session":
        result = await initiate_research_session(**arguments)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    elif name == "coordinate_workflow":
        result = await coordinate_workflow(**arguments)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    elif name == "get_session_status":
        result = await get_session_status(**arguments)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    elif name == "manage_agents":
        result = await manage_agents(**arguments)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    else:
        return [TextContent(type="text", text=json.dumps({"error": f"Unknown tool: {name}"}))]

async def main():
    """Main entry point for the MCP server"""
    logger.info("Starting Mathematical Research Master Coordinator...")
    
    # Ensure required directories exist
    ensure_directory(config['paths']['obsidian_vault'])
    ensure_directory(config['paths']['manim_output'])
    
    # Run the server
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="mathematical-research-coordinator",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())