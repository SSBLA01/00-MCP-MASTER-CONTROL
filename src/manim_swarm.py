#!/usr/bin/env python3
"""
Manim Swarm - GitHub Pattern Mining Implementation
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


class ManimSwarm:
    """The Manim Swarm system for discovering animation patterns across GitHub"""
    
    def __init__(self, name: str = "ManimSwarm"):
        self.name = name
        self.discovered_patterns = []
        self.search_queries = self._initialize_search_queries()
        self.quality_thresholds = {
            "min_stars": 5,
            "min_documentation_ratio": 0.1,
            "min_code_quality": 0.6
        }
        self.active_agents = {
            "scout": True,
            "analyzer": True,
            "extractor": True,
            "cataloger": True
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
            ],
            "calculus": [
                "site:github.com manim derivative visualization",
                "site:github.com manim integral animation",
                "site:github.com manim vector field",
                "site:github.com manim differential equation"
            ]
        }
    
    async def deploy_swarm(self, category: str = "all", max_patterns: int = 50) -> List[ManimPattern]:
        """Deploy the Manim Swarm to discover patterns"""
        patterns = []
        
        print(f"\n{'='*60}")
        print(f"{self.name} Deployment Started")
        print(f"Target: {category} | Max Patterns: {max_patterns}")
        print('='*60)
        
        # Select queries based on category
        if category == "all":
            queries = [q for queries in self.search_queries.values() for q in queries]
        else:
            queries = self.search_queries.get(category, [])
        
        # Scout Phase
        if self.active_agents["scout"]:
            print("\n[Scout Agent] Searching GitHub...")
            for query in queries[:10]:  # Limit queries
                print(f"  → {query}")
                results = await self._scout_search(query)
                
                # Analyzer Phase
                if self.active_agents["analyzer"]:
                    for result in results:
                        if await self._analyze_repository(result):
                            # Extractor Phase
                            if self.active_agents["extractor"]:
                                pattern = await self._extract_pattern(result)
                                if pattern and len(patterns) < max_patterns:
                                    patterns.append(pattern)
                                    print(f"  ✓ Extracted: {pattern.mathematical_concept}")
        
        # Cataloger Phase
        if self.active_agents["cataloger"] and patterns:
            print(f"\n[Cataloger Agent] Organizing {len(patterns)} patterns...")
            self.discovered_patterns.extend(patterns)
            await self._catalog_patterns(patterns)
        
        print(f"\n{'='*60}")
        print(f"Swarm Complete: {len(patterns)} patterns discovered")
        print('='*60)
        
        return patterns
    
    async def _scout_search(self, query: str) -> List[Dict]:
        """Scout agent: Search GitHub for repositories"""
        # In real implementation, this would use web_search
        # For demonstration, returning mock results
        mock_results = []
        
        if "gyrovector" in query:
            mock_results.append({
                "url": "https://github.com/example/manim-gyrovector",
                "title": "Gyrovector Animations in Manim",
                "description": "Beautiful visualizations of gyrovector operations",
                "stars": 42
            })
        elif "stereographic" in query:
            mock_results.append({
                "url": "https://github.com/example/manim-projections",
                "title": "Stereographic Projection Animations",
                "description": "S³ to R³ projections with Manim",
                "stars": 87
            })
        
        return mock_results
    
    async def _analyze_repository(self, repo: Dict) -> bool:
        """Analyzer agent: Evaluate repository quality"""
        # Check quality indicators
        stars = repo.get("stars", 0)
        has_description = bool(repo.get("description"))
        
        # Simple quality check
        quality_score = 0
        if stars >= self.quality_thresholds["min_stars"]:
            quality_score += 0.5
        if has_description:
            quality_score += 0.3
        if "visualization" in repo.get("description", "").lower():
            quality_score += 0.2
        
        return quality_score >= self.quality_thresholds["min_code_quality"]
    
    async def _extract_pattern(self, result: Dict) -> Optional[ManimPattern]:
        """Extractor agent: Extract reusable pattern from repository"""
        # Extract mathematical concept
        concept = self._identify_concept(result)
        if not concept:
            return None
        
        # Generate pattern ID
        pattern_id = f"manim_{concept.lower().replace(' ', '_')}_{hashlib.md5(result['url'].encode()).hexdigest()[:8]}"
        
        # Create example code based on concept
        code_snippet = self._generate_example_code(concept)
        
        return ManimPattern(
            pattern_id=pattern_id,
            source_url=result["url"],
            mathematical_concept=concept,
            code_snippet=code_snippet,
            description=result.get("description", ""),
            tags=self._extract_tags(concept, result),
            quality_score=self._calculate_quality_score(result),
            reusability=self._assess_reusability(code_snippet),
            dependencies=["manim>=0.17.0", "numpy"],
            discovered_at=datetime.now().isoformat()
        )
    
    def _identify_concept(self, result: Dict) -> Optional[str]:
        """Identify mathematical concept from repository"""
        title = result.get("title", "").lower()
        desc = result.get("description", "").lower()
        
        concepts = {
            "gyrovector": "Gyrovector Operations",
            "stereographic": "Stereographic Projection",
            "mobius": "Möbius Transformation",
            "manifold": "Manifold Visualization",
            "topology": "Topological Structures",
            "hyperbolic": "Hyperbolic Geometry",
            "clifford": "Clifford Algebra",
            "lie": "Lie Groups and Algebras",
            "derivative": "Calculus Visualization",
            "integral": "Integration Techniques"
        }
        
        for keyword, concept in concepts.items():
            if keyword in title or keyword in desc:
                return concept
        return None
    
    def _generate_example_code(self, concept: str) -> str:
        """Generate example code for concept"""
        examples = {
            "Gyrovector Operations": """
