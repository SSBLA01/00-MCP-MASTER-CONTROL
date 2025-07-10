#!/bin/bash
# Wrapper script for Dobbs-MCP to ensure proper environment

# Change to the project directory
cd "/Users/scottbroock/00 MCP MASTER CONTROL/mathematical-research-mcp"

# Activate virtual environment
source venv/bin/activate

# Export Python path
export PYTHONPATH="/Users/scottbroock/00 MCP MASTER CONTROL/mathematical-research-mcp"

# Run the unified Dobbs MCP server
exec python -m src.servers.dobbs_unified