# Gyrovector Visualization Module

This module provides Manim-based visualizations for gyrovector spaces, orbifolds, and gyrotrigonometry.

## Files

### Core Animations
- `gyrovector_clean.py` - Clean animation demonstrating Möbius addition in Poincaré disk
- `gyrovector_quick.py` - Quick demo version
- `gyrovector_animation.py` - Extended version with more features

### Mathematical Implementation
- Core Möbius addition formula
- Gyration operators
- Poincaré disk visualization

## Usage

```bash
# Generate animation
manim -pql gyrovector_clean.py GyrovectorCleanAnimation

# High quality render
manim -pqh gyrovector_clean.py GyrovectorCleanAnimation
```

## Output
Animations are saved to the MCP Living Knowledge System visualization folder:
`00_MCP_Living_Knowledge_System/10_Visualization_Media/`

## Dependencies
- Manim Community Edition
- NumPy
- Python 3.8+