class GyroveorAnimation(Scene):
    def construct(self):
        # Poincaré disk setup
        disk = Circle(radius=2, color=WHITE)
        self.add(disk)
        
        # Gyrovectors
        u = np.array([0.3, 0.4, 0])
        v = np.array([0.1, 0.2, 0])
        
        # Visualize gyroaddition
        u_arrow = Arrow(ORIGIN, u*2, color=BLUE)
        v_arrow = Arrow(ORIGIN, v*2, color=GREEN)
        result = self.gyro_add(u, v)
        result_arrow = Arrow(ORIGIN, result*2, color=RED)
        
        self.play(Create(u_arrow), Create(v_arrow))
        self.play(Transform(VGroup(u_arrow, v_arrow), result_arrow))
    
    def gyro_add(self, u, v):
        # Einstein velocity addition
        gamma_u = 1 / np.sqrt(1 - np.dot(u, u))
        return (u + v/gamma_u) / (1 + np.dot(u, v))
""",
            "Stereographic Projection": """
class StereographicProjection(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=75*DEGREES, theta=-45*DEGREES)
        
        # Create S³ representation (as S²)
        sphere = Sphere(radius=2, resolution=(30, 30))
        sphere.set_color(BLUE_E)
        
        # Projection plane
        plane = Square(side_length=6).rotate(PI/2, RIGHT)
        plane.shift(3*DOWN)
        
        # Animate projection
        self.play(Create(sphere), Create(plane))
        
        # Project points
        def project(p):
            x, y, z = p
            return np.array([x/(1-z), y/(1-z), -3])
        
        # Show projection lines
        sample_points = sphere.get_all_points()[::100]
        for p in sample_points:
            proj_line = Line3D(p, project(p), color=YELLOW)
            self.play(Create(proj_line), run_time=0.1)
