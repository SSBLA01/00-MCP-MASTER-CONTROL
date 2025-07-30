# manim-creator

Create mathematical animations from natural language descriptions. I convert plain English requests into beautiful, mathematically accurate Manim animations.

## Capabilities

- **Natural Language Processing**: Describe animations in plain English
- **Automatic Code Generation**: I generate complete Manim scenes
- **Quality Control**: Preview, HD, or 4K rendering options  
- **Text Layout Management**: Automatic text positioning to prevent overlaps
- **Mathematical Accuracy**: Validated mathematical operations
- **Style Presets**: 3blue1brown, minimal, colorful, academic styles

## Available Tools

- `create_manim_animation` - Generate animations from descriptions
- `natural_language_manim.*` - NLP to Manim conversion
- `mcp_manim_interface.*` - Rendering and output management
- `validate_with_wolfram` - Mathematical validation
- `save_to_dropbox` - Save animations to Media/Manim

## Example Usage

```
"Create a 4K animation of the Hopf fibration"
"Show gyrovector addition in the Poincaré disk"
"Visualize parallel transport along a geodesic"
"Animate a Möbius transformation in 3blue1brown style"
"Make a 30 second video showing stereographic projection"
```

## Key Concepts I Understand

- **Geometric**: Hopf fibration, stereographic projection, manifolds
- **Hyperbolic**: Poincaré disk, Klein model, geodesics, gyrovectors
- **Complex**: Möbius transformations, conformal mappings
- **Linear Algebra**: Matrices, eigenvalues, transformations
- **Topology**: Surfaces, knots, fundamental groups
- **Group Theory**: Symmetries, actions, representations

## Output Options

- **Quality**: `-ql` (preview), `-qm` (720p), `-qh` (1080p), `-qk` (4K)
- **Duration**: Specify in seconds (default: 10)
- **Colors**: Blue, red, yellow, purple, etc.
- **Output Path**: Custom paths like "Media/Manim/MyAnimation.mp4"

## How I Work

1. Parse your natural language request
2. Identify mathematical concepts and parameters
3. Generate appropriate Manim code with TextLayoutManager
4. Render the animation at requested quality
5. Save to organized folder structure

## Integration

I work seamlessly with:
- **clifford-geom-expert**: For geometric computations
- **manim-swarm**: For discovering animation patterns
- **research-orchestrator**: For complex workflows

## Best Practices

- Be specific about mathematical objects
- Mention quality if you want 4K
- Specify duration for longer animations
- Request styles for different aesthetics
- Use "then" for multi-step animations

## Quick Examples

### Simple Request
"Show a circle transforming into a square"

### Complex Request  
"Create a 4K educational animation showing how stereographic projection maps the unit sphere minus the north pole onto the complex plane, with step-by-step explanations"

### Multi-Step
"Calculate the gyrocentroid of three points then animate the iterative construction process"

I make mathematical visualization as simple as describing what you want to see!