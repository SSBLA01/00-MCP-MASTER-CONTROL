# Claude Code Sub-agents for Mathematical Research

## Overview
This directory contains specialized Claude Code sub-agents that complement the existing Claude Flow hive-mind system. These sub-agents provide focused expertise with isolated contexts, preventing conversation pollution while maintaining access to necessary tools.

## Enhanced Sub-agents (Updated 2025-07-30)

### 1. clifford-geom-expert ✨ (Enhanced)
**Advanced Geometric Computation Specialist** - Expert in Clifford algebras, gyrovector spaces, hyperbolic geometry, and orbifolds. Features:
- **Multi-Model Support**: Poincaré, Klein, Einstein, and Möbius gyrovector spaces
- **Symbolic Computation**: SymPy integration for exact calculations
- **Validation Framework**: Internal consistency checks and Wolfram Alpha verification
- **Advanced Algorithms**: Fast gyroaddition, 8th-order geodesic solver, orbifold classifier
- **Performance Modes**: Exact (symbolic), high-precision, and GPU-optimized modes

### 2. math-animator ✨ (Enhanced)
**Manim & Visual Explanation Specialist** - Creates mathematically accurate animations from natural language descriptions. Features:
- **NLP Pipeline**: Advanced plain English to animation translation
- **Template System**: Pre-built templates for common mathematical animations
- **Validation Layer**: Mathematical accuracy verification before rendering
- **Scene Graph Management**: Efficient handling of complex 3D animations
- **Quality Options**: Preview, standard, and 4K rendering modes

### 3. manim-swarm 🐝 (New)
**GitHub Pattern Discovery Swarm** - Automated discovery system that searches GitHub for Manim animation patterns and examples. Features:
- **Multi-Agent Architecture**: Scout, Analyzer, Extractor, and Cataloger agents
- **Pattern Mining**: Discovers reusable animation code across repositories
- **Quality Assessment**: Evaluates code quality and mathematical accuracy
- **Knowledge Integration**: Automatically enhances other agents with discoveries
- **Continuous Learning**: Weekly discovery runs for emerging patterns

### 4. mobius-transformer
Specialized in Möbius transformations, conformal mappings, and complex analysis. Manages transformation groups, fixed point analysis, and connections to physics.

### 5. auxetic-materials
Expert in auxetic bistable metamaterials, negative Poisson's ratio structures, and advanced material design. Handles deformation analysis and optimization.

### 6. quantum-qbism
Specialist in Quantum Bayesianism, subjective probability in quantum contexts, and philosophical interpretations of quantum mechanics.

### 7. charm-cognition
Expert in the CHARM framework for cognition and manifolds, analyzing cognitive processes through manifold theory and consciousness studies.

### 8. research-orchestrator
Meta-coordinator that routes tasks between sub-agents and Claude Flow based on task characteristics, managing complex multi-domain research sessions.

## Manim Swarm System

### Quick Deployment
```bash
# Run swarm for specific concept
python scripts/run_manim_swarm.py --concept gyrovector

# Batch discovery
python scripts/run_manim_swarm.py --batch

# Full scan across all categories
python scripts/run_manim_swarm.py --full-scan
```

### Integration with MCP
```python
# Import manim swarm
from src.manim_swarm import ManimSwarm

# Deploy swarm
swarm = ManimSwarm()
patterns = await swarm.deploy_swarm("hyperbolic geometry")

# Enhance agents with discoveries
swarm.enhance_agents(patterns)
```

## NLP to Manim Pipeline

### New Module: `nlp_manim_pipeline.py`
Complete natural language processing pipeline for animation generation:
- **Parser**: Extracts objects, transformations, and parameters from descriptions
- **Code Generator**: Creates Manim code with appropriate templates
- **Validator**: Ensures mathematical accuracy and numerical stability

### Example Usage
```python
from src.nlp_manim_pipeline import process_animation_request

result = process_animation_request(
    "Create an animation showing a stereo projected S³ sphere on a polar plane, then rotate the plane relative to the pole"
)

if result["success"]:
    print(result["manim_code"])  # Ready-to-run Manim code
```

## Installation

1. **Create directories**:
```bash
mkdir -p ~/.claude/agents
```

