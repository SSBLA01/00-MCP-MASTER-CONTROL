#!/usr/bin/env python3
"""
GitHub Operations MCP Server Component
Provides comprehensive GitHub functionality
"""

import os
import json
import aiohttp
from typing import List, Dict, Any, Optional
from datetime import datetime
import base64
import ssl
import certifi

from mcp.types import Tool, TextContent

# GitHub API base URL
GITHUB_API_BASE = "https://api.github.com"

# Create SSL context
def get_ssl_context():
    """Get SSL context with proper certificates"""
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    return ssl_context

# Create session with SSL
async def create_session():
    """Create aiohttp session with proper SSL context"""
    connector = aiohttp.TCPConnector(ssl=get_ssl_context())
    return aiohttp.ClientSession(connector=connector)

# Tool definitions for GitHub operations
LIST_REPOS_TOOL = Tool(
    name="list_github_repos",
    description="List all your GitHub repositories",
    inputSchema={
        "type": "object",
        "properties": {
            "type": {
                "type": "string",
                "enum": ["all", "owner", "public", "private", "member"],
                "description": "Type of repositories to list",
                "default": "all"
            },
            "sort": {
                "type": "string",
                "enum": ["created", "updated", "pushed", "full_name"],
                "description": "How to sort repositories",
                "default": "updated"
            }
        }
    }
)

BROWSE_REPO_TOOL = Tool(
    name="browse_github_repo",
    description="Browse files and folders in a GitHub repository",
    inputSchema={
        "type": "object",
        "properties": {
            "repo_name": {
                "type": "string",
                "description": "Repository name (e.g., 'myproject' or 'username/myproject')"
            },
            "path": {
                "type": "string",
                "description": "Path within the repository (leave empty for root)",
                "default": ""
            }
        },
        "required": ["repo_name"]
    }
)

READ_GITHUB_FILE_TOOL = Tool(
    name="read_github_file",
    description="Read a file from a GitHub repository",
    inputSchema={
        "type": "object",
        "properties": {
            "repo_name": {
                "type": "string",
                "description": "Repository name"
            },
            "file_path": {
                "type": "string",
                "description": "Path to the file in the repository"
            },
            "branch": {
                "type": "string",
                "description": "Branch name",
                "default": "main"
            }
        },
        "required": ["repo_name", "file_path"]
    }
)

CREATE_GITHUB_FILE_TOOL = Tool(
    name="create_github_file",
    description="Create or update a file in a GitHub repository",
    inputSchema={
        "type": "object",
        "properties": {
            "repo_name": {
                "type": "string",
                "description": "Repository name"
            },
            "file_path": {
                "type": "string",
                "description": "Path for the file"
            },
            "content": {
                "type": "string",
                "description": "File content"
            },
            "commit_message": {
                "type": "string",
                "description": "Commit message"
            },
            "branch": {
                "type": "string",
                "description": "Branch name",
                "default": "main"
            }
        },
        "required": ["repo_name", "file_path", "content", "commit_message"]
    }
)

GET_REPO_INFO_TOOL = Tool(
    name="get_github_repo_info",
    description="Get detailed information about a GitHub repository",
    inputSchema={
        "type": "object",
        "properties": {
            "repo_name": {
                "type": "string",
                "description": "Repository name"
            }
        },
        "required": ["repo_name"]
    }
)

LIST_COMMITS_TOOL = Tool(
    name="list_github_commits",
    description="List recent commits in a repository",
    inputSchema={
        "type": "object",
        "properties": {
            "repo_name": {
                "type": "string",
                "description": "Repository name"
            },
            "branch": {
                "type": "string",
                "description": "Branch name",
                "default": "main"
            },
            "limit": {
                "type": "integer",
                "description": "Number of commits to return",
                "default": 10
            }
        },
        "required": ["repo_name"]
    }
)

SEARCH_GITHUB_TOOL = Tool(
    name="search_github",
    description="Search your GitHub repositories for code or files",
    inputSchema={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Search query"
            },
            "search_type": {
                "type": "string",
                "enum": ["code", "repositories", "commits"],
                "description": "What to search for",
                "default": "code"
            },
            "repo": {
                "type": "string",
                "description": "Limit search to specific repository (optional)"
            }
        },
        "required": ["query"]
    }
)

