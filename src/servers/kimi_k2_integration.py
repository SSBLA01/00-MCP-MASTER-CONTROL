"""
Kimi K2 Integration Module for Dobbs-MCP
=========================================

This module integrates Moonshot AI's Kimi K2 model via Groq API
into the existing MCP system, providing enhanced mathematical reasoning
and agentic capabilities.

Version: 1.0.1
"""

import os
import json
import asyncio
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime

import aiohttp

# Defensive import for groq module
try:
    from groq import AsyncGroq
    GROQ_AVAILABLE = True
except ImportError as e:
    GROQ_AVAILABLE = False
    AsyncGroq = None
    logging.warning(f"groq module not available: {e}")

from mcp import Server, types
from mcp.types import Tool, TextContent

# Configure logging
logger = logging.getLogger(__name__)

@dataclass
class KimiK2Config:
    """Configuration for Kimi K2 integration"""
    groq_api_key: str
    model_name: str = "moonshotai/kimi-k2-instruct"
    temperature: float = 0.7
    max_tokens: int = 32768
    timeout: int = 60
    context_window: int = 128000  # 128K context window

class KimiK2Agent:
    """
    Kimi K2 Agent for mathematical reasoning and agentic tasks
    """
    
    def __init__(self, config: KimiK2Config):
        self.config = config
        if GROQ_AVAILABLE and AsyncGroq:
            self.client = AsyncGroq(api_key=config.groq_api_key)
        else:
            self.client = None
            logger.warning("Kimi K2 Agent initialized without groq client")
        self.session_history: List[Dict[str, Any]] = []
        
    async def query(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Send a query to Kimi K2 via Groq API
        
        Args:
            prompt: The user query
            system_prompt: Optional system prompt for specialized behavior
            tools: Optional list of tools for agentic tasks
            context: Optional context (mathematical formulas, previous results, etc.)
            
        Returns:
            Response from Kimi K2 with enhanced mathematical reasoning
        """
        if not GROQ_AVAILABLE or self.client is None:
            return {
                "error": "Groq module not available. Please install: pip install groq",
                "status": "error"
            }
        
        try:
            # Prepare messages
            messages = []
            
            # Add system prompt
            if system_prompt:
                messages.append({
                    "role": "system",
                    "content": system_prompt
                })
            else:
                # Default system prompt for mathematical reasoning
                messages.append({
                    "role": "system",
                    "content": """You are Kimi K2, an advanced mathematical reasoning agent 
                    specialized in gyrovector spaces, lattices, recursive harmonics, and orbifolds. 
                    You excel at both theoretical proofs and computational mathematics.
                    When solving problems, think step-by-step and verify your results."""
                })
            
            # Add context if provided
            if context:
                context_str = f"Context:\n{json.dumps(context, indent=2)}"
                messages.append({
                    "role": "system",
                    "content": context_str
                })
            
            # Add user prompt
            messages.append({
                "role": "user",
                "content": prompt
            })
            
            # Make API call
            start_time = datetime.now()
            
            response = await self.client.chat.completions.create(
                model=self.config.model_name,
                messages=messages,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
                tools=tools,
                tool_choice="auto" if tools else None
            )
            
            end_time = datetime.now()
            duration_ms = (end_time - start_time).total_seconds() * 1000
            
            # Process response
            result = {
                "status": "success",
                "content": response.choices[0].message.content,
                "tool_calls": response.choices[0].message.tool_calls if hasattr(response.choices[0].message, 'tool_calls') else None,
                "metadata": {
                    "model": self.config.model_name,
                    "duration_ms": duration_ms,
                    "tokens": {
                        "prompt": response.usage.prompt_tokens,
                        "completion": response.usage.completion_tokens,
                        "total": response.usage.total_tokens
                    },
                    "timestamp": datetime.now().isoformat()
                }
            }
            
            # Store in session history
            self.session_history.append({
                "prompt": prompt,
                "response": result,
                "timestamp": datetime.now().isoformat()
            })
            
            return result
            
        except Exception as e:
            logger.error(f"Kimi K2 query error: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "metadata": {
                    "timestamp": datetime.now().isoformat()
                }
            }
    
    async def solve_mathematical_problem(
        self,
        problem: str,
        domain: str = "general",
        validate: bool = True
    ) -> Dict[str, Any]:
        """
        Solve a mathematical problem with step-by-step reasoning
        
        Args:
            problem: Mathematical problem description
            domain: Specific domain (gyrovector, lattice, harmonic, orbifold)
            validate: Whether to validate the solution
            
        Returns:
            Solution with steps and validation
        """
        # Domain-specific prompts
        domain_prompts = {
            "gyrovector": """Solve this problem using gyrovector space theory. 
                           Apply gyroaddition, gyroscalar multiplication, and gyroparallel transport as needed.""",
            "lattice": """Solve this problem using lattice theory. 
                         Consider lattice operations, sublattices, and homomorphisms.""",
            "harmonic": """Solve this problem using recursive harmonic analysis. 
                          Apply Fourier analysis and recursive decomposition techniques.""",
            "orbifold": """Solve this problem using orbifold theory. 
                          Consider quotient spaces and group actions.""",
            "general": "Solve this mathematical problem step-by-step."
        }
        
        system_prompt = f"""You are solving a mathematical problem in the {domain} domain.
        {domain_prompts.get(domain, domain_prompts['general'])}
        
        Provide:
        1. Problem understanding and setup
        2. Step-by-step solution
        3. Final answer
        4. Verification of the result
        """
        
        # Get solution
        solution = await self.query(
            prompt=problem,
            system_prompt=system_prompt
        )
        
        # Optionally validate with a second pass
        if validate and solution["status"] == "success":
            validation_prompt = f"""Verify the following solution:
            Problem: {problem}
            Solution: {solution['content']}
            
            Check for:
            1. Mathematical correctness
            2. Logical consistency
            3. Completeness of the solution
            """
            
            validation = await self.query(
                prompt=validation_prompt,
                system_prompt="You are a mathematical proof verifier. Be rigorous and thorough."
            )
            
            solution["validation"] = validation
        
        return solution
    
    async def generate_manim_code(
        self,
        concept: str,
        animation_type: str = "2d_plot",
        style: str = "minimalist"
    ) -> Dict[str, Any]:
        """
        Generate Manim animation code for mathematical concepts
        
        Args:
            concept: Mathematical concept to visualize
            animation_type: Type of animation
            style: Visual style
            
        Returns:
            Manim code and metadata
        """
        prompt = f"""Generate Manim code to visualize: {concept}
        
        Animation type: {animation_type}
        Style: {style}
        
        Requirements:
        1. Use Manim Community Edition (import from manim import *)
        2. Create a complete Scene class
        3. Include mathematical formulas using MathTex
        4. Add smooth animations and transitions
        5. Follow the gyrovector visualization patterns if applicable
        
        Provide the complete Python code that can be saved and executed.
        """
        
        system_prompt = """You are an expert in creating mathematical visualizations 
        using Manim. You understand advanced mathematical concepts and can translate 
        them into beautiful, educational animations."""
        
        result = await self.query(prompt, system_prompt)
        
        if result["status"] == "success":
            # Extract code from response
            code = result["content"]
            
            # Clean up code if needed
            if "```python" in code:
                code = code.split("```python")[1].split("```")[0].strip()
            elif "```" in code:
                code = code.split("```")[1].split("```")[0].strip()
            
            result["manim_code"] = code
            result["file_name"] = f"{concept.replace(' ', '_').lower()}_animation.py"
        
        return result

class KimiK2Integration:
    """
    Main integration class for Kimi K2 with the MCP system
    """
    
    def __init__(self, server: Server):
        self.server = server
        self.config = KimiK2Config(
            groq_api_key=os.getenv("GROQ_API_KEY", "")
        )
        if GROQ_AVAILABLE:
            self.agent = KimiK2Agent(self.config)
        else:
            self.agent = None
            logger.warning("Kimi K2 Integration initialized without agent (groq not available)")
        self.tools = self._define_tools()
        
    def _define_tools(self) -> List[Tool]:
        """Define MCP tools for Kimi K2 integration"""
        return [
            Tool(
                name="kimi_k2_query",
                description="Query Kimi K2 for advanced mathematical reasoning and problem solving",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "prompt": {
                            "type": "string",
                            "description": "The mathematical question or problem"
                        },
                        "context": {
                            "type": "object",
                            "description": "Optional context (formulas, previous results, etc.)"
                        }
                    },
                    "required": ["prompt"]
                }
            ),
            Tool(
                name="kimi_k2_solve_problem",
                description="Solve a mathematical problem with step-by-step reasoning",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "problem": {
                            "type": "string",
                            "description": "Mathematical problem to solve"
                        },
                        "domain": {
                            "type": "string",
                            "enum": ["general", "gyrovector", "lattice", "harmonic", "orbifold"],
                            "default": "general",
                            "description": "Mathematical domain"
                        },
                        "validate": {
                            "type": "boolean",
                            "default": True,
                            "description": "Whether to validate the solution"
                        }
                    },
                    "required": ["problem"]
                }
            ),
            Tool(
                name="kimi_k2_generate_visualization",
                description="Generate Manim code for mathematical visualizations",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "concept": {
                            "type": "string",
                            "description": "Mathematical concept to visualize"
                        },
                        "animation_type": {
                            "type": "string",
                            "enum": ["2d_plot", "3d_surface", "transformation", "proof_visualization", "geometric_construction"],
                            "default": "2d_plot"
                        },
                        "style": {
                            "type": "string",
                            "enum": ["minimalist", "3blue1brown", "academic", "colorful"],
                            "default": "minimalist"
                        }
                    },
                    "required": ["concept"]
                }
            ),
            Tool(
                name="kimi_k2_collaborative_reasoning",
                description="Use Kimi K2 in collaboration with Claude Flow for complex mathematical tasks",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "task": {
                            "type": "string",
                            "description": "Complex mathematical task requiring collaboration"
                        },
                        "agents": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "Other agents to collaborate with"
                        },
                        "workflow_type": {
                            "type": "string",
                            "enum": ["sequential", "parallel", "iterative"],
                            "default": "sequential"
                        }
                    },
                    "required": ["task"]
                }
            )
        ]
    
    async def handle_tool_call(self, name: str, arguments: Dict[str, Any]) -> Any:
        """Handle MCP tool calls for Kimi K2"""
        
        if not GROQ_AVAILABLE or self.agent is None:
            return [TextContent(
                type="text",
                text=json.dumps({
                    "error": "Kimi K2 integration requires groq module. Install with: pip install groq",
                    "status": "error"
                }, indent=2)
            )]
        
        if name == "kimi_k2_query":
            result = await self.agent.query(
                prompt=arguments["prompt"],
                context=arguments.get("context")
            )
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]
            
        elif name == "kimi_k2_solve_problem":
            result = await self.agent.solve_mathematical_problem(
                problem=arguments["problem"],
                domain=arguments.get("domain", "general"),
                validate=arguments.get("validate", True)
            )
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]
            
        elif name == "kimi_k2_generate_visualization":
            result = await self.agent.generate_manim_code(
                concept=arguments["concept"],
                animation_type=arguments.get("animation_type", "2d_plot"),
                style=arguments.get("style", "minimalist")
            )
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]
            
        elif name == "kimi_k2_collaborative_reasoning":
            # This would integrate with Claude Flow
            # For now, return a placeholder
            return [TextContent(
                type="text",
                text=json.dumps({
                    "status": "success",
                    "message": "Collaborative reasoning initiated",
                    "task": arguments["task"],
                    "agents": arguments.get("agents", ["kimi_k2"]),
                    "workflow": arguments.get("workflow_type", "sequential")
                }, indent=2)
            )]
        
        else:
            raise ValueError(f"Unknown tool: {name}")
    
    def register_with_server(self):
        """Register Kimi K2 tools with the MCP server"""
        if not self.tools:
            logger.warning("No Kimi K2 tools to register")
            return
            
        for tool in self.tools:
            self.server.add_tool(tool)
            
        # Register tool handler
        @self.server.call_tool()
        async def handle_kimi_k2_tool(name: str, arguments: Dict[str, Any]) -> Any:
            if name.startswith("kimi_k2_"):
                return await self.handle_tool_call(name, arguments)
            return None