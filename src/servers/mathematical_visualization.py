#!/usr/bin/env python3
"""
Mathematical Visualization Agent MCP Server

This agent creates mathematical visualizations using Manim and validates
mathematical concepts using Wolfram Alpha.
"""

import asyncio
import json
import sys
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path
import subprocess
import hashlib
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
logger = setup_logging("MathematicalVisualization")

# Load configuration
config = load_config()

# Initialize MCP server
server = Server("mathematical-visualization-agent")

# Tool definitions
CREATE_MANIM_ANIMATION_TOOL = Tool(
    name="create_manim_animation",
    description="Create a mathematical animation using Manim",
    inputSchema={
        "type": "object",
        "properties": {
            "concept": {
                "type": "string",
                "description": "Mathematical concept to animate"
            },
            "animation_type": {
                "type": "string",
                "enum": ["2d_plot", "3d_surface", "transformation", "proof_visualization", "geometric_construction"],
                "description": "Type of animation to create"
            },
            "style": {
                "type": "string",
                "enum": ["minimalist", "3blue1brown", "academic", "colorful"],
                "description": "Visual style for the animation"
            },
            "duration": {
                "type": "integer",
                "description": "Duration in seconds",
                "minimum": 5,
                "maximum": 300
            },
            "equations": {
                "type": "array",
                "items": {"type": "string"},
                "description": "LaTeX equations to include"
            },
            "output_path": {
                "type": "string",
                "description": "Custom output path for the final MP4 (relative to Dropbox root, e.g., 'Media/Manim/my_animation.mp4'). If not specified, uses default manim_outputs folder."
            }
        },
        "required": ["concept", "animation_type"]
    }
)

CREATE_STATIC_DIAGRAM_TOOL = Tool(
    name="create_static_diagram",
    description="Create a static mathematical diagram",
    inputSchema={
        "type": "object",
        "properties": {
            "diagram_type": {
                "type": "string",
                "enum": ["graph", "geometry", "topology", "algebra", "category_theory"],
                "description": "Type of diagram to create"
            },
            "elements": {
                "type": "object",
                "description": "Elements to include in the diagram"
            },
            "labels": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Labels and annotations"
            },
            "output_format": {
                "type": "string",
                "enum": ["svg", "png", "pdf"],
                "description": "Output format for the diagram"
            }
        },
        "required": ["diagram_type", "elements"]
    }
)

VALIDATE_WITH_WOLFRAM_TOOL = Tool(
    name="validate_with_wolfram",
    description="Validate mathematical statements using Wolfram Alpha",
    inputSchema={
        "type": "object",
        "properties": {
            "expression": {
                "type": "string",
                "description": "Mathematical expression or equation to validate"
            },
            "validation_type": {
                "type": "string",
                "enum": ["solve", "simplify", "verify_identity", "compute", "plot"],
                "description": "Type of validation to perform"
            },
            "assumptions": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Assumptions about variables"
            }
        },
        "required": ["expression", "validation_type"]
    }
)

CREATE_INTERACTIVE_VISUAL_TOOL = Tool(
    name="create_interactive_visual",
    description="Create an interactive mathematical visualization",
    inputSchema={
        "type": "object",
        "properties": {
            "concept": {
                "type": "string",
                "description": "Mathematical concept for interaction"
            },
            "parameters": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "min": {"type": "number"},
                        "max": {"type": "number"},
                        "default": {"type": "number"}
                    }
                },
                "description": "Interactive parameters"
            },
            "output_type": {
                "type": "string",
                "enum": ["html", "jupyter_widget", "dash_app"],
                "description": "Type of interactive output"
            }
        },
        "required": ["concept", "parameters"]
    }
)

# Tool registry
TOOLS = [
    CREATE_MANIM_ANIMATION_TOOL,
    CREATE_STATIC_DIAGRAM_TOOL,
    VALIDATE_WITH_WOLFRAM_TOOL,
    CREATE_INTERACTIVE_VISUAL_TOOL
]

