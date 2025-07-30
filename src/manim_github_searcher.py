#!/usr/bin/env python3
"""
Practical Manim GitHub Discovery Tool
Uses MCP web_search to find real Manim examples across GitHub
"""

import json
import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime

class ManimGitHubSearcher:
    """Search GitHub for Manim animation examples and patterns"""
    
    def __init__(self):
        self.search_results = []
        self.discovered_repos = []
        self.pattern_library = {}
        
    def get_search_queries(self, focus_area: str = "all") -> List[str]:
        """Generate optimized search queries for GitHub"""
        
        base_queries = {
            "gyrovector": [
                'site:github.com "from manim import" gyrovector',
                'site:github.com "class.*Scene" gyroaddition filetype:py',
                'site:github.com manim "poincare disk" animation',
                'site:github.com manim hyperbolic geometry visualization'
            ],
            "stereographic": [
                'site:github.com "from manim import" "stereographic projection"',
                'site:github.com manim "S3 sphere" projection filetype:py',
                'site:github.com manim stereographic animation code'
            ],
            "topology": [
                'site:github.com manim manifold visualization filetype:py',
                'site:github.com "from manim import" topology',
                'site:github.com manim "fiber bundle" animation',
                'site:github.com manim homotopy visualization'
            ],
            "mobius": [
                'site:github.com manim "mobius transformation" filetype:py',
                'site:github.com manim conformal mapping animation',
                'site:github.com "from manim import" mobius'
            ],
            "examples": [
                'site:github.com path:examples manim mathematical',
                'site:github.com "manim examples" geometry',
                'site:github.com inurl:manim-examples mathematical'
            ],
            "educational": [
                'site:github.com manim tutorial mathematical animations',
                'site:github.com "learning manim" geometry examples',
                'site:github.com manim course mathematical visualization'
            ]
        }
        
        if focus_area == "all":
            return [q for queries in base_queries.values() for q in queries]
        else:
            return base_queries.get(focus_area, [])
    
    def parse_search_results(self, search_output: str) -> List[Dict]:
        """Parse web_search results to extract GitHub repositories"""
        repos = []
        
        # Extract GitHub URLs and descriptions
        github_pattern = r'(https://github\.com/[\w-]+/[\w-]+(?:/[\w/-]+)?)'
        
        for line in search_output.split('\n'):
            match = re.search(github_pattern, line)
            if match:
                url = match.group(1)
                
                # Try to extract surrounding context as description
                description = line.strip()
                
                repo_info = {
                    "url": url,
                    "description": description,
                    "type": self._classify_url(url),
                    "discovered_at": datetime.now().isoformat()
                }
                
                # Avoid duplicates
                if not any(r["url"] == url for r in repos):
                    repos.append(repo_info)
        
        return repos
    
    def _classify_url(self, url: str) -> str:
        """Classify the type of GitHub URL"""
        if "/blob/" in url or url.endswith(".py"):
            return "file"
        elif "/tree/" in url or "/examples" in url:
            return "directory"
        elif url.count("/") == 4:  # Basic repo URL
            return "repository"
        else:
            return "other"
    
    def analyze_code_snippet(self, code: str) -> Dict:
        """Analyze a code snippet for Manim patterns"""
        analysis = {
            "has_manim_import": False,
            "scene_classes": [],
            "animation_methods": [],
            "mathematical_concepts": [],
            "complexity": "low",
            "educational_value": "unknown"
        }
        
        # Check for Manim imports
        if "from manim import" in code or "import manim" in code:
            analysis["has_manim_import"] = True
        
        # Find Scene classes
        scene_pattern = r'class\s+(\w+)\s*\(\s*(?:Three)?(?:D)?Scene\s*\)'
        scenes = re.findall(scene_pattern, code)
        analysis["scene_classes"] = scenes
        
        # Find animation methods
        animation_methods = [
            "Create", "Transform", "FadeIn", "FadeOut", "Rotate",
            "Scale", "Shift", "MoveToTarget", "ApplyMethod",
            "AnimationGroup", "Succession", "Write", "ShowCreation"
        ]
        found_methods = []
        for method in animation_methods:
            if method in code:
                found_methods.append(method)
        analysis["animation_methods"] = found_methods
        
        # Detect mathematical concepts
        math_concepts = {
            "gyrovector": ["gyro", "poincare", "hyperbolic"],
            "projection": ["project", "stereographic", "orthogonal"],
            "transformation": ["transform", "mobius", "conformal"],
            "topology": ["manifold", "bundle", "homology"],
            "geometry": ["euclidean", "riemannian", "differential"]
        }
        
        found_concepts = []
        code_lower = code.lower()
        for concept, keywords in math_concepts.items():
            if any(keyword in code_lower for keyword in keywords):
                found_concepts.append(concept)
        analysis["mathematical_concepts"] = found_concepts
        
        # Assess complexity
        line_count = code.count('\n')
        if line_count > 100 and len(found_methods) > 5:
            analysis["complexity"] = "high"
        elif line_count > 50 or len(found_methods) > 3:
            analysis["complexity"] = "medium"
        
        # Educational value (heuristic)
        if any(marker in code for marker in ["#", "'''", '"""', "NOTE:", "TODO:"]):
            if line_count > 30:
                analysis["educational_value"] = "high"
            else:
                analysis["educational_value"] = "medium"
        
        return analysis
    
    def extract_reusable_pattern(self, code: str, concept: str) -> Optional[Dict]:
        """Extract a reusable pattern from code"""
        pattern = {
            "concept": concept,
            "code_template": "",
            "required_imports": [],
            "example_usage": "",
            "notes": []
        }
        
        # Extract imports
        import_pattern = r'from manim import (.+)|import manim'
        imports = re.findall(import_pattern, code)
        if imports:
            pattern["required_imports"] = [imp.strip() for imp in imports[0].split(',') if imp]
        
        # Try to extract a complete class or function
        class_pattern = rf'class\s+\w+.*?(?=\nclass|\n\n|\Z)'
        classes = re.findall(class_pattern, code, re.DOTALL)
        
        if classes and concept in code.lower():
            pattern["code_template"] = classes[0]
            
            # Extract any comments as notes
            comment_pattern = r'#\s*(.+)'
            comments = re.findall(comment_pattern, classes[0])
            pattern["notes"] = comments[:3]  # First 3 comments
            
            return pattern
        
        return None
    
    def generate_search_report(self) -> Dict:
        """Generate a comprehensive search report"""
        report = {
            "search_date": datetime.now().isoformat(),
            "total_results": len(self.search_results),
            "unique_repositories": len(set(r["url"].split("/")[:5] for r in self.search_results)),
            "file_results": len([r for r in self.search_results if r["type"] == "file"]),
            "repository_results": len([r for r in self.search_results if r["type"] == "repository"]),
            "discovered_patterns": len(self.pattern_library),
            "top_repositories": self._get_top_repositories(),
            "concept_distribution": self._get_concept_distribution()
        }
        
        return report
    
    def _get_top_repositories(self, limit: int = 10) -> List[str]:
        """Get most frequently appearing repositories"""
        repo_counts = {}
        
        for result in self.search_results:
            repo = "/".join(result["url"].split("/")[:5])
            repo_counts[repo] = repo_counts.get(repo, 0) + 1
        
        sorted_repos = sorted(repo_counts.items(), key=lambda x: x[1], reverse=True)
        return [repo for repo, count in sorted_repos[:limit]]
    
    def _get_concept_distribution(self) -> Dict[str, int]:
        """Get distribution of mathematical concepts found"""
        concept_counts = {}
        
        for pattern in self.pattern_library.values():
            for concept in pattern.get("mathematical_concepts", []):
                concept_counts[concept] = concept_counts.get(concept, 0) + 1
        
        return concept_counts
    
    def format_for_obsidian(self, search_focus: str) -> str:
        """Format search results for Obsidian note"""
        report = self.generate_search_report()
        
        note = f"""# Manim GitHub Discovery - {search_focus.title()}

## Search Summary
- **Date**: {report['search_date']}
- **Total Results**: {report['total_results']}
- **Unique Repositories**: {report['unique_repositories']}
- **Discovered Patterns**: {report['discovered_patterns']}

## Top Repositories
"""
        
        for i, repo in enumerate(report['top_repositories'], 1):
            note += f"{i}. [{repo}]({repo})\n"
        
        note += "\n## Mathematical Concepts Found\n"
        for concept, count in report['concept_distribution'].items():
            note += f"- **{concept}**: {count} occurrences\n"
        
        note += "\n## Valuable Discoveries\n"
        
        # Add specific file discoveries
        file_results = [r for r in self.search_results if r["type"] == "file"][:10]
        for result in file_results:
            note += f"\n### [{result['url'].split('/')[-1]}]({result['url']})\n"
            note += f"{result['description'][:200]}...\n"
        
        note += f"""
## Integration Commands

To fetch and analyze specific repositories:
```python
# Fetch a specific file
web_fetch("{report['top_repositories'][0] if report['top_repositories'] else 'URL'}/blob/main/examples/example.py")

# Analyze with Gemini
gemini_analyze_code(code=fetched_code, analysis_type="general")

# Save pattern to Obsidian
ingest_to_obsidian(content=pattern_note, title="Manim Pattern - [Concept]", category="concepts")
```

## Next Steps
1. Analyze top repositories in detail
2. Extract reusable patterns
3. Create template library
4. Test animations locally

#manim #github #discovery #{search_focus}
"""
        
        return note


