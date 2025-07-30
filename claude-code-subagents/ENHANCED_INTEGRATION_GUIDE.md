# Enhanced Agent Integration Guide

## Quick Start: Plain English to Mathematical Animation

This guide shows how to use the enhanced Manim and geometry agents to create mathematically accurate animations from natural language descriptions.

## 1. Basic Animation Request

```python
from src.nlp_manim_pipeline import process_animation_request

# Simple request
result = process_animation_request(
    "Show gyroaddition of two vectors in the Poincaré disk"
)

if result["success"]:
    # Save and run the generated code
    with open("my_animation.py", "w") as f:
        f.write(result["manim_code"])
    
    # Run with Manim
    # manim -pql my_animation.py GeneratedAnimation
```

## 2. Advanced Geometric Visualization

```python
# Complex stereographic projection
result = process_animation_request("""
    Create a 4K animation showing a stereographic projection of an S³ sphere 
    onto a polar plane. First show the sphere rotating to reveal its structure, 
    then project it onto the plane below. Finally, rotate the plane relative 
    to the projection pole to show how the projection changes. Make it 8 seconds 
    long with artistic lighting.
""")

# The pipeline will:
# 1. Parse the request to identify S³, stereographic projection, rotations
# 2. Validate the mathematical operations
# 3. Generate appropriate Manim code with artistic styling
# 4. Set up 4K rendering parameters
```

## 3. Using Agent Collaboration

### Example: Gyrovector Research Visualization

```bash
# In Claude Desktop, use the agents together:

"Using the clifford-geom-expert agent, compute the gyrocentroid of points 
[0.2,0.3,0], [0.1,0.4,0.2], and [0.3,0.1,0.1] in the Poincaré ball model"

# Then:

"Using the math-animator agent, create a visualization showing the 
iterative gyroaddition process from the previous computation, with 
geodesic paths between points"
```

### Example: Orbifold Analysis

```bash
# Step 1: Analyze with geometry expert
"Using the clifford-geom-expert agent, analyze the orbifold structure 
of the quotient of H² by the (2,3,7) triangle group"

# Step 2: Visualize the results
"Using the math-animator agent, create an animation showing the 
fundamental domain from the previous analysis in the Poincaré disk model"
```

## 4. Integration with MCP Tools

### Complete Workflow Example

```python
# 1. Research Discovery
"Use discover_research to find recent papers on gyrovector spaces 
in hyperbolic geometry"

# 2. Geometric Analysis
"Using clifford-geom-expert, implement the main theorem from the 
first paper about gyrovector parallel transport"

# 3. Visualization
"Using math-animator, create an educational animation demonstrating 
the parallel transport concept from the previous step"

# 4. Knowledge Management
"Save the animation and analysis to Obsidian with proper tags 
and cross-references"
```

## 5. Custom Animation Templates

You can extend the system with custom templates:

```python
# Add to math-animator templates
custom_template = {
    "gyrovector_field": {
        "description": "Visualize gyrovector field dynamics",
        "parameters": ["field_function", "domain", "color_map"],
        "code": '''
        # Custom gyrovector field visualization
        field = GyroveorField(
            func=lambda p: gyro_transform(p),
            domain=PoincareDisk(radius=3)
        )
        self.play(ShowField(field), run_time=5)
        '''
    }
}
```

## 6. Performance Tips

### For Complex Computations
```python
# Use exact mode for proofs
"Using clifford-geom-expert in exact mode, prove that gyroaddition 
is associative in the Einstein velocity addition model"

# Use optimized mode for animations
"Using clifford-geom-expert in optimized mode, compute 1000 points 
on a geodesic for smooth animation"
```

### For High-Quality Output
```python
# Preview first
result = process_animation_request(
    "Your animation description here",
    quality="preview"  # Fast preview
)

# Then render in 4K
result = process_animation_request(
    "Same description",
    quality="4k"  # Final quality
)
```

## 7. Common Patterns

### Pattern 1: Concept Explanation
```
"Create an educational animation explaining [mathematical concept] 
by showing [specific example] with step-by-step transformations"
```

### Pattern 2: Theorem Visualization
```
"Visualize the proof of [theorem name] by animating the construction 
in [specific model/space] with highlighted key steps"
```

### Pattern 3: Comparative Analysis
```
"Show the difference between [concept A] and [concept B] by creating 
side-by-side animations in the same mathematical space"
```

## 8. Troubleshooting

### Issue: Ambiguous Descriptions
```python
# Be specific about mathematical objects
# Bad: "Show a sphere projection"
# Good: "Show stereographic projection of S² sphere onto complex plane"
```

### Issue: Invalid Coordinates
```python
# The system validates coordinates
# For Poincaré ball: ||v|| < 1
# For sphere: ||v|| = 1
# System will warn about invalid inputs
```

### Issue: Complex Transformations
```python
# Break down complex requests
# Instead of one complex request, use:
step1 = process_animation_request("First transformation...")
step2 = process_animation_request("Second transformation...")
# Then combine the generated code
```

## 9. Integration with Existing Tools

### With Obsidian
```bash
# After generating animation:
"Save the animation code and mathematical details to Obsidian 
under 'Visualizations/Gyrovectors' with tags #manim #gyrovector"
```

### With Claude Flow
```bash
# For batch processing:
"Using Claude Flow, generate animations for all gyrovector operations 
in parallel: addition, scalar multiplication, and parallel transport"
```

### With Dropbox
```bash
# Organized storage:
"Save the generated animation to Dropbox under 
Media/Manim/Gyrovectors/[timestamp]_description.mp4"
```

## 10. Best Practices

1. **Start Simple**: Test with basic animations before complex ones
2. **Validate First**: Use clifford-geom-expert to validate mathematics
3. **Preview Mode**: Always preview before 4K rendering
4. **Document Well**: Save both code and mathematical explanations
5. **Reuse Templates**: Build a library of common animations
6. **Version Control**: Commit generated code to GitHub
7. **Tag Properly**: Use consistent tags in Obsidian for easy retrieval

## Next Steps

1. Run the test script: `python tests/test_enhanced_agents.py`
2. Install the agents in Claude Code environment
3. Try the examples in this guide
4. Extend with your own mathematical concepts
5. Share successful animations in the research repository