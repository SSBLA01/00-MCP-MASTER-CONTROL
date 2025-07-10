#!/usr/bin/env python3
"""
Research Discovery Agent MCP Server

This agent handles discovering mathematical research papers, articles, and resources
using Perplexity AI, arXiv, and other sources.
"""

import asyncio
import json
import sys
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path
import aiohttp
import re
import ssl
import certifi

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.utils.common import setup_logging, load_config

# Import MCP SDK
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Setup logging
logger = setup_logging("ResearchDiscovery")

# Load configuration
config = load_config()

# Initialize MCP server
server = Server("research-discovery-agent")

# Tool definitions
DISCOVER_RESEARCH_TOOL = Tool(
    name="discover_research",
    description="Discover mathematical research papers and resources on a topic",
    inputSchema={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Search query for mathematical topics"
            },
            "sources": {
                "type": "array",
                "items": {"type": "string", "enum": ["perplexity", "arxiv", "mathscinet", "zbmath"]},
                "description": "Sources to search (defaults to all)"
            },
            "max_results": {
                "type": "integer",
                "description": "Maximum number of results to return",
                "minimum": 1,
                "maximum": 50
            },
            "time_filter": {
                "type": "string",
                "enum": ["all_time", "past_year", "past_month", "past_week"],
                "description": "Filter results by time period"
            }
        },
        "required": ["query"]
    }
)

ANALYZE_PAPER_TOOL = Tool(
    name="analyze_paper",
    description="Analyze a mathematical paper for key concepts and relationships",
    inputSchema={
        "type": "object",
        "properties": {
            "paper_url": {
                "type": "string",
                "description": "URL of the paper to analyze (arXiv or other)"
            },
            "extract_elements": {
                "type": "array",
                "items": {"type": "string", "enum": ["theorems", "definitions", "proofs", "examples", "references"]},
                "description": "Elements to extract from the paper"
            }
        },
        "required": ["paper_url"]
    }
)

FIND_RELATED_WORK_TOOL = Tool(
    name="find_related_work",
    description="Find papers related to a given paper or concept",
    inputSchema={
        "type": "object",
        "properties": {
            "reference": {
                "type": "string",
                "description": "Paper title, arXiv ID, or concept name"
            },
            "relationship_type": {
                "type": "string",
                "enum": ["citations", "references", "similar", "contradictory", "extends"],
                "description": "Type of relationship to search for"
            },
            "depth": {
                "type": "integer",
                "description": "How many levels deep to search",
                "minimum": 1,
                "maximum": 3
            }
        },
        "required": ["reference"]
    }
)

TRACK_RESEARCH_TRENDS_TOOL = Tool(
    name="track_research_trends",
    description="Track trends and emerging topics in mathematical research",
    inputSchema={
        "type": "object",
        "properties": {
            "field": {
                "type": "string",
                "description": "Mathematical field to analyze (e.g., 'hyperbolic geometry', 'category theory')"
            },
            "time_period": {
                "type": "string",
                "enum": ["last_month", "last_quarter", "last_year", "last_5_years"],
                "description": "Time period to analyze"
            },
            "metrics": {
                "type": "array",
                "items": {"type": "string", "enum": ["publication_count", "citation_velocity", "author_networks", "keyword_emergence"]},
                "description": "Metrics to track"
            }
        },
        "required": ["field"]
    }
)

# Tool registry
TOOLS = [
    DISCOVER_RESEARCH_TOOL,
    ANALYZE_PAPER_TOOL,
    FIND_RELATED_WORK_TOOL,
    TRACK_RESEARCH_TRENDS_TOOL
]

# Register list_tools handler
@server.list_tools()
async def handle_list_tools() -> List[Tool]:
    return TOOLS

# Research discovery functions

def get_ssl_context():
    """Get SSL context with proper certificates"""
    return ssl.create_default_context(cafile=certifi.where())
