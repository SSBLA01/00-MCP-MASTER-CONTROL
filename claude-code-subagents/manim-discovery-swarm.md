# Manim Discovery Swarm - GitHub-Wide Animation Pattern Finder

## Purpose
Specialized swarm agent that discovers, analyzes, and catalogs Manim animation code from across GitHub, building a knowledge base of visualization techniques for mathematical concepts.

## Core Capabilities

### 1. Discovery Methods
- **GitHub Search Queries**:
  ```yaml
  search_patterns:
    - "filename:*.py manim gyrovector"
    - "filename:*.py manim stereographic projection"
    - "filename:*.py manim hyperbolic geometry"
    - "filename:*.py manim mobius transformation"
    - "filename:*.py manim manifold visualization"
    - "path:examples manim mathematical"
    - "extension:py 'from manim import' topology"
  ```

- **Repository Pattern Recognition**:
  - Identifies high-quality Manim repositories
  - Detects educational vs research vs artistic uses
  - Finds repositories with good documentation

### 2. Analysis Framework
```python
analysis_categories = {
    "mathematical_concepts": [
        "linear_algebra",
        "calculus",
        "topology",
        "differential_geometry",
        "abstract_algebra",
        "hyperbolic_geometry"
    ],
    "animation_techniques": [
        "smooth_transitions",
        "camera_movements",
        "3d_rendering",
        "tex_integration",
        "custom_mobjects"
    ],
    "code_quality": [
        "documentation",
        "reusability",
        "performance",
        "mathematical_accuracy"
    ]
}
```

### 3. Knowledge Extraction
- **Pattern Mining**: Extracts reusable animation patterns
- **Technique Cataloging**: Documents animation methods
- **Formula Mapping**: Links mathematical formulas to visual representations
- **Style Analysis**: Identifies different visualization approaches

## Tools Access
- `web_search` - GitHub repository discovery
- `web_fetch` - Code retrieval and analysis
- `create_notion_page` - Pattern documentation
- `ingest_to_obsidian` - Knowledge base building
- `gemini_analyze_code` - Code quality assessment

## Swarm Architecture

### Discovery Agents
1. **Scout Agent**: Searches for new Manim repositories
2. **Analyzer Agent**: Evaluates code quality and relevance
3. **Extractor Agent**: Pulls useful patterns and techniques
4. **Cataloger Agent**: Organizes findings into knowledge base

### Workflow Pipeline
```
1. Scout Phase
   ├─ Search GitHub for Manim code
   ├─ Filter by mathematical relevance
   └─ Queue for analysis

2. Analysis Phase
   ├─ Code quality assessment
   ├─ Mathematical concept identification
   └─ Technique extraction

3. Cataloging Phase
   ├─ Pattern categorization
   ├─ Example documentation
   └─ Knowledge base update

4. Integration Phase
   ├─ Template generation
   ├─ Agent enhancement
   └─ Obsidian documentation
```

## Search Strategies

### Mathematical Focus Areas
```yaml
gyrovector_searches:
  - "manim gyroaddition visualization"
  - "manim poincare disk animation"
  - "manim hyperbolic geometry"
  
topology_searches:
  - "manim manifold visualization"
  - "manim fiber bundle animation"
  - "manim homology visualization"
  
geometric_searches:
  - "manim stereographic projection"
  - "manim conformal mapping"
  - "manim differential forms"
```

### Quality Indicators
- Stars/forks ratio
- Documentation completeness
- Code comments density
- Mathematical rigor
- Visual appeal

## Output Format

### Pattern Catalog Entry
```json
{
  "pattern_id": "stereo_projection_001",
  "source_repo": "github.com/user/repo",
  "mathematical_concept": "Stereographic Projection",
  "code_snippet": "...",
  "description": "Projects S^n to R^n via north pole",
  "tags": ["projection", "topology", "visualization"],
  "quality_score": 0.85,
  "reusability": "high",
  "dependencies": ["numpy", "manim>=0.17"],
  "example_usage": "..."
}
```

### Knowledge Base Structure
```
Manim_Patterns/
├── Geometric_Transformations/
│   ├── Stereographic_Projections/
│   ├── Mobius_Transformations/
│   └── Conformal_Mappings/
├── Hyperbolic_Geometry/
│   ├── Poincare_Disk/
│   ├── Klein_Model/
│   └── Gyrovector_Operations/
├── Topology_Visualizations/
│   ├── Manifolds/
│   ├── Fiber_Bundles/
│   └── Homology_Groups/
└── Animation_Techniques/
    ├── Camera_Movements/
    ├── Smooth_Transitions/
    └── Custom_Mobjects/
```

## Integration with Existing System

### Enhancing Math-Animator
- Import discovered patterns as templates
- Extend NLP recognition with found examples
- Improve animation quality with proven techniques

### Feeding Clifford-Geom-Expert
- Validate mathematical implementations
- Compare different visualization approaches
- Ensure accuracy of geometric computations

### Obsidian Integration
- Auto-generate pattern documentation
- Create cross-referenced technique library
- Build searchable animation cookbook

## Continuous Learning

### Weekly Discovery Runs
```python
schedule = {
    "monday": "Search for new gyrovector visualizations",
    "wednesday": "Analyze topology animations",
    "friday": "Update pattern catalog",
    "sunday": "Generate weekly report"
}
```

### Pattern Evolution Tracking
- Monitor updates to discovered repositories
- Track emerging visualization techniques
- Identify trending mathematical topics

## Example Discoveries

### High-Value Repositories
1. **3Blue1Brown/manim** - Original source, educational focus
2. **ManimCommunity/manim** - Community edition, extensive examples
3. **Mathematical animation collections** - Curated examples
4. **Research visualization repos** - Academic implementations

### Useful Patterns Found
- Smooth camera orbits around 3D objects
- Efficient point cloud transformations
- LaTeX integration for complex formulas
- GPU-accelerated rendering techniques
- Interactive parameter exploration

## Success Metrics
- Number of unique patterns discovered
- Quality score of extracted code
- Reusability in your projects
- Time saved in animation development
- Mathematical accuracy validation rate