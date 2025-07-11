#!/usr/bin/env python3
"""
Gemini Operations for Dobbs MCP
Integration with Google's Gemini AI for enhanced analysis and research capabilities
"""

import os
import json
from typing import Dict, List, Optional, Any
import aiohttp
import asyncio
import ssl
import certifi
from mcp.types import Tool

# Gemini API configuration
GEMINI_API_BASE = "https://generativelanguage.googleapis.com/v1beta"
GEMINI_MODEL = "gemini-2.0-flash-thinking-exp-01-21"  # Latest model with 1M context

# Tool definitions
GEMINI_QUERY_TOOL = Tool(
    name="gemini_query",
    description="Query Gemini AI for analysis, insights, or alternative perspectives",
    inputSchema={
        "type": "object",
        "properties": {
            "prompt": {
                "type": "string",
                "description": "The question or prompt for Gemini"
            },
            "context": {
                "type": "string",
                "description": "Additional context or background information (optional)"
            },
            "temperature": {
                "type": "number",
                "description": "Creativity level (0.0-1.0, default 0.7)",
                "default": 0.7
            }
        },
        "required": ["prompt"]
    }
)

GEMINI_ANALYZE_CODE_TOOL = Tool(
    name="gemini_analyze_code",
    description="Use Gemini to analyze code for security, performance, or quality issues",
    inputSchema={
        "type": "object",
        "properties": {
            "code": {
                "type": "string",
                "description": "The code to analyze"
            },
            "analysis_type": {
                "type": "string",
                "enum": ["security", "performance", "quality", "general"],
                "description": "Type of analysis to perform",
                "default": "general"
            },
            "language": {
                "type": "string",
                "description": "Programming language (optional, will auto-detect)"
            }
        },
        "required": ["code"]
    }
)

GEMINI_BRAINSTORM_TOOL = Tool(
    name="gemini_brainstorm",
    description="Brainstorm ideas and solutions with Gemini's creative capabilities",
    inputSchema={
        "type": "object",
        "properties": {
            "topic": {
                "type": "string",
                "description": "The topic or problem to brainstorm about"
            },
            "constraints": {
                "type": "string",
                "description": "Any constraints or requirements (optional)"
            },
            "num_ideas": {
                "type": "integer",
                "description": "Number of ideas to generate (default 5)",
                "default": 5
            }
        },
        "required": ["topic"]
    }
)

GEMINI_SUMMARIZE_TOOL = Tool(
    name="gemini_summarize",
    description="Summarize large texts or documents using Gemini's large context window",
    inputSchema={
        "type": "object",
        "properties": {
            "text": {
                "type": "string",
                "description": "The text to summarize"
            },
            "summary_type": {
                "type": "string",
                "enum": ["brief", "detailed", "bullet_points", "key_insights"],
                "description": "Type of summary to generate",
                "default": "brief"
            },
            "max_length": {
                "type": "integer",
                "description": "Maximum length of summary in words (optional)"
            }
        },
        "required": ["text"]
    }
)

GEMINI_MATH_ANALYSIS_TOOL = Tool(
    name="gemini_math_analysis",
    description="Use Gemini for mathematical analysis and theorem exploration",
    inputSchema={
        "type": "object",
        "properties": {
            "concept": {
                "type": "string",
                "description": "Mathematical concept or theorem to analyze"
            },
            "approach": {
                "type": "string",
                "enum": ["proof", "visualization", "applications", "connections"],
                "description": "Type of analysis approach",
                "default": "connections"
            },
            "context": {
                "type": "string",
                "description": "Specific mathematical context (e.g., gyrovector spaces)"
            }
        },
        "required": ["concept"]
    }
)

GEMINI_RESEARCH_REVIEW_TOOL = Tool(
    name="gemini_research_review",
    description="Have Gemini review and critique research ideas or papers",
    inputSchema={
        "type": "object",
        "properties": {
            "content": {
                "type": "string",
                "description": "Research content to review"
            },
            "focus_areas": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Specific areas to focus on (e.g., methodology, novelty, clarity)"
            },
            "academic_level": {
                "type": "string",
                "enum": ["undergraduate", "graduate", "research", "publication"],
                "description": "Target academic level",
                "default": "research"
            }
        },
        "required": ["content"]
    }
)

# Helper functions
def create_ssl_context():
    """Create SSL context with proper certificate verification"""
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    return ssl_context

async def get_gemini_headers() -> Dict[str, str]:
    """Get headers for Gemini API requests"""
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables")
    
    return {
        "Content-Type": "application/json",
        "x-goog-api-key": api_key
    }

def format_prompt(prompt: str, context: Optional[str] = None) -> str:
    """Format prompt with optional context"""
    if context:
        return f"Context: {context}\n\nQuery: {prompt}"
    return prompt

