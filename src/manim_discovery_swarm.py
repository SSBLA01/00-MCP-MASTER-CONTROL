#!/usr/bin/env python3
"""
Manim Discovery Swarm - GitHub Pattern Mining Implementation
Discovers and catalogs Manim animation patterns from GitHub repositories
"""

import json
import re
import asyncio
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import hashlib

@dataclass
class ManimPattern:
    """Represents a discovered Manim animation pattern"""
    pattern_id: str
    source_url: str
    mathematical_concept: str
    code_snippet: str
    description: str
    tags: List[str]
    quality_score: float
    reusability: str
    dependencies: List[str]
    discovered_at: str
    
    def to_obsidian_note(self) -> str:
        """Convert pattern to Obsidian note format"""
        return f"""# Manim Pattern: {self.mathematical_concept}

## Overview
- **Pattern ID**: {self.pattern_id}
- **Source**: {self.source_url}
- **Quality Score**: {self.quality_score}/1.0
- **Reusability**: {self.reusability}
- **Discovered**: {self.discovered_at}

## Description
{self.description}

## Code
```python
{self.code_snippet}
```

## Dependencies
{', '.join(self.dependencies)}

## Tags
{' '.join([f'#{tag}' for tag in self.tags])}

## Related Patterns
- [[Manim Pattern Catalog]]
- [[{self.mathematical_concept} Visualizations]]
"""


