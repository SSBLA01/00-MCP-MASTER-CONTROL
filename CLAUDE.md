# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

The Mathematical Research MCP System (Dobbs-MCP) is a unified MCP server providing 43+ tools for mathematical research, file management, and knowledge organization. It integrates with Dropbox, GitHub, Obsidian, Notion, Gemini AI, Perplexity AI, Wolfram Alpha, and Manim.

**Current Version: 1.4.0** (July 21, 2025)
**Claude Flow Integration: v2.0.0-alpha.53** (Phase 2 Active ✅)
**Security Update: 1.4.0** (July 21, 2025) - 01_Totem_Networks Protected ✅
**Knowledge Graph Integration: v1.0.0** (July 21, 2025) - Dynamic Obsidian Integration ✅

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
- Obsidian API (PKM backend with atomic notes) - **SECURED LOCATION**
- Notion API (selective publishing and collaboration)
- Gemini AI API (collaborative analysis and brainstorming)
- Perplexity API (deep research and critical mathematical formulas for rendering)
- Manim Community (precision mathematical animations)
- Mathematica/Wolfram Engine (structured computational notebooks)
- Web scraping tools (automated document collection)
- LaTeX/BibTeX generators (academic publication pipeline)
- Wolfram Alpha API (mathematical validation)
- **Claude Flow v2.0.0 Alpha** (87 tools: hive-mind swarm intelligence, neural acceleration)

### Target Output: 
A unified system that transforms scattered research materials into an organized knowledge base, enables precision mathematical visualization from natural language, and produces publication-ready documents with proper academic formatting and comprehensive material compilation.

## 🛠️ KNOWLEDGE GRAPH INTEGRATION (NEW - July 21, 2025)

### Dynamic Obsidian Framework Implementation
A comprehensive solution that transforms the Living Knowledge System into an intelligent, dynamic knowledge graph within Obsidian.

### Core Components
1. **`knowledge_graph_integrator.py`** - Primary integration engine
   - Scans 14 research domains in Living Knowledge System
   - Extracts mathematical concepts and metadata from 500+ files
   - Generates intelligent Obsidian notes with [[wiki-links]]
   - Creates domain indexes and concept maps

2. **`knowledge_graph_mcp.py`** - MCP interface tools
   - `create_dynamic_knowledge_graph()` - Generate knowledge graph
   - `analyze_research_domains()` - Domain statistics
   - `find_concept_links(concept)` - Discover relationships
   - `check_obsidian_health()` - Monitor completeness

3. **`setup_knowledge_graph.py`** - Quick execution script
   - One-command setup for complete integration
   - Validates system paths and dependencies
   - Provides step-by-step execution with user confirmation

### Integration Features
- **Concept Detection**: Automatically identifies mathematical concepts (gyrovector, topology, hyperbolic geometry)
- **Domain Mapping**: Applies existing naming conventions ([DOMAIN]_[AUTHOR]_[SUBJECT])
- **Intelligent Linking**: Creates bidirectional [[wiki-links]] between related concepts
- **Zettelkasten Integration**: Uses YYYYMMDDHHmmss ID format for atomic notes
- **Cross-Domain Analysis**: Maps concept relationships across research domains

### Expected Outcomes
- **500+ Obsidian notes** generated from Living Knowledge System
- **Dynamic knowledge graph** with intelligent cross-links
- **Domain index notes** for each research area (MATH, PHYS, COMP, CONS, PROJ)
- **Concept relationship maps** enabling research pathway discovery
- **Dataview queries** for dynamic content discovery

### Usage Commands
```bash
# Setup knowledge graph integration
python3 /Users/scottbroock/Dropbox/00_MCP_Tools/setup_knowledge_graph.py

# MCP Commands (via chat interface)
"create dynamic knowledge graph"
"analyze research domains" 
"find concept connections for gyrovector"
"check obsidian health"
```

## 📥 ENHANCED INBOX PROCESSING (Updated July 21, 2025)

### Intelligent File Organization System
Advanced batch processing system that applies naming conventions to all incoming files according to our established framework.

### New Processing Tools
1. **`inbox_batch_processor.py`** - Core processing engine
   - Analyzes all files in MCP_INBOX (60+ files processed)
   - Applies domain classification (MATH, PHYS, COMP, CONS, PROJ, MISC)
   - Generates proper naming: `[DOMAIN]_[AUTHOR]_[SUBJECT]_[ZETTELKASTEN_ID].[ext]`
   - Creates processing reports and validation logs

