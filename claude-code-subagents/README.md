# Claude Code Sub-agents for Mathematical Research

## Overview
This directory contains specialized Claude Code sub-agents that complement the existing Claude Flow hive-mind system. These sub-agents provide focused expertise with isolated contexts, preventing conversation pollution while maintaining access to necessary tools.

## Sub-agents Created

### 1. gyrovector-geometry
Expert in gyrovector spaces, hyperbolic geometry, and Möbius transformations. Handles all gyrovector calculations, transformations between hyperbolic models, and gyrotrigonometry.

### 2. mobius-transformer
Specialized in Möbius transformations, conformal mappings, and complex analysis. Manages transformation groups, fixed point analysis, and connections to physics.

### 3. auxetic-materials
Expert in auxetic bistable metamaterials, negative Poisson's ratio structures, and advanced material design. Handles deformation analysis and optimization.

### 4. quantum-qbism
Specialist in Quantum Bayesianism, subjective probability in quantum contexts, and philosophical interpretations of quantum mechanics.

### 5. charm-cognition
Expert in the CHARM framework for cognition and manifolds, analyzing cognitive processes through manifold theory and consciousness studies.

### 6. research-orchestrator
Meta-coordinator that routes tasks between sub-agents and Claude Flow based on task characteristics, managing complex multi-domain research sessions.

## Installation

1. **Create directories**:
```bash
mkdir -p ~/.claude/agents
```

2. **Copy sub-agents**:
```bash
cp *.md ~/.claude/agents/
```

3. **Verify installation**:
Use `/agents` command in Claude Code to see all available sub-agents.

## Integration with Claude Flow

### Architecture Benefits
- **Claude Flow**: Handles parallel processing, heavy computation, batch operations
- **Sub-agents**: Provide domain expertise, context isolation, specialized analysis
- **Orchestrator**: Routes tasks optimally between systems

### Communication Flow
```
Claude Desktop → Research Orchestrator → Decision
                                          ├→ Sub-agent (for focused tasks)
                                          └→ Claude Flow (for distributed tasks)
```

## Usage Examples

### Direct Sub-agent Invocation
```
"Using the gyrovector-geometry agent, calculate the gyroaddition of [0.3,0.4,0] and [0.1,0.2,0.5]"
```

### Orchestrated Research
```
"Research the connection between gyrovector spaces and QBism interpretations"
→ Orchestrator routes to both gyrovector-geometry and quantum-qbism agents
```

### Hybrid Workflow
```
"Generate a comprehensive analysis of auxetic metamaterials in hyperbolic space"
→ Orchestrator uses auxetic-materials for analysis, Claude Flow for computations
```

## Security Considerations

Following Gemini's security recommendations:
1. Each sub-agent operates in isolated context
2. Tool access is explicitly defined per agent
3. Communication through secure channels (planned RabbitMQ implementation)
4. No direct database access from sub-agents

## Future Enhancements

1. **Phase 2**: RabbitMQ message queue integration
2. **Phase 3**: PostgreSQL migration from SQLite
3. **Phase 4**: Docker containerization for each sub-agent type
4. **Phase 5**: JWT authentication for inter-agent communication

## Tool Mapping

| Sub-agent | Primary Tools | Claude Flow Integration |
|-----------|--------------|------------------------|
| gyrovector-geometry | cf_gyro*, create_manim_animation | Full access to mathematical tools |
| mobius-transformer | cf_mobius_transform, cf_conformal_map | Computation delegation |
| auxetic-materials | validate_with_wolfram, gemini_analyze | Material simulation tools |
| quantum-qbism | discover_research, gemini_math_analysis | Research discovery |
| charm-cognition | cf_geodesic_compute, cf_curvature_tensor | Manifold computations |
| research-orchestrator | All coordination tools | Full system access |

## Best Practices

1. **Use sub-agents for**:
   - Domain-specific expertise
   - Preventing context pollution
   - Focused analysis tasks

2. **Use Claude Flow for**:
   - Parallel computations
   - Batch processing
   - Workflow automation

3. **Use orchestrator when**:
   - Task spans multiple domains
   - Optimal routing unclear
   - Complex research sessions

## Maintenance

- Sub-agents are version controlled in GitHub
- Regular updates based on research needs
- Performance monitoring through orchestrator
- Feedback incorporation from usage patterns