# Claude Flow Integration Guide

**Version**: v2.0.0-alpha.53  
**Phase**: 2 (Active)  
**Status**: ✅ Operational  
**Integration Date**: July 14, 2025

## Overview

Claude Flow brings advanced AI orchestration to Dobbs-MCP through a hive-mind swarm intelligence model. This integration adds 87 specialized tools that work in concert with the existing 43+ Dobbs-MCP tools, creating a powerful 130+ tool ecosystem for mathematical research and knowledge management.

## Architecture

### Hive-Mind Swarm Model

```
┌─────────────────────────────────────────┐
│            Queen Agent                  │
│    (Task Distribution & Aggregation)    │
└────────────────┬───────────────────────┘
                 │
     ┌───────────┴───────────┐
     │                       │
┌────▼────┐  ┌────────┐  ┌──▼─────┐  ┌────────┐
│Worker 1 │  │Worker 2│  │Worker 3│  │Worker 4│
│(Compute)│  │(Analyze)│  │(Memory)│  │(I/O)   │
└─────────┘  └────────┘  └────────┘  └────────┘
     │            │           │            │
     └────────────┴───────────┴────────────┘
                       │
              ┌───────▼────────┐
              │ Shared Memory  │
              │(.swarm/memory.db)│
              └────────────────┘
```

### Component Breakdown

1. **Queen Agent**
   - Receives high-level tasks from MCP
   - Decomposes into subtasks
   - Distributes to workers
   - Aggregates results
   - Handles error recovery

2. **Worker Agents**
   - **Worker 1 (Compute)**: Mathematical calculations
   - **Worker 2 (Analyze)**: Pattern recognition
   - **Worker 3 (Memory)**: Knowledge base operations
   - **Worker 4 (I/O)**: File and API operations

3. **Shared Memory (SQLite)**
   - Mathematical formulas
   - Computation history
   - Workflow definitions
   - Performance metrics

## Installation & Setup

### Prerequisites
```bash
# Ensure Dobbs-MCP is installed and working
cd /path/to/00-MCP-MASTER-CONTROL
source venv/bin/activate

# Install Claude Flow dependencies
npm install -g claude-flow@alpha
```

### Configuration
```bash
# Set environment variables
export CLAUDE_FLOW_PATH="/Users/scottbroock/Dropbox/MathematicalResearch/claude-flow-integration"
export CLAUDE_FLOW_MEMORY_DB="$CLAUDE_FLOW_PATH/.swarm/memory.db"
export CLAUDE_FLOW_WORKERS=4
```

### Integration with Dobbs-MCP
The integration is automatic through the unified server. Claude Flow tools are registered alongside native tools:

```python
# src/servers/dobbs_unified.py
ALL_TOOLS = [
    # Native Dobbs-MCP tools (43+)
    *FILE_OPERATION_TOOLS,
    *GITHUB_OPERATION_TOOLS,
    # ... other native tools ...
    
    # Claude Flow tools (87)
    *CLAUDE_FLOW_TOOLS  # Automatically loaded
]
```

## Tool Categories

### 1. Hive-Mind Coordination (12 tools)
- `cf_queen_delegate` - Delegate task to swarm
- `cf_worker_status` - Check worker availability
- `cf_swarm_execute` - Execute swarm workflow
- `cf_memory_sync` - Synchronize shared memory
- `cf_error_recovery` - Handle worker failures
- `cf_load_balance` - Distribute workload
- `cf_result_aggregate` - Combine worker outputs
- `cf_swarm_monitor` - Real-time monitoring
- `cf_worker_assign` - Manual task assignment
- `cf_queue_status` - Check task queue
- `cf_priority_set` - Set task priorities
- `cf_swarm_reset` - Reset swarm state

### 2. Mathematical Computation (15 tools)
- `cf_gyroaddition` - Möbius addition in hyperbolic space
- `cf_gyroscalar` - Scalar multiplication
- `cf_gyrodistance` - Hyperbolic distance
- `cf_gyroparallel` - Parallel transport
- `cf_gyrotrigonometry` - Trigonometric functions
- `cf_gyrovector_field` - Vector field operations
- `cf_poincare_disk` - Poincaré disk calculations
- `cf_klein_model` - Klein model transformations
- `cf_hyperboloid_model` - Hyperboloid computations
- `cf_stereographic` - Stereographic projections
- `cf_conformal_map` - Conformal mappings
- `cf_mobius_transform` - Möbius transformations
- `cf_hyperbolic_area` - Area calculations
- `cf_geodesic_compute` - Geodesic paths
- `cf_curvature_tensor` - Curvature computations

### 3. Enhanced GitHub Operations (6 modes)
- `cf_gh_coordinator` - Multi-repo orchestration
- `cf_pr_manager` - Advanced PR workflows
- `cf_repo_architect` - Repository structure design
- `cf_code_reviewer` - AI-powered code review
- `cf_branch_strategist` - Branch management
- `cf_release_automator` - Release pipeline