# API Functions
async def gemini_query(
    prompt: str,
    context: Optional[str] = None,
    temperature: float = 0.7
) -> Dict[str, Any]:
    """Query Gemini AI"""
    headers = await get_gemini_headers()
    
    formatted_prompt = format_prompt(prompt, context)
    
    payload = {
        "contents": [{
            "parts": [{
                "text": formatted_prompt
            }]
        }],
        "generationConfig": {
            "temperature": temperature,
            "maxOutputTokens": 8192,
            "topP": 0.95,
            "topK": 40
        }
    }
    
    ssl_context = create_ssl_context()
    connector = aiohttp.TCPConnector(ssl=ssl_context)
    
    async with aiohttp.ClientSession(connector=connector) as session:
        async with session.post(
            f"{GEMINI_API_BASE}/models/{GEMINI_MODEL}:generateContent",
            headers=headers,
            json=payload
        ) as response:
            if response.status == 200:
                data = await response.json()
                
                # Extract text from response
                text = ""
                if "candidates" in data and data["candidates"]:
                    candidate = data["candidates"][0]
                    if "content" in candidate and "parts" in candidate["content"]:
                        text = candidate["content"]["parts"][0].get("text", "")
                
                return {
                    "status": "success",
                    "response": text,
                    "model": GEMINI_MODEL,
                    "usage": data.get("usageMetadata", {})
                }
            else:
                error = await response.text()
                return {
                    "status": "error",
                    "error": f"Gemini API error: {error}"
                }

async def gemini_analyze_code(
    code: str,
    analysis_type: str = "general",
    language: Optional[str] = None
) -> Dict[str, Any]:
    """Analyze code using Gemini"""
    
    analysis_prompts = {
        "security": "Analyze this code for security vulnerabilities, potential exploits, and unsafe practices:",
        "performance": "Analyze this code for performance issues, bottlenecks, and optimization opportunities:",
        "quality": "Analyze this code for quality issues, maintainability, and best practices:",
        "general": "Provide a comprehensive analysis of this code including security, performance, and quality:"
    }
    
    prompt = f"{analysis_prompts[analysis_type]}\n\n"
    if language:
        prompt += f"Language: {language}\n\n"
    prompt += f"```\n{code}\n```"
    
    return await gemini_query(prompt, temperature=0.3)

async def gemini_brainstorm(
    topic: str,
    constraints: Optional[str] = None,
    num_ideas: int = 5
) -> Dict[str, Any]:
    """Brainstorm ideas with Gemini"""
    
    prompt = f"Please brainstorm {num_ideas} creative ideas for: {topic}"
    if constraints:
        prompt += f"\n\nConstraints/Requirements: {constraints}"
    prompt += "\n\nFormat your response as a numbered list with brief explanations for each idea."
    
    return await gemini_query(prompt, temperature=0.8)

async def gemini_summarize(
    text: str,
    summary_type: str = "brief",
    max_length: Optional[int] = None
) -> Dict[str, Any]:
    """Summarize text using Gemini"""
    
    summary_prompts = {
        "brief": "Provide a brief summary of the following text:",
        "detailed": "Provide a detailed summary of the following text:",
        "bullet_points": "Summarize the following text as bullet points:",
        "key_insights": "Extract the key insights and takeaways from the following text:"
    }
    
    prompt = summary_prompts[summary_type]
    if max_length:
        prompt += f" (maximum {max_length} words)"
    prompt += f"\n\n{text}"
    
    return await gemini_query(prompt, temperature=0.3)

async def gemini_math_analysis(
    concept: str,
    approach: str = "connections",
    context: Optional[str] = None
) -> Dict[str, Any]:
    """Analyze mathematical concepts with Gemini"""
    
    approach_prompts = {
        "proof": "Provide a rigorous mathematical proof or explanation for:",
        "visualization": "Describe how to visualize and understand:",
        "applications": "Explain the practical applications and use cases of:",
        "connections": "Explore the connections and relationships of this concept with other mathematical ideas:"
    }
    
    prompt = f"{approach_prompts[approach]} {concept}"
    if context:
        prompt += f"\n\nSpecific context: {context}"
    prompt += "\n\nPlease use proper mathematical notation and be precise in your explanations."
    
    return await gemini_query(prompt, temperature=0.5)

async def gemini_research_review(
    content: str,
    focus_areas: Optional[List[str]] = None,
    academic_level: str = "research"
) -> Dict[str, Any]:
    """Review research content with Gemini"""
    
    prompt = f"Please review the following research content at the {academic_level} level:\n\n{content}\n\n"
    
    if focus_areas:
        prompt += f"Focus particularly on: {', '.join(focus_areas)}\n\n"
    else:
        prompt += "Consider: methodology, novelty, clarity, rigor, and potential impact.\n\n"
    
    prompt += "Provide constructive feedback and suggestions for improvement."
    
    return await gemini_query(prompt, temperature=0.4)

# Export tools list
GEMINI_OPERATION_TOOLS = [
    GEMINI_QUERY_TOOL,
    GEMINI_ANALYZE_CODE_TOOL,
    GEMINI_BRAINSTORM_TOOL,
    GEMINI_SUMMARIZE_TOOL,
    GEMINI_MATH_ANALYSIS_TOOL,
    GEMINI_RESEARCH_REVIEW_TOOL
]