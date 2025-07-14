# Changelog

All notable changes to the MCP Master Control system will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2025-07-14

### Added
- **Gyrovector Visualization Module** - New module for visualizing hyperbolic geometry
  - `gyrovector_clean.py` - Clean animation with proper text layout
  - `gyrovector_quick.py` - Quick demo version
  - Mathematical foundations documentation
  - README for the visualization module
- **Animation Text Fix** - Resolved overlapping text issues in Manim animations
  - Implemented spatial layout separation
  - Added proper label positioning strategy
  - Created dedicated formula areas

### Changed
- Updated main README with visualization module information
- Improved animation rendering workflow
- Enhanced text positioning in all Manim scenes

### Fixed
- Text overlapping in Manim animations
- Label collision in Poincaré disk visualizations
- Formula readability issues

## [1.1.0] - 2025-07-11

### Added
- Notion integration support
- Enhanced Manim custom output paths
- Improved MCP API documentation

### Changed
- Updated configuration structure
- Improved error handling in visualization pipeline

## [1.0.0] - 2025-07-01

### Added
- Initial release of MCP Master Control system
- Research discovery with Perplexity AI
- Mathematical visualization with Manim
- Knowledge organization with Obsidian
- Dropbox and GitHub synchronization
- Multi-agent coordination system

### Core Features
- Master Coordinator for orchestrating agents
- Research Discovery Agent
- Mathematical Visualization Agent
- Knowledge Ingestion Agent