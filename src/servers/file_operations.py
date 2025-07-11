#!/usr/bin/env python3
"""
File Operations MCP Server Component
Handles searching, reading, and managing files in Dropbox
"""

import os
import glob
from pathlib import Path
from typing import List, Dict, Any, Optional
import json
from datetime import datetime

from mcp.types import Tool, TextContent

# Tool definitions for file operations
SEARCH_DROPBOX_TOOL = Tool(
    name="search_dropbox",
    description="Search for files or folders in your Dropbox by name or content",
    inputSchema={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "What to search for (file name, folder name, or content)"
            },
            "search_type": {
                "type": "string",
                "enum": ["filename", "content", "folders"],
                "description": "Type of search to perform"
            },
            "path": {
                "type": "string",
                "description": "Specific Dropbox path to search in (optional)"
            }
        },
        "required": ["query", "search_type"]
    }
)

LIST_DROPBOX_FOLDER_TOOL = Tool(
    name="list_dropbox_folder",
    description="List contents of a Dropbox folder",
    inputSchema={
        "type": "object",
        "properties": {
            "folder_path": {
                "type": "string",
                "description": "Path to the folder (e.g., 'Research', 'Projects/Math')"
            },
            "include_hidden": {
                "type": "boolean",
                "description": "Include hidden files",
                "default": False
            }
        },
        "required": ["folder_path"]
    }
)

READ_DROPBOX_FILE_TOOL = Tool(
    name="read_dropbox_file",
    description="Read contents of a file from Dropbox",
    inputSchema={
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "Path to the file in Dropbox"
            }
        },
        "required": ["file_path"]
    }
)

SAVE_TO_DROPBOX_TOOL = Tool(
    name="save_to_dropbox",
    description="Save content to a file in Dropbox",
    inputSchema={
        "type": "object",
        "properties": {
            "content": {
                "type": "string",
                "description": "Content to save"
            },
            "file_path": {
                "type": "string",
                "description": "Where to save in Dropbox (e.g., 'Research/notes.md')"
            },
            "overwrite": {
                "type": "boolean",
                "description": "Overwrite if file exists",
                "default": False
            }
        },
        "required": ["content", "file_path"]
    }
)