async def search_perplexity(query: str, max_results: int = 10) -> List[Dict[str, Any]]:
    """Search using Perplexity AI API"""
    api_key = config['api_keys']['perplexity']
    if not api_key:
        logger.error("Perplexity API key not configured")
        return []
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Enhance query for mathematical context
    enhanced_query = f"mathematical research papers: {query}"
    
    payload = {
        "model": "sonar-small-online",
        "messages": [
            {
                "role": "system",
                "content": "You are a mathematical research assistant. Find and summarize relevant papers and resources."
            },
            {
                "role": "user",
                "content": enhanced_query
            }
        ],
        "max_tokens": 1000,
        "temperature": 0.2,
        "top_p": 0.9
    }
    
    try:
        connector = aiohttp.TCPConnector(ssl=get_ssl_context())
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.post(
                "https://api.perplexity.ai/chat/completions",
                headers=headers,
                json=payload
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    # Parse the response to extract paper information
                    content = data['choices'][0]['message']['content']
                    
                    # Simple extraction of paper-like references
                    papers = []
                    lines = content.split('\n')
                    for line in lines:
                        if any(keyword in line.lower() for keyword in ['arxiv', 'paper', 'article', 'journal']):
                            papers.append({
                                "title": line.strip(),
                                "source": "perplexity",
                                "relevance": "high",
                                "summary": ""
                            })
                    
                    return papers[:max_results]
                else:
                    logger.error(f"Perplexity API error: {response.status}")
                    return []
    except Exception as e:
        logger.error(f"Error searching Perplexity: {e}")
        return []

async def search_arxiv(query: str, max_results: int = 10) -> List[Dict[str, Any]]:
    """Search arXiv for papers"""
    base_url = "http://export.arxiv.org/api/query"
    
    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": max_results,
        "sortBy": "relevance",
        "sortOrder": "descending"
    }
    
    try:
        connector = aiohttp.TCPConnector(ssl=get_ssl_context())
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(base_url, params=params) as response:
                if response.status == 200:
                    # Parse XML response (simplified for this example)
                    text = await response.text()
                    
                    # Extract paper information using regex (in production, use proper XML parser)
                    papers = []
                    
                    # Simple pattern matching for demonstration
                    title_pattern = r'<title>(.*?)</title>'
                    summary_pattern = r'<summary>(.*?)</summary>'
                    id_pattern = r'<id>(.*?)</id>'
                    
                    titles = re.findall(title_pattern, text, re.DOTALL)
                    summaries = re.findall(summary_pattern, text, re.DOTALL)
                    ids = re.findall(id_pattern, text, re.DOTALL)
                    
                    # Skip the first entry (feed title)
                    for i in range(1, min(len(titles), max_results + 1)):
                        if i < len(summaries) and i < len(ids):
                            papers.append({
                                "title": titles[i].strip(),
                                "summary": summaries[i].strip()[:500] + "...",
                                "url": ids[i].strip(),
                                "source": "arxiv",
                                "relevance": "high"
                            })
                    
                    return papers
                else:
                    logger.error(f"arXiv API error: {response.status}")
                    return []
    except Exception as e:
        logger.error(f"Error searching arXiv: {e}")
        return []

async def discover_research(
    query: str,
    sources: Optional[List[str]] = None,
    max_results: int = 20,
    time_filter: str = "all_time"
) -> Dict[str, Any]:
    """Discover research papers across multiple sources"""
    if sources is None:
        sources = ["perplexity", "arxiv"]
    
    all_results = []
    session_id = datetime.now().isoformat()
    
    # Search each source
    for source in sources:
        if source == "perplexity":
            results = await search_perplexity(query, max_results)
            all_results.extend(results)
        elif source == "arxiv":
            results = await search_arxiv(query, max_results)
            all_results.extend(results)
    
    # Sort by relevance and deduplicate
    seen_titles = set()
    unique_results = []
    for result in all_results:
        title_lower = result['title'].lower()
        if title_lower not in seen_titles:
            seen_titles.add(title_lower)
            unique_results.append(result)
    
    return {
        "session_id": session_id,
        "query": query,
        "sources_searched": sources,
        "total_results": len(unique_results),
        "results": unique_results[:max_results],
        "timestamp": datetime.now().isoformat()
    }

