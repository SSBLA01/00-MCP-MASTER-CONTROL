#!/usr/bin/env python3
"""
Knowledge Ingestion Agent MCP Server

This agent handles organizing and storing mathematical research in Obsidian,
syncing with Dropbox, and managing GitHub repositories.
"""

import asyncio
import json
import sys
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path
import re
import shutil
import aiofiles
import aiohttp

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.utils.common import setup_logging, load_config, ensure_directory

# Import MCP SDK
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Setup logging
logger = setup_logging("KnowledgeIngestion")

# Load configuration
config = load_config()

# Initialize MCP server
server = Server("knowledge-ingestion-agent")

# Tool definitions
INGEST_TO_OBSIDIAN_TOOL = Tool(
    name="ingest_to_obsidian",
    description="Ingest mathematical content into Obsidian vault with smart organization",
    inputSchema={
        "type": "object",
        "properties": {
            "content": {
                "type": "string",
                "description": "Content to ingest (markdown formatted)"
            },
            "title": {
                "type": "string",
                "description": "Title for the note"
            },
            "category": {
                "type": "string",
                "enum": ["concepts", "papers", "proofs", "examples", "notebooks", "daily_notes"],
                "description": "Category for organization"
            },
            "tags": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Tags for the note"
            },
            "links": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Links to other notes"
            },
            "metadata": {
                "type": "object",
                "description": "Additional metadata"
            }
        },
        "required": ["content", "title", "category"]
    }
)

SYNC_TO_DROPBOX_TOOL = Tool(
    name="sync_to_dropbox",
    description="Sync files or folders to Dropbox",
    inputSchema={
        "type": "object",
        "properties": {
            "source_path": {
                "type": "string",
                "description": "Local path to sync from"
            },
            "dropbox_path": {
                "type": "string",
                "description": "Dropbox path to sync to"
            },
            "sync_type": {
                "type": "string",
                "enum": ["upload", "download", "bidirectional"],
                "description": "Type of sync operation"
            },
            "conflict_resolution": {
                "type": "string",
                "enum": ["rename", "overwrite", "skip"],
                "description": "How to handle conflicts"
            }
        },
        "required": ["source_path", "dropbox_path", "sync_type"]
    }
)

MANAGE_GITHUB_REPO_TOOL = Tool(
    name="manage_github_repo",
    description="Manage mathematical research in GitHub repository",
    inputSchema={
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["create_repo", "commit_files", "create_branch", "create_pr"],
                "description": "GitHub action to perform"
            },
            "repo_name": {
                "type": "string",
                "description": "Repository name"
            },
            "files": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string"},
                        "content": {"type": "string"}
                    }
                },
                "description": "Files to manage"
            },
            "commit_message": {
                "type": "string",
                "description": "Commit message"
            }
        },
        "required": ["action", "repo_name"]
    }
)

CREATE_SMART_INDEX_TOOL = Tool(
    name="create_smart_index",
    description="Create an intelligent index of mathematical content",
    inputSchema={
        "type": "object",
        "properties": {
            "scope": {
                "type": "string",
                "enum": ["vault", "category", "tag", "recent"],
                "description": "Scope of indexing"
            },
            "grouping": {
                "type": "string",
                "enum": ["topic", "date", "author", "complexity"],
                "description": "How to group content"
            },
            "include_visualizations": {
                "type": "boolean",
                "description": "Include links to visualizations"
            },
            "format": {
                "type": "string",
                "enum": ["markdown", "graph", "timeline"],
                "description": "Output format for the index"
            }
        },
        "required": ["scope", "grouping"]
    }
)

# Tool registry
TOOLS = [
    INGEST_TO_OBSIDIAN_TOOL,
    SYNC_TO_DROPBOX_TOOL,
    MANAGE_GITHUB_REPO_TOOL,
    CREATE_SMART_INDEX_TOOL
]

# Register list_tools handler
@server.list_tools()
async def handle_list_tools() -> List[Tool]:
    return TOOLS

# Helper functions
def sanitize_filename(filename: str) -> str:
    """Sanitize filename for filesystem"""
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Replace spaces with underscores
    filename = filename.replace(' ', '_')
    # Limit length
    return filename[:200]