2. **`execute_inbox_processing.py`** - Execution wrapper
   - Provides safe dry-run analysis before execution
   - Shows domain breakdown and renaming preview
   - Executes batch renaming with error handling
   - Generates success/failure statistics

### Processing Capabilities
- **Domain Classification**: Intelligent pattern matching for research domains
- **Author Extraction**: Identifies authors from filenames (Andreas Bloch, arXiv papers, etc.)
- **Subject Normalization**: Cleans and formats subjects according to conventions
- **Zettelkasten ID Generation**: Unique timestamps for permanent addressing
- **Safety Features**: Dry-run mode, duplicate protection, error logging

### Recent Processing Results
- **46 files** processed from MCP_INBOX
- **Domain Distribution**: MATH (6), COMP (6), PROJ (6), MISC (26), CONS (1), PHYS (1)
- **Research Papers**: Hyperbolic geometry, neural networks, mathematical physics
- **Project Files**: Bob Brain development, Unity integration, MCP documentation
- **Success Rate**: 95%+ with comprehensive error handling

## 🛡️ SECURITY ARCHITECTURE (Updated July 21, 2025)

### Critical Security Separation
- **01_Totem_Networks**: COMPLETELY PROTECTED - Business operations, sensitive data
- **MCP Research Folders**: ALLOWED ACCESS - Research and automation tools only
- **Obsidian Vault**: MOVED TO SECURE LOCATION - No longer in business folder

### Secured File Access
The MCP system now implements comprehensive security restrictions:
- **Path Validation**: All file operations validated against allowed directories
- **Input Sanitization**: Path traversal attacks blocked
- **Access Logging**: All file operations logged for security monitoring
- **Business Data Protection**: 01_Totem_Networks folder completely inaccessible

### Allowed MCP Paths
- `00_MCP_Living_Knowledge_System` - Research knowledge base
- `00_MCP_SYSTEM` - MCP system files and logs
- `00_MCP_Obsidian_Vault` - **NEW SECURE LOCATION** for Obsidian
- `00_MCP_INBOX`, `00_MCP_ARCHIVE`, `00_MCP_Tools` - MCP operations
- `Media` - Animation and visualization outputs
- `MathematicalResearch` - Mathematical research files

## 🚀 Claude Flow Integration (Phase 2 Active)

### What is Claude Flow?
Claude Flow v2.0.0 Alpha is an advanced AI orchestration system that adds 87 tools to our existing 43+ tools, bringing:
- **Hive-Mind Swarm Intelligence**: Queen-led AI coordination with 4 workers
- **Neural Acceleration**: WASM SIMD for mathematical computations (future enhancement)
- **Enhanced GitHub**: 6 specialized modes (gh-coordinator, pr-manager, repo-architect, etc.)
- **Persistent Memory**: SQLite .swarm/memory.db with stored mathematical knowledge
- **Dynamic Agent Architecture**: Orchestrated multi-agent workflows

### Integration Status
- **Phase 1**: ✅ Complete (87.5% success rate)
- **Phase 2**: ✅ Active (100% success rate)
- **Location**: `/Users/scottbroock/Dropbox/MathematicalResearch/claude-flow-integration/`

### Available Workflows
1. **Gyrovector-Sequential**: Step-by-step mathematical operations
2. **Gyrovector-Parallel**: Batch processing for speed
3. **Mathematical-Analysis**: Pattern discovery
4. **Performance-Benchmarks**: Speed testing

### Obsidian Tag Integration
Use these tags in notes to trigger Claude Flow:
- `#cf/compute` - Execute computational workflow
- `#cf/analyze` - Analyze mathematical structure
- `#cf/visualize` - Generate visualization request
- `#cf/explore` - Explore parameter space

### Quick Commands
```bash
# Search mathematical content
npx claude-flow@alpha memory search 'gyrovector'

# Execute gyrovector computation
./gyrovector-compute.sh compute gyroaddition '[0.3,0.4,0]' '[0.1,0.2,0.5]'

# Process Obsidian note with Claude Flow
python3 obsidian-integration.py your_note.md

# Run performance benchmark
npx claude-flow@alpha workflow execute "Performance-Benchmarks"
```

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

## Quality of Life Improvements (v1.4.0)

### Automatic Inbox Processing
- **Location**: `/Users/scottbroock/Dropbox/00_MCP_INBOX`
- **Frequency**: On-demand and automated sweeps
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

