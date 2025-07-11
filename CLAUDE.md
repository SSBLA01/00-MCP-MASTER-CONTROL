# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

The Mathematical Research MCP System (Dobbs-MCP) is a unified MCP server providing 27 tools for mathematical research, file management, and knowledge organization. It integrates with Dropbox, GitHub, Obsidian, Perplexity AI, Wolfram Alpha, and Manim.

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
- Perplexity API (deep research and critical mathematical formulas for rendering)
- Manim Community (precision mathematical animations)
- Mathematica/Wolfram Engine (structured computational notebooks)
- Web scraping tools (automated document collection)
- LaTeX/BibTeX generators (academic publication pipeline)
- Wolfram Alpha API (mathematical validation)

### Target Output: 
A unified system that transforms scattered research materials into an organized knowledge base, enables precision mathematical visualization from natural language, and produces publication-ready documents with proper academic formatting and comprehensive material compilation.

## Key Commands

### Development
```bash
# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install/update dependencies
pip install -r requirements.txt

# Run the unified server (primary entry point)
python -m src.servers.dobbs_unified

# Run tests
python test_system.py
python test_obsidian.py
python test_github.py
```

### Claude Desktop Integration
```bash
# The server is configured to run via wrapper script
./run_dobbs_mcp.sh
```

## Architecture

### Entry Points
- **Primary Server**: `src/servers/dobbs_unified.py` - Unified server with all 27 tools
- **Wrapper Script**: `run_dobbs_mcp.sh` - Ensures proper environment for Claude Desktop

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

5. **Knowledge Management** (`src/servers/knowledge_ingestion.py`)
   - Obsidian vault integration
   - Zettelkasten note creation with timestamps
   - Smart indexing

6. **Gemini Operations** (`src/servers/gemini_operations.py`)
   - AI-powered analysis and brainstorming
   - Code security and performance analysis
   - Mathematical concept exploration
   - Research review and feedback

### Enhanced Features
- **Obsidian Enhanced** (`src/servers/obsidian_enhanced.py`): Atomic note creation with Zettelkasten IDs
- **Folder Mapping**: Uses numbered folders (01_Sources, 02_Literature_Notes, etc.)
- **Gemini Integration**: 6 tools for collaborative AI analysis

## Environment Configuration

Critical paths in `.env`:
- `OBSIDIAN_VAULT_PATH`: `/Users/scottbroock/Dropbox/01_Totem_Networks/04_Obsidian`
- `MANIM_OUTPUT_DIR`: `/Users/scottbroock/Dropbox/MathematicalResearch/manim_outputs`
- `DROPBOX_BASE_PATH`: `/Users/scottbroock/Dropbox`

## Tool Categories

The unified server provides 43 tools:
- 8 Dropbox file operation tools (including binary file support)
- 7 GitHub repository tools
- 6 Notion workspace tools
- 6 Gemini AI analysis tools
- 4 Research discovery tools
- 4 Mathematical visualization tools
- 4 Knowledge management tools
- 4 Research coordination tools

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

## Known Issues

1. Perplexity API returns 400 errors - may need endpoint/auth updates
2. Manim requires system dependencies (ffmpeg, LaTeX)
3. Dropbox OAuth flow not fully implemented (using app key/secret)