# Register list_tools handler
@server.list_tools()
async def handle_list_tools() -> List[Tool]:
    return TOOLS

# Visualization functions
def generate_manim_code(concept: str, animation_type: str, style: str, equations: List[str] = None) -> str:
    """Generate Manim code for the animation"""
    
    # Generate class name
    class_name = "".join(word.capitalize() for word in concept.split())
    
    # Start building the code
    code = f"""from manim import *

class {class_name}(Scene):
    def construct(self):
        # Animation: {concept}
        # Style: {style}
        
"""
    
    # Add style-specific configuration
    if style == "3blue1brown":
        code += """        self.camera.background_color = "#1e1e1e"
        Text.set_default(font="Arial", color=BLUE)
        
"""
    elif style == "minimalist":
        code += """        self.camera.background_color = WHITE
        Text.set_default(color=BLACK)
        
"""
    
    # Add animation-specific code
    if animation_type == "2d_plot":
        code += """        # Create axes
        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            axis_config={"color": BLUE},
        )
        
        # Add grid
        axes.add_coordinates()
        
        # Create function
        graph = axes.plot(lambda x: x**2, color=GREEN)
        
        # Animate
        self.play(Create(axes), run_time=2)
        self.play(Create(graph), run_time=2)
        self.wait()
"""
    elif animation_type == "3d_surface":
        # Change the class definition for 3D scenes
        code = code.replace("(Scene):", "(ThreeDScene):")
        
        code += """        # Create 3D axes
        axes = ThreeDAxes()
        
        # Create surface
        surface = Surface(
            lambda u, v: axes.c2p(u, v, u**2 + v**2),
            u_range=[-2, 2],
            v_range=[-2, 2],
            resolution=(30, 30)
        )
        
        # Set camera
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        
        # Animate
        self.play(Create(axes))
        self.play(Create(surface))
        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(5)
"""
    elif animation_type == "transformation":
        code += """        # Create grid
        grid = NumberPlane()
        
        # Create transformation
        def transform_func(point):
            x, y, z = point
            return np.array([x + 0.5 * y, y + 0.5 * x, z])
        
        # Apply transformation
        self.play(Create(grid))
        self.wait()
        self.play(grid.animate.apply_function(transform_func))
        self.wait()
"""
    
    # Add equations if provided
    if equations:
        code += """
        # Display equations
"""
        for i, eq in enumerate(equations):
            code += f"""        eq{i} = MathTex(r"{eq}")
        self.play(Write(eq{i}))
        self.wait()
        
"""
    
    return code