class ManimDiscoverySwarm:
    """Swarm system for discovering Manim patterns across GitHub"""
    
    def __init__(self):
        self.discovered_patterns = []
        self.search_queries = self._initialize_search_queries()
        self.quality_thresholds = {
            "min_stars": 5,
            "min_documentation_ratio": 0.1,
            "min_code_quality": 0.6
        }
    
    def _initialize_search_queries(self) -> Dict[str, List[str]]:
        """Initialize search queries for different mathematical concepts"""
        return {
            "gyrovector": [
                "site:github.com manim gyrovector",
                "site:github.com manim gyroaddition visualization",
                "site:github.com manim poincare disk animation",
                "site:github.com manim hyperbolic geometry"
            ],
            "topology": [
                "site:github.com manim manifold visualization",
                "site:github.com manim topology animation",
                "site:github.com manim fiber bundle",
                "site:github.com manim homology"
            ],
            "geometry": [
                "site:github.com manim stereographic projection",
                "site:github.com manim mobius transformation",
                "site:github.com manim conformal mapping",
                "site:github.com manim differential geometry"
            ],
            "algebra": [
                "site:github.com manim group theory visualization",
                "site:github.com manim lie algebra",
                "site:github.com manim clifford algebra",
                "site:github.com manim representation theory"
            ]
        }
    
    async def discover_patterns(self, category: str = "all") -> List[ManimPattern]:
        """Main discovery process"""
        patterns = []
        
        # Select queries based on category
        if category == "all":
            queries = [q for queries in self.search_queries.values() for q in queries]
        else:
            queries = self.search_queries.get(category, [])
        
        print(f"Starting discovery for category: {category}")
        print(f"Total queries to process: {len(queries)}")
        
        for query in queries:
            print(f"\nSearching: {query}")
            results = await self._search_github(query)
            
            for result in results:
                pattern = await self._analyze_result(result)
                if pattern and self._meets_quality_threshold(pattern):
                    patterns.append(pattern)
                    print(f"✓ Discovered pattern: {pattern.mathematical_concept}")
        
        self.discovered_patterns.extend(patterns)
        return patterns
    
    async def _search_github(self, query: str) -> List[Dict]:
        """Simulate GitHub search (would use web_search in real implementation)"""
        # In actual implementation, this would use web_search tool
        # For demonstration, returning mock results
        mock_results = [
            {
                "url": f"https://github.com/example/manim-{query.split()[-1]}",
                "title": f"Manim {query.split()[-1].title()} Animations",
                "description": f"Beautiful animations of {query.split()[-1]}",
                "stars": 42
            }
        ]
        return mock_results
    
    async def _analyze_result(self, result: Dict) -> Optional[ManimPattern]:
        """Analyze a search result and extract pattern if valuable"""
        # In real implementation, would fetch actual code using web_fetch
        # For demonstration, creating example pattern
        
        concept = self._extract_mathematical_concept(result)
        if not concept:
            return None
        
        pattern_id = self._generate_pattern_id(result["url"], concept)
        
        # Mock code extraction (would actually fetch and parse)
        code_snippet = self._extract_code_example(concept)
        
        return ManimPattern(
            pattern_id=pattern_id,
            source_url=result["url"],
            mathematical_concept=concept,
            code_snippet=code_snippet,
            description=result.get("description", ""),
            tags=self._extract_tags(concept, code_snippet),
            quality_score=self._calculate_quality_score(result, code_snippet),
            reusability=self._assess_reusability(code_snippet),
            dependencies=self._extract_dependencies(code_snippet),
            discovered_at=datetime.now().isoformat()
        )
    
    def _extract_mathematical_concept(self, result: Dict) -> Optional[str]:
        """Extract the mathematical concept from search result"""
        title = result.get("title", "").lower()
        concepts = {
            "gyrovector": "Gyrovector Operations",
            "stereographic": "Stereographic Projection",
            "mobius": "Möbius Transformation",
            "manifold": "Manifold Visualization",
            "topology": "Topological Structures",
            "hyperbolic": "Hyperbolic Geometry",
            "clifford": "Clifford Algebra",
            "lie": "Lie Groups and Algebras"
        }
        
        for keyword, concept in concepts.items():
            if keyword in title:
                return concept
        return None
    
    def _generate_pattern_id(self, url: str, concept: str) -> str:
        """Generate unique pattern ID"""
        hash_input = f"{url}_{concept}_{datetime.now().date()}"
        return hashlib.md5(hash_input.encode()).hexdigest()[:8]
    
    def _extract_code_example(self, concept: str) -> str:
        """Extract relevant code example (mock implementation)"""
        examples = {
            "Gyrovector Operations": """
class GyrovectorAnimation(Scene):
    def construct(self):
        # Poincaré disk model
        disk = Circle(radius=2, color=WHITE)
        
        # Gyrovector addition
        u = np.array([0.3, 0.4, 0])
        v = np.array([0.1, 0.2, 0])
        
        # Einstein velocity addition formula
        w = self.einstein_add(u, v)
        
        # Visualize vectors
        u_arrow = Arrow(ORIGIN, u*2, color=BLUE)
        v_arrow = Arrow(ORIGIN, v*2, color=GREEN)
        w_arrow = Arrow(ORIGIN, w*2, color=RED)
        
        self.play(Create(disk))
        self.play(Create(u_arrow), Create(v_arrow))
        self.play(Transform(VGroup(u_arrow, v_arrow), w_arrow))
    
    def einstein_add(self, u, v):
        c = 1  # Speed of light normalized
        u_dot_v = np.dot(u, v)
        gamma_u = 1 / np.sqrt(1 - np.dot(u, u)/c**2)
        
        numerator = u + v/gamma_u + u_dot_v * u / (c**2 * (1 + gamma_u))
        denominator = 1 + u_dot_v / c**2
        
        return numerator / denominator
""",
            "Stereographic Projection": """
class StereographicProjection(ThreeDScene):
    def construct(self):
        # Create sphere
        sphere = Sphere(radius=2, resolution=(30, 30))
        sphere.set_color(BLUE_E)
        
        # Projection plane
        plane = Square(side_length=6).rotate(PI/2, RIGHT)
        plane.shift(3*DOWN)
        
        # North pole
        north_pole = Dot3D(point=np.array([0, 0, 2]), color=RED)
        
        # Stereographic projection function
        def project_point(p):
            x, y, z = p
            if z >= 1.99:  # Near north pole
                return np.array([0, 0, -3])
            factor = 1 / (1 - z/2)
            return np.array([factor * x, factor * y, -3])
        
        # Animate projection
        self.play(Create(sphere), Create(plane), Create(north_pole))
        
        # Project sample points
        sample_points = sphere.get_all_points()[::50]
        projections = VGroup(*[
            Line3D(north_pole.get_center(), project_point(p), color=YELLOW)
            for p in sample_points
        ])
        
        self.play(Create(projections), run_time=3)
"""
        }
        return examples.get(concept, "# No example available")
    
    def _extract_tags(self, concept: str, code: str) -> List[str]:
        """Extract relevant tags"""
        tags = ["manim", "animation", "mathematics"]
        
        # Add concept-specific tags
        concept_tags = {
            "Gyrovector": ["gyrovector", "hyperbolic", "poincare"],
            "Stereographic": ["projection", "topology", "manifold"],
            "Möbius": ["transformation", "complex", "conformal"]
        }
        
        for key, value in concept_tags.items():
            if key in concept:
                tags.extend(value)
        
        # Add technique tags based on code
        if "ThreeDScene" in code:
            tags.append("3d")
        if "Transform" in code:
            tags.append("transformation")
        if "VGroup" in code:
            tags.append("grouping")
        
        return list(set(tags))
    
    def _calculate_quality_score(self, result: Dict, code: str) -> float:
        """Calculate quality score based on various factors"""
        score = 0.5  # Base score
        
        # Repository popularity
        stars = result.get("stars", 0)
        if stars > 100:
            score += 0.2
        elif stars > 50:
            score += 0.1
        elif stars > 10:
            score += 0.05
        
        # Code quality indicators
        if "def " in code and "class " in code:
            score += 0.1  # Well-structured
        if code.count("\n") > 20:
            score += 0.1  # Substantial example
        if "#" in code or '"""' in code:
            score += 0.1  # Has comments/documentation
        
        return min(score, 1.0)
    
    def _assess_reusability(self, code: str) -> str:
        """Assess how reusable the pattern is"""
        if "def " in code or "class " in code:
            if code.count("def ") > 2:
                return "high"
            return "medium"
        return "low"
    
    def _extract_dependencies(self, code: str) -> List[str]:
        """Extract required dependencies from code"""
        dependencies = ["manim>=0.17.0"]
        
        imports = re.findall(r'from (\w+) import|import (\w+)', code)
        for imp in imports:
            dep = imp[0] or imp[1]
            if dep not in ["manim", "math", "os", "sys"]:
                dependencies.append(dep)
        
        return list(set(dependencies))
    
    def _meets_quality_threshold(self, pattern: ManimPattern) -> bool:
        """Check if pattern meets quality thresholds"""
        return pattern.quality_score >= self.quality_thresholds["min_code_quality"]
    
    def generate_catalog(self) -> Dict[str, List[ManimPattern]]:
        """Generate categorized catalog of discovered patterns"""
        catalog = {}
        
        for pattern in self.discovered_patterns:
            # Categorize by mathematical concept
            category = pattern.mathematical_concept.split()[0]
            if category not in catalog:
                catalog[category] = []
            catalog[category].append(pattern)
        
        return catalog
    
    def export_to_obsidian(self, vault_path: str = "Manim_Patterns"):
        """Export discovered patterns to Obsidian vault structure"""
        catalog = self.generate_catalog()
        
        # Create catalog index
        index_content = "# Manim Pattern Catalog\n\n"
        index_content += f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        index_content += f"Total patterns discovered: {len(self.discovered_patterns)}\n\n"
        
        for category, patterns in catalog.items():
            index_content += f"\n## {category}\n"
            for pattern in patterns:
                index_content += f"- [[{pattern.pattern_id}]] - {pattern.mathematical_concept}\n"
        
        print("\n=== Obsidian Export ===")
        print(index_content)
        
        # Export individual patterns
        for pattern in self.discovered_patterns:
            print(f"\n--- Pattern: {pattern.pattern_id} ---")
            print(pattern.to_obsidian_note())
    
    def generate_enhanced_templates(self) -> Dict[str, str]:
        """Generate enhanced templates for math-animator agent"""
        templates = {}
        
        for pattern in self.discovered_patterns:
            if pattern.reusability == "high":
                template_name = pattern.mathematical_concept.lower().replace(" ", "_")
                templates[template_name] = {
                    "description": pattern.description,
                    "code": pattern.code_snippet,
                    "tags": pattern.tags,
                    "quality": pattern.quality_score
                }
        
        return templates


