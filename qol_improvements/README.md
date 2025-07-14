# MCP Quality of Life Improvements

This directory contains automation tools to improve the MCP system's usability and efficiency.

## Components

### 1. MCP Inbox Processor (`mcp_inbox_processor.py`)
Automatically processes files from the MCP_INBOX hourly:
- Applies proper naming conventions from RENAMING_GUIDE.md
- Categorizes files by content analysis
- Moves files to appropriate knowledge system folders
- Archives originals with tracking

### 2. MCP Search Priority (`mcp_search_priority.py`)
Implements hierarchical search across all data sources:
1. GitHub Cloud (first priority)
2. Dropbox Cloud
3. Obsidian (in Dropbox)
4. Error Logs (Claude Desktop)

### 3. MCP QoL Master Control (`mcp_qol_master.py`)
Master control system that integrates all features:
- Runs as background daemon
- Provides status reports
- Includes diagnostics
- Can be installed as system service

## Installation

1. Install dependencies:
```bash
pip install PyPDF2 schedule requests
```

2. Install as system service (macOS):
```bash
python3 mcp_qol_master.py --install
```

3. The service will automatically start on system boot and run hourly inbox sweeps.

## Usage

### Check Status
```bash
python3 mcp_qol_master.py --status
```

### Run Diagnostics
```bash
python3 mcp_qol_master.py --diagnostics
```

### Search All Sources
```bash
python3 mcp_qol_master.py --search "your query"
```

### Interactive Mode
```bash
python3 mcp_qol_master.py
```

## Configuration

Environment variables can be set in the launch daemon or shell:
- `MCP_INBOX_PATH`: Path to inbox folder
- `MCP_LKS_PATH`: Path to Living Knowledge System
- `MCP_ARCHIVE_PATH`: Path to archive folder
- `MCP_SEARCH_PRIORITY`: Set to "cloud_first"
- `MCP_AUTO_PROCESS`: Set to "enabled"

## Logs

All logs are stored in:
- `/Users/scottbroock/Dropbox/00_MCP_Tools/logs/`
- Individual component logs
- Master control logs
- Error logs

## Integration with Claude Desktop

The system automatically configures Claude Desktop to:
- Prioritize cloud searches over local files
- Act as the primary agent for MCP operations
- Use the unified search system

## Security Features

- Input validation and sanitization
- File integrity checking with MD5
- Comprehensive error handling
- Secure file operations
- Configurable paths (no hardcoding)