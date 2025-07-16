"""
Example: Gyrovector Research Workflow with Kimi K2
=================================================

This example demonstrates how to use Kimi K2 with other MCP tools
for a complete mathematical research workflow.
"""

# Example workflow for investigating gyrovector properties

async def gyrovector_research_workflow():
    """
    Complete workflow using Kimi K2 and other tools
    """
    
    # 1. Start with Kimi K2 to understand the concept
    understanding = await call_tool("kimi_k2_query", {
        "prompt": """Explain the relationship between gyrovector spaces 
        and hyperbolic geometry, focusing on:
        1. The Poincaré ball model
        2. Gyroaddition and its properties
        3. Applications to special relativity"""
    })
    
    # 2. Research existing literature
    papers = await call_tool("discover_research", {
        "query": "gyrovector spaces hyperbolic geometry applications",
        "sources": ["arxiv", "perplexity"],
        "max_results": 5
    })
    
    # 3. Solve a specific problem
    solution = await call_tool("kimi_k2_solve_problem", {
        "problem": """In the Poincaré ball model with c=1:
        1. Given u = [0.3, 0.4, 0] and v = [0.2, 0.1, 0.3]
        2. Calculate u ⊕ v (gyroaddition)
        3. Verify ||u ⊕ v|| < 1
        4. Calculate the gyrodistance d(u, v)
        5. Find the midpoint m = u ⊕_{1/2} v""",
        "domain": "gyrovector",
        "validate": True
    })
    
    # 4. Generate visualization
    visualization = await call_tool("kimi_k2_generate_visualization", {
        "concept": "Gyrovector addition and parallel transport in Poincaré disk",
        "animation_type": "geometric_construction",
        "style": "3blue1brown"
    })
    
    # 5. Validate key results with Wolfram
    validation = await call_tool("validate_with_wolfram", {
        "expression": "||[0.3, 0.4, 0] ⊕ [0.2, 0.1, 0.3]|| < 1",
        "validation_type": "verify_identity",
        "assumptions": ["Poincaré ball model", "c = 1"]
    })
    
    # 6. Create knowledge artifact
    note = await call_tool("ingest_to_obsidian", {
        "title": "Gyrovector Spaces - Complete Analysis",
        "content": f"""# Gyrovector Spaces Analysis

## Understanding
{understanding['content']}

## Literature Review
{papers['data']}

## Calculations
{solution['content']}

## Validation
{validation['data']}

## Visualization
Generated Manim code saved to: {visualization.get('saved_to', 'N/A')}

## Tags
#gyrovector #hyperbolic-geometry #poincare-model #kimi-k2
""",
        "category": "concepts",
        "tags": ["gyrovector", "hyperbolic-geometry", "kimi-k2"]
    })
    
    # 7. Collaborative analysis for deeper insights
    collaboration = await call_tool("kimi_k2_collaborative_reasoning", {
        "task": """Investigate potential applications of gyrovector spaces to:
        1. Quantum information theory
        2. Machine learning on hyperbolic manifolds
        3. Network embedding in hyperbolic space""",
        "agents": ["kimi_k2", "claude_flow_queen", "gemini_ai"],
        "workflow_type": "parallel"
    })
    
    return {
        "understanding": understanding,
        "papers": papers,
        "solution": solution,
        "visualization": visualization,
        "validation": validation,
        "knowledge": note,
        "collaboration": collaboration
    }

# Usage example:
# results = await gyrovector_research_workflow()
# print(json.dumps(results, indent=2))
