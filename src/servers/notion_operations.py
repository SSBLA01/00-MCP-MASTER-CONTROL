#!/usr/bin/env python3
"""
Notion Operations for Dobbs MCP
Full control over Notion workspace including page creation, updates, and database operations
"""

import os
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
import aiohttp
import asyncio
from mcp.types import Tool

# Notion API configuration
NOTION_API_VERSION = "2022-06-28"
NOTION_API_BASE = "https://api.notion.com/v1"

# Tool definitions
SEARCH_NOTION_TOOL = Tool(
    name="search_notion",
    description="Search for pages and databases in Notion",
    inputSchema={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Search query"
            },
            "filter": {
                "type": "string",
                "enum": ["page", "database", "all"],
                "description": "Filter by object type",
                "default": "all"
            }
        },
        "required": ["query"]
    }
)

CREATE_NOTION_PAGE_TOOL = Tool(
    name="create_notion_page",
    description="Create a new page in Notion with rich content",
    inputSchema={
        "type": "object",
        "properties": {
            "title": {
                "type": "string",
                "description": "Page title"
            },
            "content": {
                "type": "string",
                "description": "Page content (supports markdown)"
            },
            "parent_page_id": {
                "type": "string",
                "description": "Parent page ID (optional). If not provided, creates in workspace root"
            },
            "icon": {
                "type": "string",
                "description": "Emoji icon for the page (optional)"
            },
            "cover_url": {
                "type": "string",
                "description": "URL for page cover image (optional)"
            }
        },
        "required": ["title", "content"]
    }
)

UPDATE_NOTION_PAGE_TOOL = Tool(
    name="update_notion_page",
    description="Update an existing Notion page",
    inputSchema={
        "type": "object",
        "properties": {
            "page_id": {
                "type": "string",
                "description": "ID of the page to update"
            },
            "title": {
                "type": "string",
                "description": "New title (optional)"
            },
            "content": {
                "type": "string",
                "description": "New content to append (optional)"
            },
            "replace_content": {
                "type": "boolean",
                "description": "Replace entire content instead of appending",
                "default": False
            }
        },
        "required": ["page_id"]
    }
)

ADD_TO_NOTION_DATABASE_TOOL = Tool(
    name="add_to_notion_database",
    description="Add a new entry to a Notion database",
    inputSchema={
        "type": "object",
        "properties": {
            "database_id": {
                "type": "string",
                "description": "Database ID"
            },
            "properties": {
                "type": "object",
                "description": "Properties for the database entry (as JSON object)"
            },
            "content": {
                "type": "string",
                "description": "Page content for the database entry (optional)"
            }
        },
        "required": ["database_id", "properties"]
    }
)

LIST_NOTION_DATABASES_TOOL = Tool(
    name="list_notion_databases",
    description="List all accessible databases in Notion",
    inputSchema={
        "type": "object",
        "properties": {}
    }
)

SYNC_OBSIDIAN_TO_NOTION_TOOL = Tool(
    name="sync_obsidian_to_notion",
    description="Sync an Obsidian note to Notion",
    inputSchema={
        "type": "object",
        "properties": {
            "obsidian_path": {
                "type": "string",
                "description": "Path to Obsidian note (relative to vault)"
            },
            "parent_page_id": {
                "type": "string",
                "description": "Notion parent page ID (optional)"
            },
            "sync_mode": {
                "type": "string",
                "enum": ["create", "update", "sync"],
                "description": "How to sync: create new, update existing, or smart sync",
                "default": "sync"
            }
        },
        "required": ["obsidian_path"]
    }
)

# Helper functions
async def get_notion_headers() -> Dict[str, str]:
    """Get headers for Notion API requests"""
    token = os.getenv('NOTION_TOKEN')
    if not token:
        raise ValueError("NOTION_TOKEN not found in environment variables")
    
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Notion-Version": NOTION_API_VERSION
    }