async def create_manim_animation(
    concept: str,
    animation_type: str,
    style: str = "3blue1brown",
    duration: int = 30,
    equations: List[str] = None,
    output_path: str = None
) -> Dict[str, Any]:
    """Create a Manim animation"""
    
    # Generate unique filename
    hash_obj = hashlib.md5(f"{concept}{animation_type}{datetime.now()}".encode())
    filename = f"manim_{hash_obj.hexdigest()[:8]}"
    
    # Ensure output directory exists
    output_dir = ensure_directory(config['paths']['manim_output'])
    
    # Generate Manim code
    manim_code = generate_manim_code(concept, animation_type, style, equations)
    
    # Save Manim file
    manim_file = output_dir / f"{filename}.py"
    with open(manim_file, 'w') as f:
        f.write(manim_code)
    
    # Run Manim
    quality_setting = config['settings']['manim_quality']
    
    # Map quality settings to Manim's single-letter codes
    quality_map = {
        'low_quality': 'l',
        'medium_quality': 'm',
        'high_quality': 'h',
        'production_quality': 'p',
        '4k_quality': 'k',
        'l': 'l',
        'm': 'm',
        'h': 'h',
        'p': 'p',
        'k': 'k'
    }
    quality = quality_map.get(quality_setting, 'm')  # Default to medium
    
    # Get the class name from the generated code
    class_name = "".join(word.capitalize() for word in concept.split())
    
    # Build the command - manim needs the class name, not the filename pattern
    cmd = [
        "manim", 
        "-q", quality,
        "--disable_caching",
        str(manim_file),
        class_name
    ]
    
    try:
        logger.info(f"Running Manim command: {' '.join(cmd)}")
        
        # Run Manim subprocess
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(output_dir))
        
        if result.returncode == 0:
            # Find the actual output file
            # Manim creates videos in media/videos/<script_name>/<quality>/<ClassName>.mp4
            # The quality folder name depends on the quality setting
            quality_folder_map = {
                'l': '480p15',
                'm': '720p30',
                'h': '1080p30',
                'p': '1080p60',
                'k': '2160p60'
            }
            quality_folder = quality_folder_map.get(quality, '720p30')
            
            media_dir = output_dir / "media" / "videos" / filename / quality_folder
            video_files = list(media_dir.glob("*.mp4")) if media_dir.exists() else []
            
            if video_files:
                video_file = video_files[0]
                logger.info(f"Animation created successfully: {video_file}")
                
                # Handle custom output path if specified
                final_video_path = str(video_file)
                if output_path:
                    import shutil
                    # Ensure output_path is relative to Dropbox
                    dropbox_base = "/Users/scottbroock/Dropbox"
                    custom_path = Path(dropbox_base) / output_path.strip('/')
                    
                    # Create parent directory if needed
                    custom_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    # Copy the video to the custom location
                    try:
                        shutil.copy2(video_file, custom_path)
                        logger.info(f"Video copied to custom location: {custom_path}")
                        final_video_path = str(custom_path)
                    except Exception as e:
                        logger.error(f"Failed to copy to custom location: {e}")
                        # Still return success but note the copy failure
                
                return {
                    "status": "success",
                    "animation_file": final_video_path,
                    "source_file": str(manim_file),
                    "concept": concept,
                    "type": animation_type,
                    "duration": duration,
                    "creation_time": datetime.now().isoformat(),
                    "manim_output": result.stdout,
                    "original_location": str(video_file) if output_path else None
                }
            else:
                # Also check without quality folder (some versions of Manim)
                media_dir_alt = output_dir / "media" / "videos" / filename
                video_files_alt = list(media_dir_alt.glob("**/*.mp4")) if media_dir_alt.exists() else []
                
                if video_files_alt:
                    video_file = video_files_alt[0]
                    logger.info(f"Animation created successfully: {video_file}")
                    
                    # Handle custom output path if specified
                    final_video_path = str(video_file)
                    if output_path:
                        import shutil
                        # Ensure output_path is relative to Dropbox
                        dropbox_base = "/Users/scottbroock/Dropbox"
                        custom_path = Path(dropbox_base) / output_path.strip('/')
                        
                        # Create parent directory if needed
                        custom_path.parent.mkdir(parents=True, exist_ok=True)
                        
                        # Copy the video to the custom location
                        try:
                            shutil.copy2(video_file, custom_path)
                            logger.info(f"Video copied to custom location: {custom_path}")
                            final_video_path = str(custom_path)
                        except Exception as e:
                            logger.error(f"Failed to copy to custom location: {e}")
                            # Still return success but note the copy failure
                    
                    return {
                        "status": "success",
                        "animation_file": final_video_path,
                        "source_file": str(manim_file),
                        "concept": concept,
                        "type": animation_type,
                        "duration": duration,
                        "creation_time": datetime.now().isoformat(),
                        "manim_output": result.stdout,
                        "original_location": str(video_file) if output_path else None
                    }
                else:
                    logger.error(f"No video file found after Manim execution")
                    logger.error(f"Searched in: {media_dir} and {media_dir_alt}")
                    return {
                        "status": "error",
                        "error": "Video file not found after Manim execution",
                        "concept": concept,
                        "stdout": result.stdout,
                        "stderr": result.stderr
                    }
        else:
            logger.error(f"Manim failed with return code {result.returncode}")
            logger.error(f"Stdout: {result.stdout}")
            logger.error(f"Stderr: {result.stderr}")
            
            return {
                "status": "error",
                "error": f"Manim failed with return code {result.returncode}",
                "concept": concept,
                "stdout": result.stdout,
                "stderr": result.stderr
            }
    except Exception as e:
        logger.error(f"Error creating animation: {e}")
        return {
            "status": "error",
            "error": str(e),
            "concept": concept
        }