"""
        }
        return examples.get(concept, "# Example code for " + concept)
    
    def _extract_tags(self, concept: str, result: Dict) -> List[str]:
        """Extract relevant tags"""
        tags = ["manim", "animation", "mathematics"]
        
        # Add concept-based tags
        concept_words = concept.lower().split()
        tags.extend(concept_words)
        
        # Add technique tags from description
        desc = result.get("description", "").lower()
        if "3d" in desc or "three" in desc:
            tags.append("3d")
        if "interactive" in desc:
            tags.append("interactive")
        if "educational" in desc:
            tags.append("educational")
        
        return list(set(tags))
    
    def _calculate_quality_score(self, result: Dict) -> float:
        """Calculate quality score for pattern"""
        score = 0.5  # Base score
        
        # Repository metrics
        stars = result.get("stars", 0)
        if stars > 100:
            score += 0.3
        elif stars > 50:
            score += 0.2
        elif stars > 10:
            score += 0.1
        
        # Description quality
        desc = result.get("description", "")
        if len(desc) > 50:
            score += 0.1
        if "example" in desc.lower() or "tutorial" in desc.lower():
            score += 0.1
        
        return min(score, 1.0)
    
    def _assess_reusability(self, code: str) -> str:
        """Assess pattern reusability"""
        if "class" in code and "def" in code:
            if code.count("def") > 2:
                return "high"
            return "medium"
        return "low"
    
    async def _catalog_patterns(self, patterns: List[ManimPattern]) -> None:
        """Cataloger agent: Organize patterns into knowledge base"""
        catalog = {}
        
        # Categorize patterns
        for pattern in patterns:
            category = pattern.mathematical_concept.split()[0]
            if category not in catalog:
                catalog[category] = []
            catalog[category].append(pattern)
        
        # Generate catalog report
        print("\n[Catalog Summary]")
        for category, cat_patterns in catalog.items():
            print(f"  {category}: {len(cat_patterns)} patterns")
    
    def generate_swarm_report(self) -> Dict:
        """Generate comprehensive swarm activity report"""
        return {
            "swarm_name": self.name,
            "deployment_date": datetime.now().isoformat(),
            "total_patterns": len(self.discovered_patterns),
            "pattern_categories": self._get_category_distribution(),
            "quality_distribution": self._get_quality_distribution(),
            "top_concepts": self._get_top_concepts(),
            "active_agents": self.active_agents
        }
    
    def _get_category_distribution(self) -> Dict[str, int]:
        """Get distribution of patterns by category"""
        distribution = {}
        for pattern in self.discovered_patterns:
            category = pattern.mathematical_concept.split()[0]
            distribution[category] = distribution.get(category, 0) + 1
        return distribution
    
    def _get_quality_distribution(self) -> Dict[str, int]:
        """Get distribution of patterns by quality"""
        distribution = {"high": 0, "medium": 0, "low": 0}
        for pattern in self.discovered_patterns:
            if pattern.quality_score >= 0.8:
                distribution["high"] += 1
            elif pattern.quality_score >= 0.6:
                distribution["medium"] += 1
            else:
                distribution["low"] += 1
        return distribution
    
    def _get_top_concepts(self, limit: int = 5) -> List[str]:
        """Get most common mathematical concepts"""
        concept_counts = {}
        for pattern in self.discovered_patterns:
            concept = pattern.mathematical_concept
            concept_counts[concept] = concept_counts.get(concept, 0) + 1
        
        sorted_concepts = sorted(concept_counts.items(), key=lambda x: x[1], reverse=True)
        return [concept for concept, count in sorted_concepts[:limit]]
    
    def enhance_agents(self, patterns: List[ManimPattern]) -> Dict[str, int]:
        """Enhance math-animator and clifford-geom-expert with discovered patterns"""
        enhancements = {
            "math_animator_templates": 0,
            "geometry_validations": 0,
            "nlp_patterns": 0
        }
        
        for pattern in patterns:
            if pattern.reusability == "high":
                # Add to math-animator templates
                enhancements["math_animator_templates"] += 1
                
                # Add to NLP recognition
                if pattern.quality_score >= 0.8:
                    enhancements["nlp_patterns"] += 1
            
            # Validate geometric patterns
            if any(term in pattern.mathematical_concept.lower() 
                   for term in ["geometry", "projection", "transformation"]):
                enhancements["geometry_validations"] += 1
        
        return enhancements


# Utility functions for running the swarm
async def run_manim_swarm(concept: str = "all", deploy_full: bool = False):
    """Run the Manim Swarm with specified parameters"""
    swarm = ManimSwarm()
    
    if deploy_full:
        # Full deployment across all categories
        all_patterns = []
        for category in swarm.search_queries.keys():
            patterns = await swarm.deploy_swarm(category, max_patterns=10)
            all_patterns.extend(patterns)
        
        # Generate final report
        report = swarm.generate_swarm_report()
        print("\n" + "="*60)
        print("MANIM SWARM FINAL REPORT")
        print("="*60)
        print(json.dumps(report, indent=2))
        
        return all_patterns
    else:
        # Single concept deployment
        patterns = await swarm.deploy_swarm(concept, max_patterns=20)
        
        # Enhance agents
        enhancements = swarm.enhance_agents(patterns)
        print(f"\nAgent Enhancements: {enhancements}")
        
        return patterns


def create_mcp_commands(patterns: List[ManimPattern]) -> List[str]:
    """Generate MCP commands to integrate discovered patterns"""
    commands = []
    
    for pattern in patterns[:5]:  # Top 5 patterns
        # Fetch actual code
        commands.append(f'web_fetch("{pattern.source_url}")')
        
        # Analyze with Gemini
        commands.append(
            f'gemini_analyze_code(code=pattern_{pattern.pattern_id}, '
            f'analysis_type="quality")'
        )
        
        # Save to Obsidian
        commands.append(
            f'ingest_to_obsidian(content="""{pattern.to_obsidian_note()}""", '
            f'title="Manim Pattern - {pattern.mathematical_concept}", '
            f'category="concepts", tags={pattern.tags})'
        )
    
    return commands


if __name__ == "__main__":
    # Example usage
    print("MANIM SWARM - Pattern Discovery System")
    print("=====================================\n")
    
    # Run discovery for gyrovector patterns
    asyncio.run(run_manim_swarm("gyrovector"))
    
    # Show how to run full swarm
    print("\nTo run full swarm deployment:")
    print("asyncio.run(run_manim_swarm(deploy_full=True))")
