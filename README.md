# Mathematical Research MCP System (Dobbs-MCP)

## Overview
This MCP server system provides AI-powered tools for mathematical research management, including:
- Research discovery with Perplexity AI
- Mathematical visualization with Manim
- Knowledge organization with Obsidian
- Smart file management with Dropbox and GitHub

## Quick Start

### 1. Install Dependencies
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your API keys:
# - PERPLEXITY_API_KEY
# - WOLFRAM_ALPHA_APP_ID
# - DROPBOX_APP_KEY and DROPBOX_APP_SECRET
# - GITHUB_TOKEN
```

### 3. Configure Claude Desktop
Add the Dobbs-MCP server to your Claude Desktop configuration:

**On macOS:**
Edit `~/Library/Application Support/Claude/claude_desktop_config.json`

**On Windows:**
Edit `%APPDATA%\Claude\claude_desktop_config.json`

Add this configuration:
```json
{
  "mcpServers": {
    "Dobbs-MCP": {
      "command": "python",
      "args": ["-m", "src.servers.master_coordinator"],
      "cwd": "/Users/scottbroock/00 MCP MASTER CONTROL/mathematical-research-mcp",
      "env": {
        "PYTHONPATH": "/Users/scottbroock/00 MCP MASTER CONTROL/mathematical-research-mcp"
      }
    }
  }
}
```

### 4. Restart Claude Desktop
After updating the configuration, restart Claude Desktop to load the MCP server.

## Usage Examples

### Starting a Research Session
```
Initialize a research session on gyrovector trigonometry
```

### Discovering Research
```
Find recent papers on hyperbolic geometry using Perplexity
```

### Creating Visualizations
```
Create a Manim animation of stereographic projection
```

### Organizing Knowledge
```
Ingest this research paper into Obsidian under the "Papers" category
```

## Architecture

### Servers
- **Master Coordinator**: Orchestrates all agents and manages research sessions
- **Research Discovery Agent**: Finds papers using Perplexity and arXiv
- **Mathematical Visualization Agent**: Creates animations with Manim and validates with Wolfram
- **Knowledge Ingestion Agent**: Organizes content in Obsidian and syncs with Dropbox/GitHub

### Key Features
- Multi-agent coordination for complex workflows
- Smart categorization and tagging of mathematical content
- Integration with popular research tools and platforms
- Automated visualization generation
- Cross-platform synchronization

## API Keys Required
1. **Perplexity API Key**: For AI-powered research discovery
2. **Wolfram Alpha App ID**: For mathematical validation
3. **Dropbox App Key & Secret**: For cloud synchronization
4. **GitHub Token**: For version control of research

## Directory Structure
```
mathematical-research-mcp/
├── src/
│   ├── servers/
│   │   ├── master_coordinator.py
│   │   ├── research_discovery.py
│   │   ├── mathematical_visualization.py
│   │   └── knowledge_ingestion.py
│   └── utils/
│       └── common.py
├── data/
│   ├── obsidian_vault/
│   ├── manim_outputs/
│   └── dropbox_sync/
├── config/
│   └── mcp_config.yaml
├── .env
├── requirements.txt
└── README.md
```

## Troubleshooting

### Server won't start
1. Check that all API keys are properly configured in `.env`
2. Ensure the virtual environment is activated
3. Verify all dependencies are installed: `pip install -r requirements.txt`

### Claude Desktop doesn't see the server
1. Make sure the path in `claude_desktop_config.json` is absolute and correct
2. Restart Claude Desktop after configuration changes
3. Check the Claude Desktop logs for error messages

### Manim animations fail
1. Ensure Manim dependencies are installed: `manim --version`
2. Check that ffmpeg is installed on your system
3. Verify the MANIM_OUTPUT_DIR path exists and is writable

## Development

### Running Tests
```bash
pytest tests/
```

### Adding New Tools
1. Define the tool in the appropriate server file
2. Implement the tool handler function
3. Register the tool with the server
4. Update documentation

## License
MIT License - See LICENSE file for details