async def validate_with_wolfram(
    expression: str,
    validation_type: str,
    assumptions: List[str] = None
) -> Dict[str, Any]:
    """Validate mathematical expressions with Wolfram Alpha"""
    
    app_id = config['api_keys']['wolfram']
    if not app_id:
        return {"error": "Wolfram Alpha App ID not configured"}
    
    # Build query
    query = expression
    if assumptions:
        query += " assuming " + " and ".join(assumptions)
    
    # Wolfram Alpha API endpoint
    base_url = "http://api.wolframalpha.com/v2/query"
    
    params = {
        "appid": app_id,
        "input": query,
        "format": "plaintext",
        "output": "json"
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(base_url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    # Parse Wolfram response
                    if data.get("queryresult", {}).get("success"):
                        pods = data["queryresult"].get("pods", [])
                        
                        results = []
                        for pod in pods:
                            if pod.get("subpods"):
                                for subpod in pod["subpods"]:
                                    if subpod.get("plaintext"):
                                        results.append({
                                            "title": pod.get("title", ""),
                                            "value": subpod["plaintext"]
                                        })
                        
                        return {
                            "status": "success",
                            "expression": expression,
                            "validation_type": validation_type,
                            "results": results,
                            "timestamp": datetime.now().isoformat()
                        }
                    else:
                        return {
                            "status": "no_results",
                            "expression": expression,
                            "message": "Wolfram Alpha could not interpret the expression"
                        }
                else:
                    return {
                        "status": "error",
                        "error": f"API request failed with status {response.status}"
                    }
    except Exception as e:
        logger.error(f"Error validating with Wolfram: {e}")
        return {
            "status": "error",
            "error": str(e)
        }

async def create_static_diagram(
    diagram_type: str,
    elements: Dict[str, Any],
    labels: List[str] = None,
    output_format: str = "svg"
) -> Dict[str, Any]:
    """Create a static mathematical diagram"""
    
    # This would use matplotlib, tikz, or other libraries in production
    # For now, return a template response
    
    output_dir = ensure_directory(config['paths']['manim_output'])
    filename = f"diagram_{diagram_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{output_format}"
    
    return {
        "status": "success",
        "diagram_file": str(output_dir / filename),
        "diagram_type": diagram_type,
        "elements_count": len(elements),
        "format": output_format,
        "creation_time": datetime.now().isoformat()
    }

async def create_interactive_visual(
    concept: str,
    parameters: List[Dict[str, Any]],
    output_type: str = "html"
) -> Dict[str, Any]:
    """Create an interactive visualization"""
    
    # This would create actual interactive visualizations in production
    # Using plotly, bokeh, or custom JavaScript
    
    output_dir = ensure_directory(config['paths']['manim_output'])
    filename = f"interactive_{concept.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{output_type}"
    
    return {
        "status": "success",
        "interactive_file": str(output_dir / filename),
        "concept": concept,
        "parameters": parameters,
        "output_type": output_type,
        "creation_time": datetime.now().isoformat()
    }

# Tool handlers
@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> List[TextContent]:
    """Handle tool calls"""
    if name == "create_manim_animation":
        result = await create_manim_animation(**arguments)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    elif name == "create_static_diagram":
        result = await create_static_diagram(**arguments)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    elif name == "validate_with_wolfram":
        result = await validate_with_wolfram(**arguments)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    elif name == "create_interactive_visual":
        result = await create_interactive_visual(**arguments)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    else:
        return [TextContent(type="text", text=json.dumps({"error": f"Unknown tool: {name}"}))]

async def main():
    """Main entry point for the MCP server"""
    logger.info("Starting Mathematical Visualization Agent...")
    
    # Ensure output directories exist
    ensure_directory(config['paths']['manim_output'])
    
    # Run the server
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="mathematical-visualization-agent",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())