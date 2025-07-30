# Natural Language Manim Interface

The MCP system now supports creating Manim animations using plain English descriptions through Claude Desktop.

## Quick Start

Simply tell Claude what animation you want:
- "Create a 4K Hopf fibration animation"
- "Show me gyrovector addition in the Poincaré disk"
- "Make a Möbius transformation with colorful style"

## Key Features

### ✅ Text Overlap Prevention
- Automatic text positioning with `TextLayoutManager`
- Smart collision detection and adjustment
- Works in both 2D and 3D scenes
- Background rectangles for readability

### 🎯 Natural Language Understanding
- Mathematical concepts (Hopf fibration, gyrovectors, etc.)
- Quality settings (4K, 1080p, 720p)
- Visual styles (3blue1brown, minimal, colorful)
- Duration control ("30 second animation")
- Color preferences ("blue and purple")

### 🚀 Seamless Integration
- Works directly through Claude Desktop
- Automatic code generation
- Integrated rendering pipeline
- Custom output paths supported

## Implementation

The system consists of:
1. **natural_language_manim.py** - Core NLP to Manim converter
2. **mcp_manim_interface.py** - MCP integration layer
3. **TextLayoutManager** - Prevents text overlapping

## Example Generated Code

```python
class HopfFibration_20250730134300(ThreeDScene):
    def construct(self):
        # Style configuration
        self.camera.background_color = "#0e1117"
        
        # Text layout manager prevents overlaps
        layout = TextLayoutManager()
        
        # Animation content...
```

## Usage Through MCP

The natural language interface is now part of the standard MCP Manim tool:
- Processes plain English requests
- Generates appropriate Manim code
- Handles text positioning automatically
- Renders to specified quality
- Outputs to organized folder structure

This makes creating complex mathematical animations as simple as describing them in words!
