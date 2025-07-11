#!/usr/bin/env python3
"""
Dobbs Unified MCP Server - Optimized Version
Improved startup performance with lazy loading
"""

import asyncio
import json
import sys
import os
from typing import Dict, List, Optional, Any
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.utils.common import setup_logging, load_config, ensure_directory

# Import MCP SDK
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Setup logging
logger = setup_logging("DobbsUnified")

# Load configuration
config = load_config()

# Initialize MCP server
server = Server("dobbs-unified-mcp")

# Lazy-loaded imports
_file_ops = None
_github_ops = None
_research_ops = None
_viz_ops = None
_knowledge_ops = None
_notion_ops = None
_gemini_ops = None

def _ensure_file_ops():
    global _file_ops
    if _file_ops is None:
        from src.servers.file_operations import (
            search_dropbox, list_dropbox_folder, read_dropbox_file, save_to_dropbox,
            copy_file, move_file, delete_file, create_folder,
            FILE_OPERATION_TOOLS
        )
        _file_ops = {
            'search_dropbox': search_dropbox,
            'list_dropbox_folder': list_dropbox_folder,
            'read_dropbox_file': read_dropbox_file,
            'save_to_dropbox': save_to_dropbox,
            'copy_file': copy_file,
            'move_file': move_file,
            'delete_file': delete_file,
            'create_folder': create_folder,
            'tools': FILE_OPERATION_TOOLS
        }
    return _file_ops

def _ensure_github_ops():
    global _github_ops
    if _github_ops is None:
        from src.servers.github_operations import (
            list_github_repos, browse_github_repo, read_github_file, create_github_file,
            get_github_repo_info, list_github_commits, search_github,
            GITHUB_OPERATION_TOOLS
        )
        _github_ops = {
            'list_github_repos': list_github_repos,
            'browse_github_repo': browse_github_repo,
            'read_github_file': read_github_file,
            'create_github_file': create_github_file,
            'get_github_repo_info': get_github_repo_info,
            'list_github_commits': list_github_commits,
            'search_github': search_github,
            'tools': GITHUB_OPERATION_TOOLS
        }
    return _github_ops

# Similar lazy loading for other modules
def _get_all_tools():
    """Get all tools with lazy loading"""
    tools = []
    
    # Always load file operations (most used)
    file_ops = _ensure_file_ops()
    tools.extend(file_ops['tools'])
    
    # Lazy load other tools only when needed
    try:
        github_ops = _ensure_github_ops()
        tools.extend(github_ops['tools'])
    except Exception as e:
        logger.warning(f"Failed to load GitHub tools: {e}")
    
    # Add other tool imports here with similar try/except blocks
    
    return tools

# List available tools
@server.list_tools()
async def handle_list_tools() -> List[Tool]:
    """Return all available tools"""
    return _get_all_tools()

# Tool handler
@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> List[TextContent]:
    """Handle all tool calls with lazy loading"""
    try:
        # File operations (most common)
        if name in ['search_dropbox', 'list_dropbox_folder', 'read_dropbox_file', 'save_to_dropbox',
                    'copy_file', 'move_file', 'delete_file', 'create_folder']:
            ops = _ensure_file_ops()
            result = await ops[name](**arguments)
        
        # GitHub operations
        elif name in ['list_github_repos', 'browse_github_repo', 'read_github_file', 
                      'create_github_file', 'get_github_repo_info', 'list_github_commits', 'search_github']:
            ops = _ensure_github_ops()
            result = await ops[name](**arguments)
        
        # Add other operations here...
        
        else:
            result = {"error": f"Unknown tool: {name}"}
        
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    
    except Exception as e:
        logger.error(f"Error handling tool {name}: {e}")
        return [TextContent(type="text", text=json.dumps({
            "error": str(e),
            "tool": name,
            "suggestion": "Check the parameters and try again"
        }, indent=2))]

async def main():
    """Main entry point for the MCP server"""
    logger.info("Starting Dobbs Unified MCP Server (Optimized)...")
    logger.info(f"Dropbox base path: {config['paths']['dropbox_base']}")
    logger.info(f"Obsidian vault: {config['paths']['obsidian_vault']}")
    
    # Don't count tools at startup to improve performance
    logger.info("Server ready for connections")
    
    # Ensure required directories exist
    ensure_directory(config['paths']['obsidian_vault'])
    ensure_directory(config['paths']['manim_output'])
    
    # Run the server
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="dobbs-unified-mcp",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())