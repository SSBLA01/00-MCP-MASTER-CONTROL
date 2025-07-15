# Dobbs-MCP Master Control System

**Version 1.3.0** | **Claude Flow Integration: v2.0.0-alpha.53** | **Total Tools: 130+**

## 🚀 Overview

Dobbs-MCP is a unified Model Context Protocol (MCP) server providing AI-powered tools for mathematical research management, knowledge organization, and intelligent automation. This stable release integrates Claude Flow's hive-mind swarm intelligence, bringing the total tool count to over 130 specialized functions.

### Key Features
- **130+ Integrated Tools**: 43+ native tools + 87 Claude Flow tools
- **Multi-Platform Integration**: Dropbox, GitHub, Obsidian, Notion, Gemini AI, Perplexity, Wolfram Alpha
- **Mathematical Visualization**: Manim animations with gyrovector space support
- **Intelligent Automation**: Hourly inbox processing, smart file organization
- **Privacy-First Architecture**: Clear separation between private research and public content
- **Claude Flow Hive-Mind**: Queen-led swarm intelligence for complex workflows

## 📋 Table of Contents
- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Claude Flow Integration](#claude-flow-integration)
- [Tool Categories](#tool-categories)
- [Privacy & Security](#privacy--security)
- [Quality of Life Features](#quality-of-life-features)
- [API Documentation](#api-documentation)
- [Development Guide](#development-guide)
- [Troubleshooting](#troubleshooting)

## 🎯 Quick Start

### Prerequisites
- Python 3.8+
- Claude Desktop
- API Keys: Perplexity, Wolfram Alpha, Dropbox, GitHub, Notion, Gemini
- Optional: Docker Desktop, Mathematica

### Installation

```bash
# Clone the repository
git clone https://github.com/SSBLA01/00-MCP-MASTER-CONTROL.git
cd 00-MCP-MASTER-CONTROL

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r qol_improvements/requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys
```

### Claude Desktop Configuration

Add to your Claude Desktop config:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "Dobbs-MCP": {
      "command": "bash",
      "args": ["/path/to/00-MCP-MASTER-CONTROL/run_dobbs_mcp.sh"],
      "cwd": "/path/to/00-MCP-MASTER-CONTROL",
      "env": {
        "PYTHONPATH": "/path/to/00-MCP-MASTER-CONTROL"
      }
    }
  }
}
```

Restart Claude Desktop after configuration.

## 🏗️ Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                    Claude Desktop Interface                  │
├─────────────────────────────────────────────────────────────┤
│                  Dobbs Unified MCP Server                    │
│                  (src/servers/dobbs_unified.py)             │
├─────────────┬───────────────┬───────────────┬──────────────┤
│   File Ops  │  Research     │ Visualization │  Knowledge   │
│  (Dropbox)  │  Discovery    │   (Manim)     │ Management   │
├─────────────┼───────────────┼───────────────┼──────────────┤
│   GitHub    │   Gemini AI   │   Notion      │ Master Coord │
│    Ops      │  Operations   │   (Manual)    │  (Workflows) │
├─────────────┴───────────────┴───────────────┴──────────────┤
│               Claude Flow Integration Layer                  │
│          (87 tools: Hive-mind, WASM, Workflows)            │
├─────────────────────────────────────────────────────────────┤
│            Quality of Life Automation Daemon                 │
│        (Inbox Processing, Search Priority, Logging)         │
└─────────────────────────────────────────────────────────────┘
```

### Core Modules

1. **Master Coordinator** (`master_coordinator.py`)
   - Orchestrates multi-agent workflows
   - Session management with UUID tracking
   - Agent status monitoring
   - Workflow execution pipelines

2. **File Operations** (`file_operations.py`)
   - Full Dropbox CRUD operations
   - Binary file support
   - Smart path handling
   - SSL certificate management

3. **Research Discovery** (`research_discovery.py`)
   - Perplexity AI integration
   - arXiv paper search
   - Related work analysis
   - Trend tracking

4. **Mathematical Visualization** (`mathematical_visualization.py`)
   - Manim animation generation
   - Wolfram Alpha validation
   - Gyrovector space animations
   - Custom output paths

5. **Knowledge Management** (`knowledge_ingestion.py`)
   - Obsidian vault integration
   - Zettelkasten methodology
   - Smart categorization
   - GitHub sync

## 🧠 Claude Flow Integration

### Overview
Claude Flow v2.0.0-alpha.53 adds 87 specialized tools with hive-mind swarm intelligence, enabling complex mathematical computations and workflow orchestration.

### Key Features
- **Hive-Mind Architecture**: Queen-led coordination with 4 worker agents
- **Persistent Memory**: SQLite database at `.swarm/memory.db`
- **Neural Acceleration**: WASM SIMD support (future enhancement)
- **Enhanced GitHub**: 6 specialized modes for code management
- **Mathematical Workflows**: Pre-configured computation sequences

### Available Workflows

1. **Gyrovector-Sequential**: Step-by-step mathematical operations
2. **Gyrovector-Parallel**: Batch processing for performance
3. **Mathematical-Analysis**: Pattern discovery and validation
4. **Performance-Benchmarks**: Speed and accuracy testing

### Quick Commands

```bash
# Navigate to Claude Flow directory
cd /Users/scottbroock/Dropbox/MathematicalResearch/claude-flow-integration

# Search mathematical knowledge base
npx claude-flow@alpha memory search 'gyrovector'

# Execute gyrovector computation
./gyrovector-compute.sh compute gyroaddition '[0.3,0.4,0]' '[0.1,0.2,0.5]'

# Run workflow
npx claude-flow@alpha workflow execute "Mathematical-Analysis"

# Process Obsidian note with Claude Flow
python3 obsidian-integration.py your_note.md
```

### Obsidian Tag Integration
Use these tags in your notes to trigger Claude Flow:
- `#cf/compute` - Execute computational workflow
- `#cf/analyze` - Analyze mathematical structure
- `#cf/visualize` - Generate visualization request
- `#cf/explore` - Explore parameter space

## 🛠️ Tool Categories

### Dobbs-MCP Native Tools (43+)

#### File Operations (8 tools)
- `search_dropbox` - Search files by name, content, or folders
- `list_dropbox_folder` - Browse directory contents
- `read_dropbox_file` - Read file contents
- `save_to_dropbox` - Create/update files
- `copy_file` - Duplicate files (binary support)
- `move_file` - Relocate files
- `delete_file` - Remove files/folders
- `create_folder` - Create directories

#### GitHub Operations (7 tools)
- `list_github_repos` - View all repositories
- `browse_github_repo` - Explore repo structure
- `read_github_file` - Read file contents
- `create_github_file` - Create/update files
- `get_github_repo_info` - Repository metadata
- `list_github_commits` - Recent commit history
- `search_github` - Search code/repos

#### Research Tools (4 tools)
- `discover_research` - Find papers via Perplexity/arXiv
- `analyze_paper` - Extract key concepts
- `find_related_work` - Discover connected research
- `track_research_trends` - Monitor field developments

#### Visualization Tools (4 tools)
- `create_manim_animation` - Generate mathematical animations
- `validate_with_wolfram` - Verify mathematical statements
- `create_static_diagram` - Generate static visualizations
- `create_interactive_visual` - Build interactive demos

#### Knowledge Management (4 tools)
- `ingest_to_obsidian` - Create atomic notes
- `sync_to_dropbox` - Synchronize files
- `manage_github_repo` - Repository operations
- `create_smart_index` - Generate knowledge maps

#### Notion Integration (6 tools) - MANUAL ONLY
- `search_notion` - Find pages/databases
- `create_notion_page` - Create new pages
- `update_notion_page` - Modify existing pages
- `add_to_notion_database` - Add database entries
- `list_notion_databases` - View all databases
- `sync_obsidian_to_notion` - MANUAL publish only

#### Gemini AI Tools (6 tools)
- `gemini_query` - General AI analysis
- `gemini_analyze_code` - Code review/security
- `gemini_brainstorm` - Creative ideation
- `gemini_summarize` - Document summarization
- `gemini_math_analysis` - Mathematical exploration
- `gemini_research_review` - Paper critique

#### Coordination Tools (4 tools)
- `initiate_research_session` - Start research workflow
- `coordinate_workflow` - Orchestrate agents
- `get_session_status` - Monitor progress
- `manage_agents` - Control agent states

### Claude Flow Tools (87 additional)
- Hive-mind coordination tools
- Neural acceleration frameworks
- Enhanced GitHub operations (6 modes)
- Memory persistence operations
- Dynamic agent management
- Workflow orchestration
- Mathematical computation modules

## 🔒 Privacy & Security

### Privacy Architecture
- **Obsidian = PRIVATE**: All research stays local in Dropbox
- **Notion = PUBLIC**: Website frontend, explicit publishing only
- **NO AUTO-SYNC**: Manual control over all publishing
- **Encrypted Storage**: API keys in environment variables

### Security Features
- SSL certificate validation for all APIs
- Path validation prevents directory traversal
- No hardcoded credentials
- Comprehensive error logging
- Sandboxed file operations

## ✨ Quality of Life Features

### Automatic Inbox Processing (v1.3.0)
- **Location**: `/Users/scottbroock/Dropbox/00_MCP_INBOX`
- **Frequency**: Hourly automated sweeps
- **Smart Naming**: `[DOMAIN]_[AUTHOR]_[SUBJECT]_[ZETTELKASTEN_ID].[ext]`
- **Categorization**: Automatic domain detection and routing

### Search Priority System
1. GitHub Cloud (code repositories)
2. Dropbox Cloud (documents)
3. Notion Cloud (public content)
4. Obsidian Local (private notes)
5. Error Logs (diagnostics)

### Master Control Daemon
```bash
# Install as system service
python3 /path/to/mcp_qol_master.py --install

# Check status
python3 /path/to/mcp_qol_master.py --status

# Run diagnostics
python3 /path/to/mcp_qol_master.py --diagnostics
```

## 📚 API Documentation

### Tool Response Format
All tools return JSON responses:
```json
{
  "status": "success|error",
  "data": {...},
  "message": "Human-readable message",
  "metadata": {
    "timestamp": "ISO-8601",
    "tool": "tool_name",
    "duration_ms": 123
  }
}
```

### Session Management
```python
# Start research session
session = await initiate_research_session(
    topic="Gyrovector Trigonometry",
    research_type="deep_dive",
    output_formats=["obsidian", "manim"],
    priority_sources=["arxiv", "perplexity"]
)

# Execute workflow
workflow = await coordinate_workflow(
    session_id=session["session_id"],
    workflow_type="discover_visualize_ingest"
)
```

### Mathematical Formulas (Pre-loaded)
```json
{
  "gyroaddition": "u ⊕ v = (1 + u·v/γ_u γ_v)^(-1) [u + (1/γ_u)v + (γ_u/(1+γ_u))(u·v/γ_u²)u]",
  "gyroscalar": "r ⊗ u = tanh(r * atanh(||u||)) * (u/||u||)",
  "gyrodistance": "d(u,v) = atanh(||u ⊖ v||)",
  "gyroparallel_transport": "P_{u→v}(w) = w + 2(u·w)/(1+γ_u)u + 2(v·w)/(1+γ_v)v"
}
```

## 🔧 Development Guide

### Running Tests
```bash
# Core system tests
python test_system.py
python test_obsidian.py
python test_github.py

# Visualization tests
python visualizations/gyrovector/test_gyrovector.py

# Claude Flow tests
cd claude-flow-integration
npm test
```

### Adding New Tools
1. Define tool schema in appropriate server module
2. Implement async handler function
3. Register tool in ALL_TOOLS array
4. Add to tool handler switch statement
5. Update documentation

### Creating Visualizations
```python
# Example: Gyrovector animation
from manim import *

class GyrovectorAnimation(Scene):
    def construct(self):
        # Implementation following spatial layout patterns
        pass
```

## 🐛 Troubleshooting

### Common Issues

**Server won't start**
- Verify all API keys in `.env`
- Check Python version (3.8+)
- Ensure virtual environment activated
- Review Claude Desktop logs

**Claude Desktop doesn't see server**
- Absolute paths in config required
- Restart Claude Desktop after changes
- Check `run_dobbs_mcp.sh` permissions

**Manim animations fail**
- Install system dependencies: `ffmpeg`, `LaTeX`
- Verify `MANIM_OUTPUT_DIR` exists
- Check available disk space

**API errors**
- Perplexity API may need endpoint updates
- Verify API key validity
- Check rate limits

### Debug Commands
```bash
# Check environment
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.environ.get('DROPBOX_BASE_PATH'))"

# Test specific module
python -m src.servers.file_operations

# View logs
tail -f ~/.claude/logs/mcp.log
```

## 📈 Performance Optimization

- **Async Operations**: All I/O operations are non-blocking
- **Connection Pooling**: Reused HTTPS connections
- **Batch Processing**: Claude Flow parallel workflows
- **Smart Caching**: Persistent memory in SQLite
- **Resource Limits**: Configurable timeouts and retries

## 🚀 Future Enhancements

- [ ] WASM SIMD acceleration for mathematical computations
- [ ] Real-time collaboration features
- [ ] Advanced visualization templates
- [ ] Extended language model integrations
- [ ] Mobile companion app
- [ ] Distributed computing support

## 📄 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## 📞 Support

- **Issues**: GitHub Issues
- **Documentation**: This README and inline code comments
- **Community**: Mathematical Research Discord (coming soon)

---

**Built with ❤️ for the mathematical research community**