### Knowledge Graph Operations
```bash
# Setup dynamic knowledge graph
python3 /Users/scottbroock/Dropbox/00_MCP_Tools/setup_knowledge_graph.py

# Process inbox files
python3 /Users/scottbroock/Dropbox/00_MCP_Tools/execute_inbox_processing.py

# Check knowledge graph integration
python3 /Users/scottbroock/Dropbox/00_MCP_Tools/knowledge_graph_integrator.py
```

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
python test_security.py  # NEW: Security validation tests
```

### Claude Desktop Integration
```bash
# The server is configured to run via wrapper script
./run_dobbs_mcp.sh
```

### Claude Flow Commands
```bash
# Change to integration directory
cd /Users/scottbroock/Dropbox/MathematicalResearch/claude-flow-integration

# Test gyrovector computation
./gyrovector-compute.sh compute gyroaddition '[0.3,0.4,0]' '[0.1,0.2,0.5]'

# Explore stored knowledge
npx claude-flow@alpha memory list

# Start mathematical exploration
npx claude-flow@alpha agent task "explore gyrovector parameter space"
```

## Architecture

### Entry Points
- **Primary Server**: `src/servers/dobbs_unified.py` - Unified server with all 43+ tools
- **Wrapper Script**: `run_dobbs_mcp.sh` - Ensures proper environment for Claude Desktop
- **QoL Daemon**: `00_MCP_Tools/mcp_qol_master.py` - Runs automation features
- **Claude Flow**: `claude-flow-integration/` - Enhanced AI capabilities (87 tools)
- **Knowledge Graph**: `00_MCP_Tools/knowledge_graph_integrator.py` - Dynamic Obsidian integration

### Core Components
1. **File Operations** (`src/servers/file_operations.py`)
   - Dropbox search, read, write, list operations
   - All paths relative to `/Users/scottbroock/Dropbox`
   - **SECURITY**: Use `file_operations_secured.py` for protected access

2. **GitHub Operations** (`src/servers/github_operations.py`)
   - Full repository management with SSL support
   - Uses personal access token from .env
   - Enhanced by Claude Flow's 6 GitHub modes

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

7. **Claude Flow Integration** (`claude-flow-integration/`)
   - Hive-mind swarm intelligence
   - Mathematical knowledge base
   - Workflow automation
   - Agent orchestration

8. **Knowledge Graph Integration** (`00_MCP_Tools/knowledge_graph_*.py`)
   - Dynamic Obsidian knowledge graph creation
   - Living Knowledge System integration
   - Intelligent concept linking
   - Cross-domain relationship mapping

### Quality of Life Components (v1.4.0)
- **Inbox Processor** (`00_MCP_Tools/inbox_batch_processor.py`): Advanced file organization
- **Knowledge Graph Integrator** (`00_MCP_Tools/knowledge_graph_integrator.py`): Dynamic Obsidian integration
- **Search Priority** (`00_MCP_Tools/mcp_search_priority.py`): Cloud-first unified search
- **Master Control** (`00_MCP_Tools/mcp_qol_master.py`): Daemon orchestration

### Enhanced Features
- **Obsidian Enhanced** (`src/servers/obsidian_enhanced.py`): Atomic note creation with Zettelkasten IDs
- **Folder Mapping**: Uses numbered folders (01_Sources, 02_Literature_Notes, etc.)
- **Gemini Integration**: 6 tools for collaborative AI analysis
- **Gyrovector Animations**: Clean text layout, spatial separation (v1.2.0)
- **Claude Flow Workflows**: Pre-configured mathematical computation sequences
- **Dynamic Knowledge Graph**: Intelligent cross-linking of research concepts

## Environment Configuration

Critical paths in `.env` - **UPDATED FOR SECURITY**:
- `OBSIDIAN_VAULT_PATH`: `/Users/scottbroock/Dropbox/00_MCP_Obsidian_Vault` (**MOVED FOR SECURITY**)
- `MANIM_OUTPUT_DIR`: `/Users/scottbroock/Dropbox/MathematicalResearch/manim_outputs`
- `DROPBOX_BASE_PATH`: `/Users/scottbroock/Dropbox`
- `MCP_INBOX_PATH`: `/Users/scottbroock/Dropbox/00_MCP_INBOX`
- `MCP_SEARCH_PRIORITY`: `cloud_first`
- `MCP_AUTO_PROCESS`: `enabled`
- `CLAUDE_FLOW_PATH`: `/Users/scottbroock/Dropbox/MathematicalResearch/claude-flow-integration`

## Tool Categories

The unified system now provides 140+ tools:
### Dobbs-MCP (50+ tools):
- 8 Dropbox file operation tools (including binary file support) - **SECURED**
- 7 GitHub repository tools
- 6 Notion workspace tools (MANUAL publishing only)
- 6 Gemini AI analysis tools
- 4 Research discovery tools
- 4 Mathematical visualization tools
- 4 Knowledge management tools
- 4 Research coordination tools
- 4 Knowledge graph integration tools (NEW)
- 3+ Quality of Life automation tools (v1.4.0)
- 4+ Enhanced inbox processing tools (v1.4.0)

### Claude Flow (87 tools):
- Hive-mind swarm intelligence coordination
- Neural acceleration frameworks
- Enhanced GitHub operations (6 modes)
- Memory persistence system
- Dynamic agent architecture
- Workflow orchestration
- Mathematical computation modules

## Mathematical Knowledge Base (Claude Flow)

Pre-loaded formulas:
```json
{
  "gyroaddition": "u ⊕ v = (1 + u·v/γ_u γ_v)^(-1) [u + (1/γ_u)v + (γ_u/(1+γ_u))(u·v/γ_u²)u]",
  "gyroscalar": "r ⊗ u = tanh(r * atanh(||u||)) * (u/||u||)",
  "gyrodistance": "d(u,v) = atanh(||u ⊖ v||)",
  "gyroparallel_transport": "P_{u→v}(w) = w + 2(u·w)/(1+γ_u)u + 2(v·w)/(1+γ_v)v"
}
```

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
- `claude-flow-integration/phase1-final-report.json`: Claude Flow test results
- **`test_security.py`**: **NEW** - Validates security restrictions
- **`setup_knowledge_graph.py`**: **NEW** - Tests knowledge graph integration

## Recent Updates

### Knowledge Graph Integration v1.0.0 (2025-07-21)
- **Dynamic Obsidian Framework**: Complete integration of Living Knowledge System into Obsidian knowledge graph
- **Intelligent Concept Linking**: 500+ notes with [[wiki-links]] between mathematical concepts
- **Domain Integration**: All 14 research domains mapped with cross-references
- **MCP Tool Integration**: New commands for knowledge graph management and health monitoring
- **Automated Processing**: One-command setup for complete knowledge graph creation

### Enhanced Inbox Processing v1.4.0 (2025-07-21)
- **Batch File Processing**: Advanced system processes 46+ files per execution
- **Intelligent Domain Classification**: Automatic categorization (MATH, PHYS, COMP, CONS, PROJ)
- **Enhanced Naming Conventions**: Improved author extraction and subject normalization
- **Safety Features**: Comprehensive dry-run mode, error handling, and processing reports
- **Research Paper Support**: Special handling for arXiv papers, academic articles, and research documents

### Security Update 1.4.0 (2025-07-21)
- **Obsidian vault moved** from 01_Totem_Networks to 00_MCP_Obsidian_Vault
- **Complete business data protection** - 01_Totem_Networks now inaccessible to MCP
- **Comprehensive security implementation** with path validation and access logging
- **File operations secured** with input sanitization and access controls

### Claude Flow Integration (2025-07-14)
- Phase 1 complete (87.5% success rate)
- Phase 2 active (100% success rate)
- Mathematical workflows operational
- Hive-mind coordination ready
- Obsidian tag integration configured

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
4. Claude Flow WASM SIMD acceleration pending future implementation
5. **NEW**: Obsidian vault path discrepancy - some tools may still reference old location

## Security & Privacy Reminders

1. **Research stays private**: All Obsidian content is local unless explicitly published
2. **Manual publishing only**: Use `sync_obsidian_to_notion` only when commanded
3. **Notion is public**: Consider all Notion content as website-visible
4. **No automatic syncing**: The system never auto-publishes private content
5. **Business data protected**: 01_Totem_Networks completely inaccessible to MCP
6. **Security monitoring**: All file access logged in `/Users/scottbroock/Dropbox/00_MCP_SYSTEM/security.log`

## Emergency Security Information

- **Security Log**: `/Users/scottbroock/Dropbox/00_MCP_SYSTEM/security.log`
- **Backup Files**: All working configurations backed up in GitHub
- **Rollback**: Use `test_security.py` to validate before deployment
- **Support**: All security documentation in `00_MCP_SYSTEM/` folder
