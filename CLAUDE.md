# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

The Mathematical Research MCP System (Dobbs-MCP) is a unified MCP server providing 43+ tools for mathematical research, file management, and knowledge organization. It integrates with Dropbox, GitHub, Obsidian, Notion, Gemini AI, Perplexity AI, Wolfram Alpha, and Manim.

**Current Version: 1.3.0** (July 14, 2025)

## Project Mission: Integrated Mathematical Research Knowledge Management & Publication System

We are developing an intelligent research automation platform to organize, validate, and publish advanced mathematical research (focusing on gyrovectors, gyrovector trigonometry, and hyperbolic geometry). The system transforms a vast existing body of work into an organized, searchable knowledge base while enabling seamless creation of publication-ready materials.

### Core Workflow Requirements:

1. **Knowledge Organization**: Collect and atomically organize existing research materials from local computer and cloud storage into Obsidian PKM backend, creating interconnected atomic notes with mathematical concept linking

2. **Intelligent Content Discovery**: Simple web crawling that automatically extracts and downloads interesting documents/links from research pages without manual clicking through each item

3. **Smart File Management**: Automatically organize ingested materials in Dropbox with consistent naming conventions capturing 1-2 keywords and classification tags (support/further research/key document)

4. **Precision Mathematical Visualization**: Translate complex plain English prompts into mathematically accurate Manim animations (e.g., "render a manim animation of a stereo projected S³ sphere on a polar plane, and then rotate the plane relative to the pole")

5. **Structured Documentation**: Generate well-organized Mathematica notebooks with proper headings, sections, explanatory paragraphs, and numbered inline LaTeX formulas for academic indexing

6. **Selective Publishing**: Choose specific content from Obsidian to push to Notion, including new page creation with customizable placement options

7. **Session Compilation**: Collect all materials from a research session and organize into comprehensive PDFs with embedded images/graphics, plus generate corresponding .tex and .bib files for publication

### Primary Tools & Infrastructure:
- GitHub (code repository and version control)
- Dropbox API (cloud storage with smart naming)
- Docker Desktop (containerized tool deployment)
- Obsidian API (PKM backend with atomic notes)
- Notion API (selective publishing and collaboration)
- Gemini AI API (collaborative analysis and brainstorming)
- Perplexity API (deep research and critical mathematical formulas for rendering)
- Manim Community (precision mathematical animations)
- Mathematica/Wolfram Engine (structured computational notebooks)
- Web scraping tools (automated document collection)
- LaTeX/BibTeX generators (academic publication pipeline)
- Wolfram Alpha API (mathematical validation)

### Target Output: 
A unified system that transforms scattered research materials into an organized knowledge base, enables precision mathematical visualization from natural language, and produces publication-ready documents with proper academic formatting and comprehensive material compilation.

## 🚨 CRITICAL PRIVACY ARCHITECTURE

### Obsidian vs Notion Separation
- **Obsidian = PRIVATE**: All research, drafts, and personal notes stay local in Dropbox
- **Notion = PUBLIC**: Website frontend, only contains explicitly published content
- **NO AUTOMATIC SYNCING**: `sync_obsidian_to_notion` is MANUAL ONLY, requires explicit command
- **Inbox Processing**: Files go to Obsidian by default, NEVER auto-publish to Notion

### Search Priority Hierarchy (v1.3.0)
1. GitHub Cloud (repositories and code)
2. Dropbox Cloud (documents and files)
3. Notion Cloud (public content only)
4. Obsidian (local knowledge base)
5. Error Logs (Claude Desktop logs)

## Quality of Life Improvements (v1.3.0)

### Automatic Inbox Processing
- **Location**: `/Users/scottbroock/Dropbox/00_MCP_INBOX`
- **Frequency**: Hourly automated sweeps
- **Naming**: Applies RENAMING_GUIDE.md conventions automatically
- **Format**: `[DOMAIN]_[AUTHOR]_[SUBJECT]_[ZETTELKASTEN_ID].[ext]`
- **Destination**: Organized into appropriate Living Knowledge System folders
- **Privacy**: All processed files stay in Obsidian (private) unless explicitly published

### File Organization System
Domain codes for automatic categorization:
- MATH - Mathematics
- PHYS - Physics
- COMP - Computer Science
- CONS - Consciousness
- BUSI - Business
- LEGA - Legal
- OPER - Operations
- WRIT - Writing
- PROJ - Projects
- BOOK - Books
- MISC - Miscellaneous

### Master Control Daemon
```bash
# Install as system service (runs automatically)
python3 /Users/scottbroock/Dropbox/00_MCP_Tools/mcp_qol_master.py --install

# Check status
python3 /Users/scottbroock/Dropbox/00_MCP_Tools/mcp_qol_master.py --status

# Run diagnostics
python3 /Users/scottbroock/Dropbox/00_MCP_Tools/mcp_qol_master.py --diagnostics
```

## Key Commands

### Development
```bash
# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install/update dependencies
pip install -r requirements.txt
pip install -r qol_improvements/requirements.txt  # For v1.3.0 features

# Run the unified server (primary entry point)
python -m src.servers.dobbs_unified

# Run tests
python test_system.py
python test_obsidian.py
python test_github.py
python visualizations/gyrovector/test_gyrovector.py  # New in v1.2.0
```