def markdown_to_notion_blocks(markdown: str) -> List[Dict[str, Any]]:
    """Convert markdown content to Notion blocks"""
    blocks = []
    lines = markdown.split('\n')
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Headers
        if line.startswith('# '):
            blocks.append({
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [{"type": "text", "text": {"content": line[2:]}}]
                }
            })
        elif line.startswith('## '):
            blocks.append({
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": line[3:]}}]
                }
            })
        elif line.startswith('### '):
            blocks.append({
                "object": "block",
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [{"type": "text", "text": {"content": line[4:]}}]
                }
            })
        # Bullet points
        elif line.startswith('- ') or line.startswith('* '):
            blocks.append({
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": line[2:]}}]
                }
            })
        # Code blocks
        elif line.startswith('```'):
            code_lines = []
            language = line[3:].strip()
            i += 1
            while i < len(lines) and not lines[i].startswith('```'):
                code_lines.append(lines[i])
                i += 1
            
            blocks.append({
                "object": "block",
                "type": "code",
                "code": {
                    "rich_text": [{"type": "text", "text": {"content": '\n'.join(code_lines)}}],
                    "language": language or "plain text"
                }
            })
        # Blockquotes
        elif line.startswith('> '):
            blocks.append({
                "object": "block",
                "type": "quote",
                "quote": {
                    "rich_text": [{"type": "text", "text": {"content": line[2:]}}]
                }
            })
        # Regular paragraphs
        elif line.strip():
            blocks.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": line}}]
                }
            })
        
        i += 1
    
    return blocks

# API Functions
async def search_notion(query: str, filter: str = "all") -> Dict[str, Any]:
    """Search Notion for pages and databases"""
    headers = await get_notion_headers()
    
    payload = {
        "query": query,
        "page_size": 20
    }
    
    if filter != "all":
        payload["filter"] = {"property": "object", "value": filter}
    
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{NOTION_API_BASE}/search",
            headers=headers,
            json=payload
        ) as response:
            if response.status == 200:
                data = await response.json()
                results = []
                
                for item in data.get("results", []):
                    result = {
                        "id": item["id"],
                        "type": item["object"],
                        "url": item.get("url", ""),
                        "last_edited": item.get("last_edited_time", "")
                    }
                    
                    # Extract title
                    if item["object"] == "page":
                        props = item.get("properties", {})
                        for prop in props.values():
                            if prop["type"] == "title" and prop["title"]:
                                result["title"] = prop["title"][0]["plain_text"]
                                break
                    elif item["object"] == "database":
                        result["title"] = item.get("title", [{}])[0].get("plain_text", "Untitled")
                    
                    results.append(result)
                
                return {
                    "status": "success",
                    "results": results,
                    "count": len(results)
                }
            else:
                error = await response.text()
                return {
                    "status": "error",
                    "error": f"Search failed: {error}"
                }

async def create_notion_page(
    title: str,
    content: str,
    parent_page_id: Optional[str] = None,
    icon: Optional[str] = None,
    cover_url: Optional[str] = None
) -> Dict[str, Any]:
    """Create a new Notion page"""
    headers = await get_notion_headers()
    
    # Convert markdown to Notion blocks
    blocks = markdown_to_notion_blocks(content)
    
    # Build page data
    page_data = {
        "properties": {
            "title": {
                "title": [{"type": "text", "text": {"content": title}}]
            }
        },
        "children": blocks
    }
    
    # Set parent
    if parent_page_id:
        page_data["parent"] = {"page_id": parent_page_id}
    else:
        # This requires workspace integration - for now, we'll require parent_page_id
        return {
            "status": "error",
            "error": "Parent page ID required. Use search_notion to find a parent page."
        }
    
    # Set icon
    if icon:
        page_data["icon"] = {"type": "emoji", "emoji": icon}
    
    # Set cover
    if cover_url:
        page_data["cover"] = {"type": "external", "external": {"url": cover_url}}
    
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{NOTION_API_BASE}/pages",
            headers=headers,
            json=page_data
        ) as response:
            if response.status == 200:
                data = await response.json()
                return {
                    "status": "success",
                    "page_id": data["id"],
                    "url": data["url"],
                    "created_time": data["created_time"]
                }
            else:
                error = await response.text()
                return {
                    "status": "error",
                    "error": f"Failed to create page: {error}"
                }

