# Kimi K2 Integration Guide

## Overview

The Kimi K2 integration brings Moonshot AI's state-of-the-art 1 trillion parameter MoE model into the Dobbs-MCP ecosystem via Groq's ultra-fast inference infrastructure. This integration enhances the system's mathematical reasoning capabilities, particularly for gyrovector spaces, lattices, recursive harmonics, and orbifolds.

### Key Features

- **Lightning-Fast Inference**: 185 tokens/second via Groq API
- **Superior Mathematical Performance**: 97.4% accuracy on MATH-500 benchmark
- **Native MCP Support**: Built-in support for Model Context Protocol
- **Agentic Intelligence**: Designed for autonomous tool use and problem-solving
- **128K Context Window**: Handle complex mathematical proofs and large documents
- **Collaborative Integration**: Works seamlessly with Claude Flow hive-mind

## Installation

### 1. Prerequisites

- Groq API key (obtain from [Groq Cloud](https://console.groq.com))
- Python 3.8+
- Existing Dobbs-MCP installation

### 2. Setup Steps

```bash
# 1. Add Groq API key to your .env file
echo "GROQ_API_KEY=your_groq_api_key_here" >> .env

# 2. Copy the Kimi K2 integration module
cp kimi_k2_integration.py src/servers/

# 3. Update requirements.txt
echo "groq>=0.11.0" >> requirements.txt
echo "aiohttp>=3.9.0" >> requirements.txt

# 4. Install new dependencies
pip install -r requirements.txt

# 5. Update your dobbs_unified.py with the integration code
# (See dobbs_unified_update.py for specific changes)

# 6. Run tests to verify installation
python tests/test_kimi_k2_integration.py
```

### 3. Configuration

Add these environment variables to your `.env` file:

```env
# Required
GROQ_API_KEY=your_groq_api_key_here

# Optional (defaults shown)
KIMI_K2_MODEL=moonshotai/kimi-k2-instruct
KIMI_K2_TEMPERATURE=0.7
KIMI_K2_MAX_TOKENS=32768
KIMI_K2_CONTEXT_WINDOW=128000
KIMI_K2_DEFAULT_DOMAIN=gyrovector
KIMI_K2_ENABLE_VALIDATION=true
```

## Usage Examples

### Basic Mathematical Query

```python
# Using the MCP tool
result = await call_tool("kimi_k2_query", {
    "prompt": "Explain the relationship between gyrovector spaces and hyperbolic geometry"
})
```

### Solving Complex Problems

```python
# Solve a gyrovector problem with validation
result = await call_tool("kimi_k2_solve_problem", {
    "problem": "Given u = [0.3, 0.4, 0] and v = [0.1, 0.2, 0.5] in the Poincaré ball model, calculate u ⊕ v and verify the result satisfies ||u ⊕ v|| < 1",
    "domain": "gyrovector",
    "validate": true
})
```

### Generating Visualizations

```python
# Generate Manim code for a mathematical concept
result = await call_tool("kimi_k2_generate_visualization", {
    "concept": "gyrovector parallel transport on a geodesic",
    "animation_type": "transformation",
    "style": "3blue1brown"
})

# The generated code will be saved to your MANIM_OUTPUT_DIR
```

### Collaborative Reasoning with Claude Flow

```python
# Complex task using multiple agents
result = await call_tool("kimi_k2_collaborative_reasoning", {
    "task": "Prove that gyrovector addition is associative up to gyroautomorphism",
    "agents": ["kimi_k2", "claude_flow_queen", "wolfram_validator"],
    "workflow_type": "iterative"
})
```

## Mathematical Domains

Kimi K2 has been configured with specialized knowledge in these domains:

### 1. Gyrovector Spaces
- Gyroaddition: `u ⊕ v`
- Gyroscalar multiplication: `r ⊗ u`
- Gyroparallel transport
- Gyroderivatives and gyrointegration

### 2. Lattice Theory
- Lattice operations (meet, join)
- Sublattices and homomorphisms
- Modular and distributive lattices
- Applications to algebraic structures

### 3. Recursive Harmonics
- Fourier analysis on recursive structures
- Harmonic decomposition
- Spectral analysis
- Wavelet transforms

### 4. Orbifolds
- Quotient spaces by group actions
- Orbifold fundamental groups
- Geometric structures on orbifolds
- Applications to mathematical physics

## Integration Architecture

```
┌─────────────────────────────────────────────────┐
│                Claude Desktop                    │
├─────────────────────────────────────────────────┤
│            Dobbs Unified MCP Server             │
├────────────┬────────────┬────────────┬──────────┤
│ Existing   │  Kimi K2   │ Claude Flow│  Other   │
│   Tools    │Integration │ Hive-Mind  │ Services │
├────────────┴────────────┴────────────┴──────────┤
│                  Groq API                        │
│            (185 tokens/second)                   │
├─────────────────────────────────────────────────┤
│         Kimi K2 Model (1T parameters)           │
└─────────────────────────────────────────────────┘
```

## Advanced Features

### 1. Context Management

Kimi K2 supports a 128K context window, allowing for:
- Long mathematical proofs
- Multiple related problems in sequence
- Extensive background information
- Complete research papers

### 2. Tool Use Capabilities

Kimi K2 can autonomously:
- Call Wolfram Alpha for validation
- Generate and execute code
- Search for related research
- Create visualizations

### 3. Performance Optimization

- **Batch Processing**: Group related queries for efficiency
- **Caching**: Results are cached for repeated queries
- **Parallel Execution**: Use with Claude Flow for parallel processing
- **Streaming**: Support for streaming responses (coming soon)

## Best Practices

### 1. Prompt Engineering

```python
# Good: Specific and contextual
"In the context of Möbius gyrovector spaces, prove that the gyrotriangle inequality holds"

# Better: With explicit requirements
"Prove the gyrotriangle inequality for Möbius gyrovector spaces. Show:
1. The mathematical statement
2. Step-by-step proof
3. Geometric interpretation
4. Connection to hyperbolic geometry"
```

### 2. Domain Selection

Choose the appropriate domain for optimal results:
- `gyrovector`: For hyperbolic geometry and gyrovector operations
- `lattice`: For order theory and algebraic structures
- `harmonic`: For frequency analysis and decomposition
- `orbifold`: For quotient spaces and group actions
- `general`: For mixed or general mathematical problems

### 3. Validation Strategy

Always validate critical results:
```python
# Enable validation for important calculations
result = await call_tool("kimi_k2_solve_problem", {
    "problem": "Your critical problem",
    "validate": true  # Double-checks the solution
})
```

## Troubleshooting

### Common Issues

1. **API Key Error**
   - Verify GROQ_API_KEY is set in .env
   - Check key validity at console.groq.com

2. **Timeout Errors**
   - Increase KIMI_K2_TIMEOUT value
   - Check network connectivity
   - Consider smaller problem decomposition

3. **Mathematical Errors**
   - Enable validation for complex problems
   - Provide more context in prompts
   - Use domain-specific mode

### Debug Mode

Enable debug logging:
```python
import logging
logging.getLogger("kimi_k2_integration").setLevel(logging.DEBUG)
```

## Performance Metrics

Expected performance with Kimi K2:
- **Inference Speed**: 185 tokens/second
- **First Token Latency**: <500ms
- **Mathematical Accuracy**: 97.4% (MATH-500)
- **Code Generation**: 53.7% (LiveCodeBench)

## Future Enhancements

### Planned Features
- [ ] Streaming response support
- [ ] Advanced caching strategies
- [ ] Direct Mathematica integration
- [ ] Custom fine-tuning for specific domains
- [ ] Real-time collaborative editing
- [ ] Visual debugger for mathematical proofs

### Research Directions
- Automated theorem proving in gyrovector spaces
- Novel applications of recursive harmonics
- Orbifold classification algorithms
- Lattice-based cryptography applications

## Contributing

To contribute to the Kimi K2 integration:

1. Fork the repository
2. Create a feature branch
3. Add comprehensive tests
4. Submit a pull request

Focus areas for contributions:
- Additional mathematical domains
- Performance optimizations
- Visualization enhancements
- Documentation improvements

## References

- [Kimi K2 Model Card](https://github.com/MoonshotAI/Kimi-K2)
- [Groq Documentation](https://console.groq.com/docs)
- [MCP Specification](https://modelcontextprotocol.io)
- [Gyrovector Spaces Theory](https://arxiv.org/abs/math/0406130)

---

**Version**: 1.0.0  
**Last Updated**: July 2025  
**Maintainer**: Dobbs-MCP Team