async def run_discovery_swarm(categories: List[str] = None):
    """Run the Manim discovery swarm"""
    swarm = ManimDiscoverySwarm()
    
    if categories is None:
        categories = ["gyrovector", "topology", "geometry"]
    
    all_patterns = []
    
    for category in categories:
        print(f"\n{'='*60}")
        print(f"Discovering patterns for: {category}")
        print('='*60)
        
        patterns = await swarm.discover_patterns(category)
        all_patterns.extend(patterns)
        
        print(f"\nDiscovered {len(patterns)} patterns in {category}")
    
    # Generate outputs
    print(f"\n{'='*60}")
    print("Generating Outputs")
    print('='*60)
    
    # Export to Obsidian format
    swarm.export_to_obsidian()
    
    # Generate enhanced templates
    templates = swarm.generate_enhanced_templates()
    print(f"\nGenerated {len(templates)} reusable templates")
    
    # Create summary report
    report = {
        "discovery_date": datetime.now().isoformat(),
        "total_patterns": len(all_patterns),
        "categories_searched": categories,
        "high_quality_patterns": len([p for p in all_patterns if p.quality_score >= 0.8]),
        "reusable_templates": len(templates),
        "unique_concepts": len(set(p.mathematical_concept for p in all_patterns))
    }
    
    print("\n=== Discovery Report ===")
    print(json.dumps(report, indent=2))
    
    return swarm, report


# Integration with existing MCP tools
def create_mcp_integration_commands():
    """Generate MCP commands for integrating discovered patterns"""
    
    commands = [
        # Search for specific patterns
        'web_search("site:github.com manim gyrovector animation example")',
        
        # Fetch and analyze specific repositories  
        'web_fetch("https://github.com/3b1b/manim/tree/master/example_scenes")',
        
        # Store discoveries in Obsidian
        'ingest_to_obsidian(content=pattern.to_obsidian_note(), '
        'title=f"Manim Pattern - {pattern.mathematical_concept}", '
        'category="concepts", tags=["manim", "pattern", "animation"])',
        
        # Use Gemini to analyze code quality
        'gemini_analyze_code(code=pattern.code_snippet, '
        'analysis_type="quality")',
        
        # Create comprehensive documentation
        'create_notion_page(title="Manim Pattern Library", '
        'content=catalog_markdown)'
    ]
    
    return commands


if __name__ == "__main__":
    # Run discovery
    asyncio.run(run_discovery_swarm(["gyrovector", "geometry"]))
    
    # Show integration commands
    print("\n=== MCP Integration Commands ===")
    for cmd in create_mcp_integration_commands():
        print(f"- {cmd}")