async def update_notion_page(
    page_id: str,
    title: Optional[str] = None,
    content: Optional[str] = None,
    replace_content: bool = False
) -> Dict[str, Any]:
    """Update an existing Notion page"""
    headers = await get_notion_headers()
    
    # Update page properties if title provided
    if title:
        page_update = {
            "properties": {
                "title": {
                    "title": [{"type": "text", "text": {"content": title}}]
                }
            }
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.patch(
                f"{NOTION_API_BASE}/pages/{page_id}",
                headers=headers,
                json=page_update
            ) as response:
                if response.status != 200:
                    error = await response.text()
                    return {
                        "status": "error",
                        "error": f"Failed to update title: {error}"
                    }
    
    # Update content if provided
    if content:
        blocks = markdown_to_notion_blocks(content)
        
        if replace_content:
            # First, get existing blocks
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{NOTION_API_BASE}/blocks/{page_id}/children",
                    headers=headers
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        # Delete existing blocks
                        for block in data.get("results", []):
                            await session.delete(
                                f"{NOTION_API_BASE}/blocks/{block['id']}",
                                headers=headers
                            )
        
        # Add new blocks
        async with aiohttp.ClientSession() as session:
            async with session.patch(
                f"{NOTION_API_BASE}/blocks/{page_id}/children",
                headers=headers,
                json={"children": blocks}
            ) as response:
                if response.status != 200:
                    error = await response.text()
                    return {
                        "status": "error",
                        "error": f"Failed to update content: {error}"
                    }
    
    return {
        "status": "success",
        "page_id": page_id,
        "updated": True
    }

async def list_notion_databases() -> Dict[str, Any]:
    """List all accessible databases"""
    results = await search_notion("", filter="database")
    return results

async def add_to_notion_database(
    database_id: str,
    properties: Dict[str, Any],
    content: Optional[str] = None
) -> Dict[str, Any]:
    """Add entry to a Notion database"""
    headers = await get_notion_headers()
    
    page_data = {
        "parent": {"database_id": database_id},
        "properties": properties
    }
    
    if content:
        blocks = markdown_to_notion_blocks(content)
        page_data["children"] = blocks
    
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{NOTION_API_BASE}/pages",
            headers=headers,
            json=page_data
        ) as response:
            if response.status == 200:
                data = await response.json()
                return {
                    "status": "success",
                    "page_id": data["id"],
                    "url": data["url"]
                }
            else:
                error = await response.text()
                return {
                    "status": "error",
                    "error": f"Failed to add to database: {error}"
                }

async def sync_obsidian_to_notion(
    obsidian_path: str,
    parent_page_id: Optional[str] = None,
    sync_mode: str = "sync"
) -> Dict[str, Any]:
    """Sync an Obsidian note to Notion"""
    # Read Obsidian note
    obsidian_vault = os.getenv('OBSIDIAN_VAULT_PATH')
    if not obsidian_vault:
        return {
            "status": "error",
            "error": "OBSIDIAN_VAULT_PATH not configured"
        }
    
    full_path = os.path.join(obsidian_vault, obsidian_path)
    
    if not os.path.exists(full_path):
        return {
            "status": "error",
            "error": f"Obsidian note not found: {obsidian_path}"
        }
    
    # Read content
    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract title from first heading or filename
    title = os.path.basename(obsidian_path).replace('.md', '')
    lines = content.split('\n')
    for line in lines:
        if line.startswith('# '):
            title = line[2:]
            break
    
    # Check if page already exists
    search_results = await search_notion(title)
    existing_page = None
    
    if search_results["status"] == "success":
        for result in search_results["results"]:
            if result.get("title") == title:
                existing_page = result
                break
    
    if sync_mode == "create" or (sync_mode == "sync" and not existing_page):
        # Create new page
        return await create_notion_page(title, content, parent_page_id)
    elif sync_mode == "update" or (sync_mode == "sync" and existing_page):
        # Update existing page
        page_id = existing_page["id"] if existing_page else None
        if not page_id:
            return {
                "status": "error",
                "error": "No existing page found to update"
            }
        return await update_notion_page(page_id, content=content, replace_content=True)
    
    return {
        "status": "error",
        "error": f"Invalid sync mode: {sync_mode}"
    }

# Export tools list
NOTION_OPERATION_TOOLS = [
    SEARCH_NOTION_TOOL,
    CREATE_NOTION_PAGE_TOOL,
    UPDATE_NOTION_PAGE_TOOL,
    ADD_TO_NOTION_DATABASE_TOOL,
    LIST_NOTION_DATABASES_TOOL,
    SYNC_OBSIDIAN_TO_NOTION_TOOL
]