# File operation implementations
async def search_dropbox(query: str, search_type: str, path: Optional[str] = None) -> Dict[str, Any]:
    """Search Dropbox for files or folders"""
    dropbox_base = "/Users/scottbroock/Dropbox"
    search_path = os.path.join(dropbox_base, path) if path else dropbox_base
    
    results = []
    
    if search_type == "filename":
        # Search for files by name
        for root, dirs, files in os.walk(search_path):
            for file in files:
                if query.lower() in file.lower():
                    full_path = os.path.join(root, file)
                    relative_path = os.path.relpath(full_path, dropbox_base)
                    results.append({
                        "type": "file",
                        "name": file,
                        "path": relative_path,
                        "full_path": full_path,
                        "size": os.path.getsize(full_path),
                        "modified": datetime.fromtimestamp(os.path.getmtime(full_path)).isoformat()
                    })
    
    elif search_type == "folders":
        # Search for folders
        for root, dirs, files in os.walk(search_path):
            for dir_name in dirs:
                if query.lower() in dir_name.lower():
                    full_path = os.path.join(root, dir_name)
                    relative_path = os.path.relpath(full_path, dropbox_base)
                    results.append({
                        "type": "folder",
                        "name": dir_name,
                        "path": relative_path,
                        "full_path": full_path,
                        "item_count": len(os.listdir(full_path))
                    })
    
    elif search_type == "content":
        # Search file contents
        text_extensions = ['.txt', '.md', '.tex', '.py', '.json', '.yaml', '.yml']
        for root, dirs, files in os.walk(search_path):
            for file in files:
                if any(file.endswith(ext) for ext in text_extensions):
                    full_path = os.path.join(root, file)
                    try:
                        with open(full_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            if query.lower() in content.lower():
                                relative_path = os.path.relpath(full_path, dropbox_base)
                                # Find the line containing the query
                                lines = content.split('\n')
                                matching_lines = []
                                for i, line in enumerate(lines):
                                    if query.lower() in line.lower():
                                        matching_lines.append({
                                            "line_number": i + 1,
                                            "content": line.strip()
                                        })
                                
                                results.append({
                                    "type": "file",
                                    "name": file,
                                    "path": relative_path,
                                    "full_path": full_path,
                                    "matches": matching_lines[:5]  # First 5 matches
                                })
                    except:
                        pass  # Skip files that can't be read
    
    return {
        "query": query,
        "search_type": search_type,
        "results_count": len(results),
        "results": results[:50]  # Limit to 50 results
    }

async def list_dropbox_folder(folder_path: str, include_hidden: bool = False) -> Dict[str, Any]:
    """List contents of a Dropbox folder"""
    dropbox_base = "/Users/scottbroock/Dropbox"
    full_path = os.path.join(dropbox_base, folder_path.strip('/'))
    
    if not os.path.exists(full_path):
        return {
            "error": f"Folder not found: {folder_path}",
            "suggestion": "Try searching for the folder name first"
        }
    
    items = []
    
    for item in os.listdir(full_path):
        if not include_hidden and item.startswith('.'):
            continue
            
        item_path = os.path.join(full_path, item)
        stat = os.stat(item_path)
        
        if os.path.isdir(item_path):
            items.append({
                "type": "folder",
                "name": item,
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "item_count": len(os.listdir(item_path))
            })
        else:
            items.append({
                "type": "file",
                "name": item,
                "size": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
            })
    
    # Sort folders first, then files
    items.sort(key=lambda x: (x['type'] != 'folder', x['name'].lower()))
    
    return {
        "folder": folder_path,
        "full_path": full_path,
        "item_count": len(items),
        "items": items
    }

async def read_dropbox_file(file_path: str) -> Dict[str, Any]:
    """Read a file from Dropbox"""
    dropbox_base = "/Users/scottbroock/Dropbox"
    full_path = os.path.join(dropbox_base, file_path.strip('/'))
    
    if not os.path.exists(full_path):
        return {
            "error": f"File not found: {file_path}",
            "suggestion": "Check the file path or search for the file"
        }
    
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return {
            "file_path": file_path,
            "content": content,
            "size": len(content),
            "lines": content.count('\n') + 1
        }
    except Exception as e:
        return {
            "error": f"Could not read file: {str(e)}",
            "file_path": file_path
        }

async def save_to_dropbox(content: str, file_path: str, overwrite: bool = False) -> Dict[str, Any]:
    """Save content to Dropbox"""
    dropbox_base = "/Users/scottbroock/Dropbox"
    full_path = os.path.join(dropbox_base, file_path.strip('/'))
    
    # Create directory if needed
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    
    if os.path.exists(full_path) and not overwrite:
        return {
            "error": "File already exists",
            "suggestion": "Set overwrite=true or choose a different filename"
        }
    
    try:
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return {
            "status": "success",
            "file_path": file_path,
            "full_path": full_path,
            "size": len(content),
            "created": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "error": f"Could not save file: {str(e)}",
            "file_path": file_path
        }

async def copy_file(source_path: str, dest_path: str) -> Dict[str, Any]:
    """Copy a file within Dropbox (supports binary files)"""
    import shutil
    
    dropbox_base = "/Users/scottbroock/Dropbox"
    source_full = os.path.join(dropbox_base, source_path.strip('/'))
    dest_full = os.path.join(dropbox_base, dest_path.strip('/'))
    
    if not os.path.exists(source_full):
        return {
            "error": f"Source file does not exist: {source_path}"
        }
    
    # Create destination directory if needed
    os.makedirs(os.path.dirname(dest_full), exist_ok=True)
    
    try:
        shutil.copy2(source_full, dest_full)  # copy2 preserves metadata
        return {
            "status": "success",
            "source": source_path,
            "destination": dest_path,
            "size": os.path.getsize(dest_full)
        }
    except Exception as e:
        return {
            "error": f"Could not copy file: {str(e)}"
        }

async def move_file(source_path: str, dest_path: str) -> Dict[str, Any]:
    """Move a file within Dropbox"""
    import shutil
    
    dropbox_base = "/Users/scottbroock/Dropbox"
    source_full = os.path.join(dropbox_base, source_path.strip('/'))
    dest_full = os.path.join(dropbox_base, dest_path.strip('/'))
    
    if not os.path.exists(source_full):
        return {
            "error": f"Source file does not exist: {source_path}"
        }
    
    # Create destination directory if needed
    os.makedirs(os.path.dirname(dest_full), exist_ok=True)
    
    try:
        shutil.move(source_full, dest_full)
        return {
            "status": "success",
            "source": source_path,
            "destination": dest_path
        }
    except Exception as e:
        return {
            "error": f"Could not move file: {str(e)}"
        }

async def delete_file(path: str) -> Dict[str, Any]:
    """Delete a file or folder in Dropbox"""
    import shutil
    
    dropbox_base = "/Users/scottbroock/Dropbox"
    full_path = os.path.join(dropbox_base, path.strip('/'))
    
    if not os.path.exists(full_path):
        return {
            "error": f"Path does not exist: {path}"
        }
    
    try:
        if os.path.isdir(full_path):
            shutil.rmtree(full_path)
            return {
                "status": "success",
                "deleted": path,
                "type": "directory"
            }
        else:
            os.remove(full_path)
            return {
                "status": "success",
                "deleted": path,
                "type": "file"
            }
    except Exception as e:
        return {
            "error": f"Could not delete: {str(e)}"
        }

async def create_folder(path: str) -> Dict[str, Any]:
    """Create a folder in Dropbox"""
    dropbox_base = "/Users/scottbroock/Dropbox"
    full_path = os.path.join(dropbox_base, path.strip('/'))
    
    try:
        os.makedirs(full_path, exist_ok=True)
        return {
            "status": "success",
            "created": path,
            "full_path": full_path
        }
    except Exception as e:
        return {
            "error": f"Could not create folder: {str(e)}"
        }

# New file operation tools
COPY_FILE_TOOL = Tool(
    name="copy_file",
    description="Copy a file within Dropbox (supports binary files)",
    inputSchema={
        "type": "object",
        "properties": {
            "source_path": {
                "type": "string",
                "description": "Source path relative to Dropbox root"
            },
            "dest_path": {
                "type": "string",
                "description": "Destination path relative to Dropbox root"
            }
        },
        "required": ["source_path", "dest_path"]
    }
)

MOVE_FILE_TOOL = Tool(
    name="move_file",
    description="Move a file within Dropbox",
    inputSchema={
        "type": "object",
        "properties": {
            "source_path": {
                "type": "string",
                "description": "Source path relative to Dropbox root"
            },
            "dest_path": {
                "type": "string",
                "description": "Destination path relative to Dropbox root"
            }
        },
        "required": ["source_path", "dest_path"]
    }
)

DELETE_FILE_TOOL = Tool(
    name="delete_file",
    description="Delete a file or folder in Dropbox",
    inputSchema={
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Path to delete relative to Dropbox root"
            }
        },
        "required": ["path"]
    }
)

CREATE_FOLDER_TOOL = Tool(
    name="create_folder",
    description="Create a folder in Dropbox",
    inputSchema={
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Folder path relative to Dropbox root"
            }
        },
        "required": ["path"]
    }
)

# Export tools list
FILE_OPERATION_TOOLS = [
    SEARCH_DROPBOX_TOOL,
    LIST_DROPBOX_FOLDER_TOOL,
    READ_DROPBOX_FILE_TOOL,
    SAVE_TO_DROPBOX_TOOL,
    COPY_FILE_TOOL,
    MOVE_FILE_TOOL,
    DELETE_FILE_TOOL,
    CREATE_FOLDER_TOOL
]