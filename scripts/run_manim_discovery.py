#!/usr/bin/env python3
"""
Quick Start: Run Manim GitHub Discovery Swarm
This script demonstrates how to use MCP tools to discover Manim patterns
"""

import json
from datetime import datetime

def run_manim_discovery():
    """
    Execute the Manim discovery workflow using MCP commands
    """
    
    print("="*60)
    print("Manim GitHub Discovery Swarm - Quick Start")
    print("="*60)
    print()
    
    # These are the MCP commands to execute in Claude Desktop
    commands = [
        # 1. Search for gyrovector animations
        {
            "step": "Search for gyrovector implementations",
            "command": 'web_search("site:github.com manim gyrovector hyperbolic geometry animation")',
            "purpose": "Find repositories with gyrovector visualizations"
        },
        
        # 2. Search for stereographic projections
        {
            "step": "Search for stereographic projection examples",
            "command": 'web_search("site:github.com manim stereographic projection S3 sphere filetype:py")',
            "purpose": "Find advanced projection implementations"
        },
        
        # 3. Search for educational examples
        {
            "step": "Search for well-documented examples",
            "command": 'web_search("site:github.com manim examples mathematical tutorial")',
            "purpose": "Find repositories with good documentation"
        },
        
        # 4. Parse and analyze results
        {
            "step": "Initialize searcher and parse results",
            "command": """
# Import the searcher
from src.manim_github_searcher import ManimGitHubSearcher
searcher = ManimGitHubSearcher()

# Parse the search results
repos = searcher.parse_search_results(search_result)
print(f"Found {len(repos)} repositories")
""",
            "purpose": "Extract GitHub URLs from search results"
        },
        
        # 5. Fetch specific examples
        {
            "step": "Fetch a specific animation file",
            "command": 'web_fetch("https://github.com/ManimCommunity/manim/blob/main/example_scenes/basic.py")',
            "purpose": "Get actual code from repository"
        },
        
        # 6. Analyze code quality
        {
            "step": "Analyze code with Gemini",
            "command": 'gemini_analyze_code(code=fetched_code, analysis_type="quality")',
            "purpose": "Assess code quality and reusability"
        },
        
        # 7. Extract patterns
        {
            "step": "Extract reusable patterns",
            "command": """
# Analyze the code
analysis = searcher.analyze_code_snippet(fetched_code)

# Extract pattern if valuable
if analysis["mathematical_concepts"]:
    pattern = searcher.extract_reusable_pattern(
        fetched_code,
        analysis["mathematical_concepts"][0]
    )
""",
            "purpose": "Extract reusable animation patterns"
        },
        
        # 8. Save to knowledge base
        {
            "step": "Save pattern to Obsidian",
            "command": """
ingest_to_obsidian(
    content=pattern.to_obsidian_note(),
    title=f"Manim Pattern - {pattern['concept']}",
    category="concepts",
    tags=["manim", "pattern", "github"]
)""",
            "purpose": "Store pattern in knowledge base"
        },
        
        # 9. Generate report
        {
            "step": "Generate discovery report",
            "command": """
# Generate comprehensive report
report = searcher.generate_search_report()
obsidian_note = searcher.format_for_obsidian("discovery_session")

# Save report
ingest_to_obsidian(
    content=obsidian_note,
    title=f"Manim Discovery Report - {datetime.now().strftime('%Y-%m-%d')}",
    category="daily_notes"
)""",
            "purpose": "Create summary of discoveries"
        }
    ]
    
    # Print commands for manual execution
    print("Execute these commands in Claude Desktop:\n")
    
    for i, cmd in enumerate(commands, 1):
        print(f"Step {i}: {cmd['step']}")
        print(f"Purpose: {cmd['purpose']}")
        print(f"Command:")
        print("-" * 40)
        print(cmd['command'])
        print("-" * 40)
        print()
    
    # Additional workflow for specific concepts
    print("\n" + "="*60)
    print("Advanced Discovery Workflows")
    print("="*60)
    print()
    
    advanced_workflows = {
        "Gyrovector Spaces": [
            'web_search("site:github.com manim poincare disk gyroaddition")',
            'web_search("site:github.com manim hyperbolic parallel transport")',
            'web_search("site:github.com manim einstein velocity addition")'
        ],
        "Topology Animations": [
            'web_search("site:github.com manim manifold fiber bundle")',
            'web_search("site:github.com manim homotopy fundamental group")',
            'web_search("site:github.com manim homology visualization")'
        ],
        "Advanced 3D": [
            'web_search("site:github.com manim ThreeDScene camera movement")',
            'web_search("site:github.com manim custom shader mathematical")',
            'web_search("site:github.com manim parametric surface animation")'
        ]
    }
    
    for concept, searches in advanced_workflows.items():
        print(f"\n{concept}:")
        for search in searches:
            print(f"  - {search}")
    
    # Create batch processing script
    batch_script = """
# Batch Discovery Script
# Run this to discover patterns for multiple concepts

concepts = ["gyrovector", "stereographic", "topology", "mobius"]
all_patterns = []

for concept in concepts:
    print(f"\\nDiscovering patterns for: {concept}")
    
    # Get search queries
    queries = searcher.get_search_queries(concept)
    
    # Execute searches
    for query in queries[:3]:  # Limit to 3 per concept
        result = web_search(query)
        repos = searcher.parse_search_results(result)
        
        # Analyze top repositories
        for repo in repos[:2]:  # Top 2 repos
            if repo["type"] == "file":
                try:
                    code = web_fetch(repo["url"])
                    pattern = searcher.extract_reusable_pattern(code, concept)
                    if pattern:
                        all_patterns.append(pattern)
                except:
                    continue

# Save all patterns
for pattern in all_patterns:
    save_to_dropbox(
        content=json.dumps(pattern, indent=2),
        file_path=f"MCP_Tools/manim_patterns/{pattern['pattern_id']}.json"
    )

print(f"\\nDiscovered {len(all_patterns)} patterns!")
"""
    
    print("\n" + "="*60)
    print("Batch Discovery Script")
    print("="*60)
    print(batch_script)
    
    # Integration tips
    print("\n" + "="*60)
    print("Integration Tips")
    print("="*60)
    print("""
1. Run discovery weekly to find new patterns
2. Validate mathematical accuracy with Wolfram Alpha
3. Test animations locally before adding to templates
4. Share valuable patterns back to the community
5. Build a curated library of high-quality examples

Remember: The goal is to learn from the community and enhance our
mathematical visualization capabilities!
""")


if __name__ == "__main__":
    run_manim_discovery()