async def analyze_paper(
    paper_url: str,
    extract_elements: Optional[List[str]] = None
) -> Dict[str, Any]:
    """Analyze a paper for mathematical content"""
    if extract_elements is None:
        extract_elements = ["theorems", "definitions", "examples"]
    
    # In a real implementation, this would download and parse the paper
    # For now, we'll return a structured analysis template
    
    analysis = {
        "paper_url": paper_url,
        "analysis_timestamp": datetime.now().isoformat(),
        "extracted_elements": {}
    }
    
    # Simulate extraction based on requested elements
    if "theorems" in extract_elements:
        analysis["extracted_elements"]["theorems"] = [
            {
                "id": "thm1",
                "statement": "Example theorem statement",
                "dependencies": []
            }
        ]
    
    if "definitions" in extract_elements:
        analysis["extracted_elements"]["definitions"] = [
            {
                "term": "Example term",
                "definition": "Example definition",
                "context": "Section 2.1"
            }
        ]
    
    if "proofs" in extract_elements:
        analysis["extracted_elements"]["proofs"] = [
            {
                "theorem_id": "thm1",
                "technique": "Direct proof",
                "key_steps": ["Step 1", "Step 2", "Step 3"]
            }
        ]
    
    return analysis

async def find_related_work(
    reference: str,
    relationship_type: str = "similar",
    depth: int = 1
) -> Dict[str, Any]:
    """Find papers related to a reference"""
    # This would implement citation graph traversal in production
    
    related_papers = []
    
    # Simulate finding related work
    if relationship_type == "citations":
        related_papers = [
            {
                "title": f"Paper citing {reference}",
                "relationship": "cites",
                "strength": 0.9
            }
        ]
    elif relationship_type == "similar":
        related_papers = [
            {
                "title": f"Paper similar to {reference}",
                "relationship": "similar_topic",
                "strength": 0.85
            }
        ]
    
    return {
        "reference": reference,
        "relationship_type": relationship_type,
        "depth_searched": depth,
        "related_count": len(related_papers),
        "related_papers": related_papers
    }

async def track_research_trends(
    field: str,
    time_period: str = "last_year",
    metrics: Optional[List[str]] = None
) -> Dict[str, Any]:
    """Track research trends in a field"""
    if metrics is None:
        metrics = ["publication_count", "keyword_emergence"]
    
    trends = {
        "field": field,
        "time_period": time_period,
        "analysis_date": datetime.now().isoformat(),
        "metrics": {}
    }
    
    # Simulate trend analysis
    if "publication_count" in metrics:
        trends["metrics"]["publication_count"] = {
            "total": 150,
            "growth_rate": 0.15,
            "peak_months": ["March", "September"]
        }
    
    if "keyword_emergence" in metrics:
        trends["metrics"]["keyword_emergence"] = {
            "emerging_keywords": ["hyperbolic neural networks", "geometric deep learning"],
            "declining_keywords": ["classical methods"],
            "stable_keywords": ["Riemannian geometry", "differential forms"]
        }
    
    return trends

# Tool handlers
@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> List[TextContent]:
    """Handle tool calls"""
    if name == "discover_research":
        result = await discover_research(**arguments)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    elif name == "analyze_paper":
        result = await analyze_paper(**arguments)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    elif name == "find_related_work":
        result = await find_related_work(**arguments)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    elif name == "track_research_trends":
        result = await track_research_trends(**arguments)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    else:
        return [TextContent(type="text", text=json.dumps({"error": f"Unknown tool: {name}"}))]

async def main():
    """Main entry point for the MCP server"""
    logger.info("Starting Research Discovery Agent...")
    
    # Run the server
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="research-discovery-agent",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())