2. **Copy sub-agents**:
```bash
cp *.md ~/.claude/agents/
```

3. **Install NLP dependencies**:
```bash
pip install spacy sympy
python -m spacy download en_core_web_sm
```

4. **Verify installation**:
Use `/agents` command in Claude Code to see all available sub-agents.

## Enhanced Integration with Claude Flow

### Architecture Benefits
- **Claude Flow**: Handles parallel processing, heavy computation, batch operations
- **Sub-agents**: Provide domain expertise, context isolation, specialized analysis
- **Orchestrator**: Routes tasks optimally between systems
- **NLP Pipeline**: Seamless plain English to animation workflow
- **Manim Swarm**: Continuous pattern discovery and integration

### Communication Flow
```
User Request (Plain English)
        ↓
NLP Pipeline Parser
        ↓
Research Orchestrator → Decision
                        ├→ math-animator (for visualizations)
                        ├→ clifford-geom-expert (for computations)
                        ├→ manim-swarm (for pattern discovery)
                        └→ Claude Flow (for distributed tasks)
```

## Usage Examples

### Enhanced Animation Generation
```
"Visualize the parallel transport of a gyrovector along a geodesic in the Poincaré disk model with 5 second duration in 4K quality"
→ NLP pipeline parses request
→ clifford-geom-expert computes geodesic
→ math-animator generates 4K animation
```

### Pattern Discovery Workflow
```
"Find examples of hyperbolic geometry animations on GitHub"
→ manim-swarm deploys scout agents
→ Discovers and analyzes repositories
→ Extracts reusable patterns
→ Updates math-animator templates
```

### Complex Geometric Computation
```
"Calculate the orbifold structure of H²/(2,3,7) and visualize the fundamental domain"
→ clifford-geom-expert analyzes orbifold
→ Validates with Wolfram Alpha
→ math-animator creates visualization
```

## Enhanced Tool Mapping

| Sub-agent | Primary Tools | Claude Flow Integration | New Capabilities |
|-----------|--------------|------------------------|------------------|
| clifford-geom-expert | cf_gyro*, symbolic computation | Full mathematical toolkit | Multi-model support, orbifold analysis |
| math-animator | create_manim_animation, NLP pipeline | Animation generation | Plain English input, 4K rendering |
| manim-swarm | web_search, web_fetch, pattern extraction | Discovery automation | GitHub mining, pattern cataloging |
| mobius-transformer | cf_mobius_transform, cf_conformal_map | Computation delegation | - |
| auxetic-materials | validate_with_wolfram, gemini_analyze | Material simulation tools | - |
| quantum-qbism | discover_research, gemini_math_analysis | Research discovery | - |
| charm-cognition | cf_geodesic_compute, cf_curvature_tensor | Manifold computations | - |
| research-orchestrator | All coordination tools | Full system access | Enhanced routing logic |

## Best Practices

1. **Use enhanced agents for**:
   - Natural language animation requests
   - Complex geometric computations requiring validation
   - Multi-model mathematical operations
   - High-quality visualization generation

2. **Deploy manim-swarm for**:
   - Discovering new animation techniques
   - Building pattern libraries
   - Learning from community examples
   - Keeping up with Manim developments

3. **Leverage NLP pipeline for**:
   - Converting research descriptions to animations
   - Batch processing of visualization requests
   - Standardizing animation workflows

4. **Combine agents when**:
   - Computations need visualization
   - Multiple mathematical domains intersect
   - Research requires both analysis and presentation
   - Pattern discovery enhances current work

## Performance Considerations

- **clifford-geom-expert**: Use exact mode for proofs, optimized mode for animations
- **math-animator**: Preview mode for development, 4K for final output
- **manim-swarm**: Schedule weekly discovery runs, cache discovered patterns
- **NLP Pipeline**: Cache parsed requests for similar animations
- **Integration**: Batch similar operations for efficiency

## Maintenance

- Sub-agents are version controlled in GitHub
- Regular updates based on research needs
- Performance monitoring through orchestrator
- Feedback incorporation from usage patterns
- NLP model training based on successful parses
- Manim swarm continuous learning from GitHub ecosystem