### Claude Desktop Integration
```bash
# The server is configured to run via wrapper script
./run_dobbs_mcp.sh
```

## Architecture

### Entry Points
- **Primary Server**: `src/servers/dobbs_unified.py` - Unified server with all 43+ tools
- **Wrapper Script**: `run_dobbs_mcp.sh` - Ensures proper environment for Claude Desktop
- **QoL Daemon**: `00_MCP_Tools/mcp_qol_master.py` - Runs automation features

### Core Components
1. **File Operations** (`src/servers/file_operations.py`)
   - Dropbox search, read, write, list operations
   - All paths relative to `/Users/scottbroock/Dropbox`

2. **GitHub Operations** (`src/servers/github_operations.py`)
   - Full repository management with SSL support
   - Uses personal access token from .env

3. **Research Tools** (`src/servers/research_discovery.py`)
   - Perplexity AI integration (note: API may need updates)
   - arXiv search capabilities

4. **Visualization** (`src/servers/mathematical_visualization.py`)
   - Manim animation generation
   - Wolfram Alpha validation
   - Outputs to Dropbox: `/MathematicalResearch/manim_outputs`
   - **NEW**: Gyrovector visualization module (`visualizations/gyrovector/`)

5. **Knowledge Management** (`src/servers/knowledge_ingestion.py`)
   - Obsidian vault integration
   - Zettelkasten note creation with timestamps
   - Smart indexing
   - **PRIVACY**: All content stays local unless explicitly published

6. **Gemini Operations** (`src/servers/gemini_operations.py`)
   - AI-powered analysis and brainstorming
   - Code security and performance analysis
   - Mathematical concept exploration
   - Research review and feedback

### Quality of Life Components (v1.3.0)
- **Inbox Processor** (`00_MCP_Tools/mcp_inbox_processor.py`): Hourly file organization
- **Search Priority** (`00_MCP_Tools/mcp_search_priority.py`): Cloud-first unified search
- **Master Control** (`00_MCP_Tools/mcp_qol_master.py`): Daemon orchestration

### Enhanced Features
- **Obsidian Enhanced** (`src/servers/obsidian_enhanced.py`): Atomic note creation with Zettelkasten IDs
- **Folder Mapping**: Uses numbered folders (01_Sources, 02_Literature_Notes, etc.)
- **Gemini Integration**: 6 tools for collaborative AI analysis
- **Gyrovector Animations**: Clean text layout, spatial separation (v1.2.0)

## Environment Configuration

Critical paths in `.env`:
- `OBSIDIAN_VAULT_PATH`: `/Users/scottbroock/Dropbox/01_Totem_Networks/04_Obsidian`
- `MANIM_OUTPUT_DIR`: `/Users/scottbroock/Dropbox/MathematicalResearch/manim_outputs`
- `DROPBOX_BASE_PATH`: `/Users/scottbroock/Dropbox`
- `MCP_INBOX_PATH`: `/Users/scottbroock/Dropbox/00_MCP_INBOX`
- `MCP_SEARCH_PRIORITY`: `cloud_first`
- `MCP_AUTO_PROCESS`: `enabled`

## Tool Categories

The unified server provides 43+ tools:
- 8 Dropbox file operation tools (including binary file support)
- 7 GitHub repository tools
- 6 Notion workspace tools (MANUAL publishing only)
- 6 Gemini AI analysis tools
- 4 Research discovery tools
- 4 Mathematical visualization tools
- 4 Knowledge management tools
- 4 Research coordination tools
- 3+ Quality of Life automation tools (v1.3.0)

## SSL/Certificate Handling

GitHub, Notion, and research APIs use custom SSL contexts:
```python
ssl_context = ssl.create_default_context(cafile=certifi.where())
connector = aiohttp.TCPConnector(ssl=ssl_context)
```

## Testing

Key test files:
- `test_system.py`: Creates sample Obsidian notes and Manim scripts
- `test_obsidian.py`: Tests Zettelkasten integration
- `test_github.py`: Verifies GitHub API connectivity
- `create_manim_demo.py`: Generates actual MP4 videos
- `visualizations/gyrovector/test_gyrovector.py`: Tests gyrovector math operations

## Recent Updates

### Version 1.3.0 (2025-07-14)
- Added automatic hourly inbox processing
- Implemented search priority hierarchy
- Enhanced Claude Desktop integration
- Clarified Obsidian vs Notion privacy separation
- Created quality of life automation daemon

### Version 1.2.0 (2025-07-14)
- Added gyrovector visualization module
- Fixed Manim text overlapping issues
- Created mathematical foundations documentation
- Improved animation spatial layouts

## Known Issues

1. Perplexity API returns 400 errors - may need endpoint/auth updates
2. Manim requires system dependencies (ffmpeg, LaTeX)
3. Dropbox OAuth flow not fully implemented (using app key/secret)

## Privacy Reminders

1. **Research stays private**: All Obsidian content is local unless explicitly published
2. **Manual publishing only**: Use `sync_obsidian_to_notion` only when commanded
3. **Notion is public**: Consider all Notion content as website-visible
4. **No automatic syncing**: The system never auto-publishes private content