def create_mcp_search_commands(focus_areas: List[str]) -> List[str]:
    """Generate MCP commands for searching GitHub"""
    searcher = ManimGitHubSearcher()
    commands = []
    
    for area in focus_areas:
        queries = searcher.get_search_queries(area)
        for query in queries[:3]:  # Limit to first 3 queries per area
            commands.append(f'web_search("{query}")')
    
    return commands


def create_discovery_workflow():
    """Create a complete discovery workflow"""
    workflow = """
# Manim GitHub Discovery Workflow

## Step 1: Initial Search
Execute these searches to find Manim repositories:

```python
# Search for gyrovector animations
result1 = web_search('site:github.com "from manim import" gyrovector')

# Search for stereographic projections  
result2 = web_search('site:github.com manim "stereographic projection" filetype:py')

# Search for example repositories
result3 = web_search('site:github.com path:examples manim mathematical')
```

## Step 2: Analyze Results
Parse the search results to identify valuable repositories:

```python
# Initialize searcher
searcher = ManimGitHubSearcher()

# Parse results
repos1 = searcher.parse_search_results(result1)
repos2 = searcher.parse_search_results(result2)
repos3 = searcher.parse_search_results(result3)

# Combine results
searcher.search_results.extend(repos1 + repos2 + repos3)
```

## Step 3: Fetch Specific Files
For promising files, fetch the actual code:

```python
# Example: Fetch a specific animation file
code = web_fetch("https://github.com/[user]/[repo]/blob/main/animations/gyrovector.py")

# Analyze the code
analysis = searcher.analyze_code_snippet(code)
print(json.dumps(analysis, indent=2))
```

## Step 4: Extract Patterns
Extract reusable patterns from the code:

```python
# Extract pattern for a specific concept
pattern = searcher.extract_reusable_pattern(code, "gyrovector")

if pattern:
    # Save to pattern library
    searcher.pattern_library["gyrovector_example"] = pattern
```

## Step 5: Generate Documentation
Create comprehensive documentation:

```python
# Generate Obsidian note
obsidian_note = searcher.format_for_obsidian("gyrovector")

# Save to Obsidian
ingest_to_obsidian(
    content=obsidian_note,
    title="Manim Discovery - Gyrovector Patterns",
    category="concepts",
    tags=["manim", "github", "patterns", "gyrovector"]
)

# Generate search report
report = searcher.generate_search_report()
print(json.dumps(report, indent=2))
```

## Step 6: Create Enhanced Templates
Convert discoveries to templates for math-animator:

```python
# For each high-value pattern
for pattern_name, pattern in searcher.pattern_library.items():
    if pattern["code_template"]:
        # Add to math-animator templates
        template = {
            "name": pattern_name,
            "concept": pattern["concept"],
            "code": pattern["code_template"],
            "imports": pattern["required_imports"],
            "usage_notes": pattern["notes"]
        }
        
        # Save template
        save_to_dropbox(
            content=json.dumps(template, indent=2),
            file_path=f"MCP_Tools/manim_templates/{pattern_name}.json"
        )
```

## Step 7: Test and Validate
Test discovered patterns:

```python
# Create test animation from pattern
test_code = f'''
from manim import *
{pattern["code_template"]}

# Test the pattern
if __name__ == "__main__":
    scene = TestScene()
    scene.render()
'''

# Save and test locally
save_to_dropbox(
    content=test_code,
    file_path=f"MCP_Tools/manim_tests/test_{pattern_name}.py"
)
```
"""
    
    return workflow


if __name__ == "__main__":
    # Example usage
    print("=== Manim GitHub Discovery Tool ===\n")
    
    # Show available search areas
    searcher = ManimGitHubSearcher()
    areas = ["gyrovector", "stereographic", "topology", "examples"]
    
    print("Available search areas:")
    for area in areas:
        queries = searcher.get_search_queries(area)
        print(f"\n{area.upper()} ({len(queries)} queries):")
        for q in queries[:2]:
            print(f"  - {q}")
    
    # Generate MCP commands
    print("\n\n=== MCP Search Commands ===")
    commands = create_mcp_search_commands(["gyrovector", "stereographic"])
    for cmd in commands:
        print(cmd)
    
    # Show workflow
    print("\n\n=== Discovery Workflow ===")
    print(create_discovery_workflow())