# GitHub operation implementations
async def get_github_headers(token: str) -> Dict[str, str]:
    """Get headers for GitHub API requests"""
    return {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

async def list_github_repos(type: str = "all", sort: str = "updated") -> Dict[str, Any]:
    """List GitHub repositories"""
    from src.utils.common import load_config
    config = load_config()
    token = config['api_keys']['github']
    
    if not token:
        return {"error": "GitHub token not configured"}
    
    headers = await get_github_headers(token)
    
    # Get authenticated user
    async with await create_session() as session:
        # First get the username
        async with session.get(f"{GITHUB_API_BASE}/user", headers=headers) as response:
            if response.status != 200:
                return {"error": "Failed to authenticate with GitHub"}
            user_data = await response.json()
            username = user_data['login']
        
        # List repositories
        params = {
            "type": type,
            "sort": sort,
            "per_page": 100
        }
        
        async with session.get(f"{GITHUB_API_BASE}/user/repos", headers=headers, params=params) as response:
            if response.status == 200:
                repos = await response.json()
                
                repo_list = []
                for repo in repos:
                    repo_list.append({
                        "name": repo['name'],
                        "full_name": repo['full_name'],
                        "description": repo.get('description', ''),
                        "private": repo['private'],
                        "language": repo.get('language', 'Unknown'),
                        "updated": repo['updated_at'],
                        "url": repo['html_url'],
                        "default_branch": repo.get('default_branch', 'main')
                    })
                
                return {
                    "username": username,
                    "repository_count": len(repo_list),
                    "repositories": repo_list
                }
            else:
                return {"error": f"Failed to list repositories: {response.status}"}

async def browse_github_repo(repo_name: str, path: str = "") -> Dict[str, Any]:
    """Browse repository contents"""
    from src.utils.common import load_config
    config = load_config()
    token = config['api_keys']['github']
    
    if not token:
        return {"error": "GitHub token not configured"}
    
    headers = await get_github_headers(token)
    
    # If repo_name doesn't include owner, get current user
    if '/' not in repo_name:
        async with await create_session() as session:
            async with session.get(f"{GITHUB_API_BASE}/user", headers=headers) as response:
                if response.status == 200:
                    user_data = await response.json()
                    repo_name = f"{user_data['login']}/{repo_name}"
    
    url = f"{GITHUB_API_BASE}/repos/{repo_name}/contents/{path}"
    
    async with await create_session() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                contents = await response.json()
                
                items = []
                for item in contents:
                    items.append({
                        "name": item['name'],
                        "type": item['type'],
                        "path": item['path'],
                        "size": item.get('size', 0),
                        "url": item.get('html_url', '')
                    })
                
                # Sort directories first, then files
                items.sort(key=lambda x: (x['type'] != 'dir', x['name'].lower()))
                
                return {
                    "repository": repo_name,
                    "path": path or "/",
                    "item_count": len(items),
                    "items": items
                }
            else:
                return {"error": f"Failed to browse repository: {response.status}"}

async def read_github_file(repo_name: str, file_path: str, branch: str = "main") -> Dict[str, Any]:
    """Read a file from GitHub"""
    from src.utils.common import load_config
    config = load_config()
    token = config['api_keys']['github']
    
    if not token:
        return {"error": "GitHub token not configured"}
    
    headers = await get_github_headers(token)
    
    # If repo_name doesn't include owner, get current user
    if '/' not in repo_name:
        async with await create_session() as session:
            async with session.get(f"{GITHUB_API_BASE}/user", headers=headers) as response:
                if response.status == 200:
                    user_data = await response.json()
                    repo_name = f"{user_data['login']}/{repo_name}"
    
    url = f"{GITHUB_API_BASE}/repos/{repo_name}/contents/{file_path}"
    params = {"ref": branch}
    
    async with await create_session() as session:
        async with session.get(url, headers=headers, params=params) as response:
            if response.status == 200:
                file_data = await response.json()
                
                # Decode base64 content
                content = base64.b64decode(file_data['content']).decode('utf-8')
                
                return {
                    "repository": repo_name,
                    "file_path": file_path,
                    "branch": branch,
                    "content": content,
                    "size": file_data['size'],
                    "sha": file_data['sha']
                }
            else:
                return {"error": f"Failed to read file: {response.status}"}

async def create_github_file(repo_name: str, file_path: str, content: str, 
                           commit_message: str, branch: str = "main") -> Dict[str, Any]:
    """Create or update a file in GitHub"""
    from src.utils.common import load_config
    config = load_config()
    token = config['api_keys']['github']
    
    if not token:
        return {"error": "GitHub token not configured"}
    
    headers = await get_github_headers(token)
    
    # If repo_name doesn't include owner, get current user
    if '/' not in repo_name:
        async with await create_session() as session:
            async with session.get(f"{GITHUB_API_BASE}/user", headers=headers) as response:
                if response.status == 200:
                    user_data = await response.json()
                    repo_name = f"{user_data['login']}/{repo_name}"
    
    url = f"{GITHUB_API_BASE}/repos/{repo_name}/contents/{file_path}"
    
    # Check if file exists (to get SHA for updates)
    sha = None
    async with await create_session() as session:
        async with session.get(url, headers=headers, params={"ref": branch}) as response:
            if response.status == 200:
                file_data = await response.json()
                sha = file_data['sha']
    
    # Prepare request
    data = {
        "message": commit_message,
        "content": base64.b64encode(content.encode()).decode(),
        "branch": branch
    }
    
    if sha:
        data["sha"] = sha
    
    async with await create_session() as session:
        async with session.put(url, headers=headers, json=data) as response:
            if response.status in [200, 201]:
                result = await response.json()
                return {
                    "status": "success",
                    "repository": repo_name,
                    "file_path": file_path,
                    "branch": branch,
                    "commit": result['commit']['sha'][:7],
                    "url": result['content']['html_url']
                }
            else:
                return {"error": f"Failed to create/update file: {response.status}"}

async def get_github_repo_info(repo_name: str) -> Dict[str, Any]:
    """Get repository information"""
    from src.utils.common import load_config
    config = load_config()
    token = config['api_keys']['github']
    
    if not token:
        return {"error": "GitHub token not configured"}
    
    headers = await get_github_headers(token)
    
    # If repo_name doesn't include owner, get current user
    if '/' not in repo_name:
        async with await create_session() as session:
            async with session.get(f"{GITHUB_API_BASE}/user", headers=headers) as response:
                if response.status == 200:
                    user_data = await response.json()
                    repo_name = f"{user_data['login']}/{repo_name}"
    
    url = f"{GITHUB_API_BASE}/repos/{repo_name}"
    
    async with await create_session() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                repo = await response.json()
                return {
                    "name": repo['name'],
                    "full_name": repo['full_name'],
                    "description": repo.get('description', ''),
                    "private": repo['private'],
                    "language": repo.get('language', 'Unknown'),
                    "created": repo['created_at'],
                    "updated": repo['updated_at'],
                    "stars": repo['stargazers_count'],
                    "forks": repo['forks_count'],
                    "open_issues": repo['open_issues_count'],
                    "default_branch": repo['default_branch'],
                    "url": repo['html_url'],
                    "topics": repo.get('topics', [])
                }
            else:
                return {"error": f"Failed to get repository info: {response.status}"}

async def list_github_commits(repo_name: str, branch: str = "main", limit: int = 10) -> Dict[str, Any]:
    """List recent commits"""
    from src.utils.common import load_config
    config = load_config()
    token = config['api_keys']['github']
    
    if not token:
        return {"error": "GitHub token not configured"}
    
    headers = await get_github_headers(token)
    
    # If repo_name doesn't include owner, get current user
    if '/' not in repo_name:
        async with await create_session() as session:
            async with session.get(f"{GITHUB_API_BASE}/user", headers=headers) as response:
                if response.status == 200:
                    user_data = await response.json()
                    repo_name = f"{user_data['login']}/{repo_name}"
    
    url = f"{GITHUB_API_BASE}/repos/{repo_name}/commits"
    params = {
        "sha": branch,
        "per_page": limit
    }
    
    async with await create_session() as session:
        async with session.get(url, headers=headers, params=params) as response:
            if response.status == 200:
                commits = await response.json()
                
                commit_list = []
                for commit in commits:
                    commit_list.append({
                        "sha": commit['sha'][:7],
                        "message": commit['commit']['message'].split('\n')[0],
                        "author": commit['commit']['author']['name'],
                        "date": commit['commit']['author']['date'],
                        "url": commit['html_url']
                    })
                
                return {
                    "repository": repo_name,
                    "branch": branch,
                    "commit_count": len(commit_list),
                    "commits": commit_list
                }
            else:
                return {"error": f"Failed to list commits: {response.status}"}

async def search_github(query: str, search_type: str = "code", repo: Optional[str] = None) -> Dict[str, Any]:
    """Search GitHub"""
    from src.utils.common import load_config
    config = load_config()
    token = config['api_keys']['github']
    
    if not token:
        return {"error": "GitHub token not configured"}
    
    headers = await get_github_headers(token)
    
    # Get username if needed
    username = None
    if repo and '/' not in repo:
        async with await create_session() as session:
            async with session.get(f"{GITHUB_API_BASE}/user", headers=headers) as response:
                if response.status == 200:
                    user_data = await response.json()
                    username = user_data['login']
                    repo = f"{username}/{repo}"
    
    # Build search query
    if repo:
        search_query = f"{query} repo:{repo}"
    else:
        search_query = f"{query} user:{username}" if username else query
    
    url = f"{GITHUB_API_BASE}/search/{search_type}"
    params = {
        "q": search_query,
        "per_page": 20
    }
    
    async with await create_session() as session:
        async with session.get(url, headers=headers, params=params) as response:
            if response.status == 200:
                data = await response.json()
                
                results = []
                if search_type == "code":
                    for item in data.get('items', []):
                        results.append({
                            "file": item['name'],
                            "path": item['path'],
                            "repository": item['repository']['full_name'],
                            "url": item['html_url']
                        })
                elif search_type == "repositories":
                    for item in data.get('items', []):
                        results.append({
                            "name": item['full_name'],
                            "description": item.get('description', ''),
                            "language": item.get('language', 'Unknown'),
                            "stars": item['stargazers_count'],
                            "url": item['html_url']
                        })
                
                return {
                    "query": query,
                    "search_type": search_type,
                    "total_count": data.get('total_count', 0),
                    "results": results
                }
            else:
                return {"error": f"Failed to search: {response.status}"}

# Export tools list
GITHUB_OPERATION_TOOLS = [
    LIST_REPOS_TOOL,
    BROWSE_REPO_TOOL,
    READ_GITHUB_FILE_TOOL,
    CREATE_GITHUB_FILE_TOOL,
    GET_REPO_INFO_TOOL,
    LIST_COMMITS_TOOL,
    SEARCH_GITHUB_TOOL
]