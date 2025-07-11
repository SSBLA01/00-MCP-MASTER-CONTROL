#!/bin/bash
# Wrapper script for Dobbs-MCP to ensure proper environment

# Error handling
set -e
trap 'echo "Error occurred at line $LINENO" >&2' ERR

# Change to the project directory
cd "/Users/scottbroock/00 MCP MASTER CONTROL/mathematical-research-mcp"

# Activate virtual environment
source venv/bin/activate

# Export Python path
export PYTHONPATH="/Users/scottbroock/00 MCP MASTER CONTROL/mathematical-research-mcp"

# Add small delay to prevent race conditions
sleep 0.5

# Run the unified Dobbs MCP server with unbuffered output
exec python -u -m src.servers.dobbs_unified