### 4. Memory & Knowledge Base (10 tools)
- `cf_memory_store` - Store knowledge
- `cf_memory_query` - Query knowledge base
- `cf_memory_search` - Semantic search
- `cf_memory_index` - Build indexes
- `cf_memory_export` - Export knowledge
- `cf_memory_import` - Import knowledge
- `cf_memory_backup` - Backup database
- `cf_memory_analyze` - Analyze patterns
- `cf_memory_visualize` - Visualize connections
- `cf_memory_prune` - Clean old data

### 5. Workflow Automation (8 tools)
- `cf_workflow_create` - Design workflows
- `cf_workflow_execute` - Run workflows
- `cf_workflow_schedule` - Schedule execution
- `cf_workflow_monitor` - Monitor progress
- `cf_workflow_abort` - Cancel workflows
- `cf_workflow_fork` - Create variants
- `cf_workflow_merge` - Combine workflows
- `cf_workflow_optimize` - Performance tuning

### 6. Neural Acceleration (6 tools) [Future]
- `cf_wasm_compile` - Compile to WASM
- `cf_simd_optimize` - SIMD optimization
- `cf_gpu_offload` - GPU acceleration
- `cf_parallel_map` - Parallel mapping
- `cf_tensor_ops` - Tensor operations
- `cf_neural_cache` - Neural caching

### 7. Integration Tools (30+ tools)
- Obsidian tag processors
- Notion sync enhancers
- Dropbox batch operations
- Manim workflow builders
- Wolfram validation pipelines
- Plus many more...

## Workflows

### Pre-configured Workflows

#### 1. Gyrovector-Sequential
```json
{
  "name": "Gyrovector-Sequential",
  "description": "Step-by-step gyrovector operations",
  "steps": [
    {"tool": "cf_memory_query", "params": {"concept": "gyroaddition"}},
    {"tool": "cf_gyroaddition", "params": {"vectors": "$input"}},
    {"tool": "cf_gyrodistance", "params": {"result": "$previous"}},
    {"tool": "cf_memory_store", "params": {"computation": "$all"}}
  ]
}
```

#### 2. Gyrovector-Parallel
```json
{
  "name": "Gyrovector-Parallel",
  "description": "Batch gyrovector processing",
  "mode": "parallel",
  "workers": 4,
  "tasks": [
    {"worker": 1, "tool": "cf_gyroaddition", "batch": true},
    {"worker": 2, "tool": "cf_gyroscalar", "batch": true},
    {"worker": 3, "tool": "cf_gyrodistance", "batch": true},
    {"worker": 4, "tool": "cf_memory_store", "batch": true}
  ]
}
```

#### 3. Mathematical-Analysis
```json
{
  "name": "Mathematical-Analysis",
  "description": "Deep mathematical structure analysis",
  "phases": [
    {
      "name": "Discovery",
      "tools": ["discover_research", "cf_memory_search"]
    },
    {
      "name": "Computation",
      "tools": ["cf_swarm_execute", "validate_with_wolfram"]
    },
    {
      "name": "Visualization",
      "tools": ["create_manim_animation", "cf_workflow_monitor"]
    },
    {
      "name": "Documentation",
      "tools": ["ingest_to_obsidian", "cf_memory_index"]
    }
  ]
}
```

## Usage Examples

### Basic Mathematical Operation
```bash
# Direct computation
npx claude-flow@alpha compute gyroaddition '[0.3,0.4,0]' '[0.1,0.2,0.5]'

# Using the wrapper script
./gyrovector-compute.sh compute gyroaddition '[0.3,0.4,0]' '[0.1,0.2,0.5]'
```

### Memory Operations
```bash
# Search mathematical concepts
npx claude-flow@alpha memory search 'gyrovector'

# List all stored formulas
npx claude-flow@alpha memory list --type=formula

# Export knowledge base
npx claude-flow@alpha memory export --format=json > knowledge.json
```

### Workflow Execution
```bash
# Execute predefined workflow
npx claude-flow@alpha workflow execute "Gyrovector-Sequential" \
  --input='{"vectors": [[0.1,0.2,0.3], [0.4,0.5,0.6]]}'

# Create custom workflow
npx claude-flow@alpha workflow create my-workflow.json

# Schedule workflow
npx claude-flow@alpha workflow schedule "Mathematical-Analysis" \
  --cron="0 9 * * *" --topic="Hyperbolic Geometry"
```

### Obsidian Integration
```python
# Process Obsidian note with Claude Flow
python3 obsidian-integration.py my_research_note.md

# Batch process folder
python3 obsidian-integration.py --folder="/path/to/notes" --recursive
```

### Using Obsidian Tags
Add these tags to your notes:

```markdown
# Gyrovector Research #cf/compute

Calculate the gyroaddition of vectors a=[0.3,0.4,0] and b=[0.1,0.2,0.5]

#cf/analyze

---

# Results #cf/visualize

The computation shows interesting properties...

#cf/explore
```

## Advanced Features

### 1. Custom Worker Configuration
```python
# claude_flow_config.py
WORKER_CONFIG = {
    "worker_1": {
        "type": "compute",
        "memory_limit": "2GB",
        "timeout": 300,
        "capabilities": ["math", "tensor", "symbolic"]
    },
    "worker_2": {
        "type": "analyze",
        "memory_limit": "1GB",
        "timeout": 600,
        "capabilities": ["pattern", "ml", "statistics"]
    }
}
```

### 2. Memory Schema Extension
```sql
-- Add custom tables to .swarm/memory.db
CREATE TABLE IF NOT EXISTS research_sessions (
    id INTEGER PRIMARY KEY,
    session_id TEXT UNIQUE,
    topic TEXT,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    artifacts JSON
);

CREATE INDEX idx_topic ON research_sessions(topic);
```

### 3. Workflow Composition
```javascript
// Compose workflows dynamically
const workflow = new WorkflowBuilder()
  .addPhase("research", ["discover_research", "cf_memory_search"])
  .addPhase("compute", ["cf_swarm_execute"], { parallel: true })
  .addPhase("validate", ["validate_with_wolfram", "cf_memory_store"])
  .onError("cf_error_recovery")
  .build();
```

## Performance Optimization

### 1. Batch Processing
```bash
# Process multiple computations in parallel
echo '[
  {"op": "gyroaddition", "a": [0.1,0.2,0.3], "b": [0.4,0.5,0.6]},
  {"op": "gyroscalar", "r": 2.0, "v": [0.1,0.2,0.3]},
  {"op": "gyrodistance", "u": [0.1,0.2,0.3], "v": [0.4,0.5,0.6]}
]' | npx claude-flow@alpha batch process
```

### 2. Memory Optimization
```bash
# Preload frequently used formulas
npx claude-flow@alpha memory preload --concepts="gyrovector,hyperbolic"

# Enable memory compression
export CLAUDE_FLOW_MEMORY_COMPRESS=true
```

### 3. Worker Tuning
```bash
# Adjust worker count based on workload
export CLAUDE_FLOW_WORKERS=8  # For heavy computation

# Set worker affinity
export CLAUDE_FLOW_WORKER_AFFINITY="0:compute,1:compute,2:analyze,3:memory"
```

## Troubleshooting

### Common Issues

1. **Workers not responding**
```bash
# Check worker status
npx claude-flow@alpha worker status

# Restart workers
npx claude-flow@alpha swarm reset
```

2. **Memory database locked**
```bash
# Unlock database
rm $CLAUDE_FLOW_PATH/.swarm/memory.db-wal
rm $CLAUDE_FLOW_PATH/.swarm/memory.db-shm

# Rebuild indexes
npx claude-flow@alpha memory reindex
```

3. **Workflow timeout**
```bash
# Increase timeout
export CLAUDE_FLOW_WORKFLOW_TIMEOUT=3600  # 1 hour

# Check workflow logs
tail -f $CLAUDE_FLOW_PATH/logs/workflow.log
```

### Debug Mode
```bash
# Enable debug logging
export CLAUDE_FLOW_DEBUG=true
export CLAUDE_FLOW_LOG_LEVEL=debug

# Trace specific workflow
npx claude-flow@alpha workflow execute "Gyrovector-Sequential" --trace
```

## Best Practices

1. **Use Appropriate Workflows**
   - Sequential for dependent operations
   - Parallel for independent computations
   - Analysis for exploration tasks

2. **Memory Management**
   - Regular backups: `npx claude-flow@alpha memory backup`
   - Prune old data: `npx claude-flow@alpha memory prune --days=30`
   - Monitor size: `du -h $CLAUDE_FLOW_PATH/.swarm/memory.db`

3. **Error Handling**
   - Always specify error recovery in workflows
   - Use timeouts for long-running operations
   - Monitor worker health regularly

4. **Performance**
   - Batch similar operations
   - Use parallel workflows when possible
   - Preload frequently used data

## Integration Checklist

- [x] Claude Flow installed globally
- [x] Environment variables configured
- [x] Memory database initialized
- [x] Obsidian tags configured
- [x] Workflows tested
- [x] Error recovery verified
- [x] Performance benchmarked
- [x] Documentation complete

## Future Enhancements

### Phase 3 (Planned)
- WASM SIMD acceleration
- GPU offloading for tensor operations
- Distributed swarm across multiple machines
- Real-time collaboration features

### Phase 4 (Conceptual)
- Quantum computing integration
- Neural network training
- Automated theorem proving
- Cross-language support

---

**Support**: For issues specific to Claude Flow integration, check the logs at `$CLAUDE_FLOW_PATH/logs/` or refer to the main Dobbs-MCP documentation.