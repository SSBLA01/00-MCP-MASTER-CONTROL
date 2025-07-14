# Changelog

All notable changes to the MCP Master Control system will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.3.0] - 2025-07-14

### Added
- **MCP Quality of Life Improvements** - Major automation and usability enhancements
  - **Automated Inbox Processor** (`mcp_inbox_processor.py`)
    - Hourly automatic processing of files from MCP_INBOX
    - Intelligent content analysis and categorization
    - Automatic application of RENAMING_GUIDE.md conventions
    - PDF text extraction and domain detection
    - URL to markdown conversion
    - Archive system with tracking
  - **Search Priority System** (`mcp_search_priority.py`)
    - Hierarchical search: GitHub → Dropbox → Obsidian → Logs
    - Unified search interface across all sources
    - Context extraction for search results
    - Comprehensive search reporting
  - **Master Control System** (`mcp_qol_master.py`)
    - Background daemon mode with hourly processing
    - Interactive command-line interface
    - System diagnostics and health checks
    - Launch daemon for automatic startup
    - Status reporting and monitoring
- **Claude Desktop Integration Enhancements**
  - Automatic configuration updates
  - Cloud-first search priority
  - Environment variable management
  - Primary agent role enforcement

### Changed
- Search behavior now prioritizes cloud sources over local files
- File processing workflow automated with intelligent routing
- Error logging improved with centralized log management

### Security
- Input validation for all file operations
- MD5 hashing for file integrity verification
- Configurable paths via environment variables
- Comprehensive error handling throughout

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