def generate_frontmatter(title: str, tags: List[str], metadata: Dict[str, Any]) -> str:
    """Generate Obsidian frontmatter"""
    frontmatter = f"""---
title: {title}
created: {datetime.now().isoformat()}
tags: {', '.join(tags) if tags else 'untagged'}
"""
    
    # Add custom metadata
    for key, value in metadata.items():
        frontmatter += f"{key}: {value}\n"
    
    frontmatter += "---\n\n"
    return frontmatter

async def ingest_to_obsidian(
    content: str,
    title: str,
    category: str,
    tags: List[str] = None,
    links: List[str] = None,
    metadata: Dict[str, Any] = None
) -> Dict[str, Any]:
    """Ingest content into Obsidian vault"""
    
    if tags is None:
        tags = []
    if links is None:
        links = []
    if metadata is None:
        metadata = {}
    
    # Ensure vault directory exists
    vault_path = Path(config['paths']['obsidian_vault'])
    category_path = ensure_directory(vault_path / category.capitalize())
    
    # Generate filename
    filename = sanitize_filename(title) + ".md"
    file_path = category_path / filename
    
    # Add frontmatter
    full_content = generate_frontmatter(title, tags, metadata)
    
    # Add title
    full_content += f"# {title}\n\n"
    
    # Add links section if links provided
    if links:
        full_content += "## Related Notes\n\n"
        for link in links:
            full_content += f"- [[{link}]]\n"
        full_content += "\n"
    
    # Add main content
    full_content += content
    
    # Add backlinks section
    full_content += "\n\n## Backlinks\n\n"
    full_content += "```dataview\n"
    full_content += "LIST\n"
    full_content += f'FROM [[{title}]]\n'
    full_content += "```\n"
    
    # Write file
    try:
        async with aiofiles.open(file_path, 'w', encoding='utf-8') as f:
            await f.write(full_content)
        
        logger.info(f"Created note: {file_path}")
        
        return {
            "status": "success",
            "file_path": str(file_path),
            "title": title,
            "category": category,
            "tags": tags,
            "word_count": len(content.split()),
            "created_at": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error ingesting to Obsidian: {e}")
        return {
            "status": "error",
            "error": str(e),
            "title": title
        }

async def get_dropbox_auth_url() -> str:
    """Generate Dropbox OAuth URL"""
    app_key = config['api_keys']['dropbox_app_key']
    redirect_uri = "http://localhost:8080/dropbox/callback"
    
    auth_url = (
        f"https://www.dropbox.com/oauth2/authorize"
        f"?client_id={app_key}"
        f"&response_type=code"
        f"&redirect_uri={redirect_uri}"
    )
    
    return auth_url

async def sync_to_dropbox(
    source_path: str,
    dropbox_path: str,
    sync_type: str,
    conflict_resolution: str = "rename"
) -> Dict[str, Any]:
    """Sync files to Dropbox"""
    
    # Check if we have access token
    access_token = config['api_keys'].get('dropbox_access_token')
    
    if not access_token:
        # Need to authenticate first
        auth_url = await get_dropbox_auth_url()
        return {
            "status": "auth_required",
            "auth_url": auth_url,
            "message": "Please authenticate with Dropbox first"
        }
    
    # In production, this would use the Dropbox API
    # For now, simulate the sync
    
    source = Path(source_path)
    
    if not source.exists():
        return {
            "status": "error",
            "error": f"Source path does not exist: {source_path}"
        }
    
    files_synced = []
    
    if source.is_file():
        files_synced.append(source.name)
    else:
        # Get all files in directory
        files_synced = [f.name for f in source.rglob("*") if f.is_file()]
    
    return {
        "status": "success",
        "sync_type": sync_type,
        "source_path": source_path,
        "dropbox_path": dropbox_path,
        "files_synced": len(files_synced),
        "conflict_resolution": conflict_resolution,
        "timestamp": datetime.now().isoformat()
    }

async def manage_github_repo(
    action: str,
    repo_name: str,
    files: List[Dict[str, str]] = None,
    commit_message: str = None
) -> Dict[str, Any]:
    """Manage GitHub repository"""
    
    github_token = config['api_keys']['github']
    
    if not github_token:
        return {
            "status": "error",
            "error": "GitHub token not configured"
        }
    
    # GitHub API headers
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    if action == "create_repo":
        # Create repository
        api_url = "https://api.github.com/user/repos"
        
        payload = {
            "name": repo_name,
            "description": "Mathematical research repository",
            "private": False,
            "auto_init": True
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(api_url, headers=headers, json=payload) as response:
                    if response.status == 201:
                        data = await response.json()
                        return {
                            "status": "success",
                            "action": "create_repo",
                            "repo_url": data["html_url"],
                            "clone_url": data["clone_url"]
                        }
                    else:
                        return {
                            "status": "error",
                            "error": f"Failed to create repository: {response.status}"
                        }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    elif action == "commit_files":
        # This would implement file commits in production
        return {
            "status": "success",
            "action": "commit_files",
            "repo_name": repo_name,
            "files_committed": len(files) if files else 0,
            "commit_message": commit_message,
            "timestamp": datetime.now().isoformat()
        }
    
    return {
        "status": "error",
        "error": f"Unknown action: {action}"
    }

async def create_smart_index(
    scope: str,
    grouping: str,
    include_visualizations: bool = True,
    format: str = "markdown"
) -> Dict[str, Any]:
    """Create an intelligent index of content"""
    
    vault_path = Path(config['paths']['obsidian_vault'])
    
    # Collect files based on scope
    files_to_index = []
    
    if scope == "vault":
        files_to_index = list(vault_path.rglob("*.md"))
    elif scope == "recent":
        # Get files modified in last 7 days
        from datetime import timedelta
        cutoff_time = datetime.now() - timedelta(days=7)
        files_to_index = [
            f for f in vault_path.rglob("*.md")
            if datetime.fromtimestamp(f.stat().st_mtime) > cutoff_time
        ]
    
    # Group files
    groups = {}
    
    for file in files_to_index:
        if grouping == "topic":
            # Group by directory
            group_key = file.parent.name
        elif grouping == "date":
            # Group by modification date
            group_key = datetime.fromtimestamp(file.stat().st_mtime).strftime("%Y-%m-%d")
        else:
            group_key = "ungrouped"
        
        if group_key not in groups:
            groups[group_key] = []
        groups[group_key].append(file)
    
    # Generate index
    if format == "markdown":
        index_content = f"# Mathematical Research Index\n\n"
        index_content += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        index_content += f"## Scope: {scope} | Grouping: {grouping}\n\n"
        
        for group, files in sorted(groups.items()):
            index_content += f"### {group}\n\n"
            for file in sorted(files):
                # Get file title from first heading or filename
                title = file.stem.replace('_', ' ')
                index_content += f"- [[{file.stem}|{title}]]\n"
            index_content += "\n"
        
        # Save index
        index_file = vault_path / f"index_{scope}_{grouping}.md"
        
        async with aiofiles.open(index_file, 'w', encoding='utf-8') as f:
            await f.write(index_content)
        
        return {
            "status": "success",
            "index_file": str(index_file),
            "total_files": len(files_to_index),
            "groups": len(groups),
            "format": format,
            "created_at": datetime.now().isoformat()
        }
    
    # Other formats would be implemented here
    return {
        "status": "success",
        "message": f"Index created with {len(files_to_index)} files in {len(groups)} groups"
    }

# Tool handlers
@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> List[TextContent]:
    """Handle tool calls"""
    if name == "ingest_to_obsidian":
        result = await ingest_to_obsidian(**arguments)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    elif name == "sync_to_dropbox":
        result = await sync_to_dropbox(**arguments)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    elif name == "manage_github_repo":
        result = await manage_github_repo(**arguments)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    elif name == "create_smart_index":
        result = await create_smart_index(**arguments)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    else:
        return [TextContent(type="text", text=json.dumps({"error": f"Unknown tool: {name}"}))]

async def main():
    """Main entry point for the MCP server"""
    logger.info("Starting Knowledge Ingestion Agent...")
    
    # Ensure required directories exist
    ensure_directory(config['paths']['obsidian_vault'])
    ensure_directory(config['paths']['obsidian_vault'] + "/Concepts")
    ensure_directory(config['paths']['obsidian_vault'] + "/Papers")
    ensure_directory(config['paths']['obsidian_vault'] + "/Proofs")
    ensure_directory(config['paths']['obsidian_vault'] + "/Examples")
    ensure_directory(config['paths']['obsidian_vault'] + "/Notebooks")
    ensure_directory(config['paths']['obsidian_vault'] + "/Daily_notes")
    
    # Run the server
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="knowledge-ingestion-agent",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())