# Unified Server Configuration Fix

## Issue
After the Flow upgrade, the Dobbs-MCP server is not starting the unified version with all tools. It keeps falling back to the basic master_coordinator.

## Root Cause
The `claude_desktop_config.json` file points to `src.servers.master_coordinator` instead of `src.servers.dobbs_unified`.

## Solution
This patch updates the configuration to use the unified server that includes all the required tools:

### Tools Included in Unified Server
- **Geometric Tools**: Manim animations, static diagrams, interactive visuals
- **Algebraic Validation**: Wolfram Alpha integration
- **Trigonometric Computations**: Mathematical analysis tools
- **File Operations**: Dropbox and GitHub integration
- **Knowledge Management**: Obsidian and Notion support
- **AI Assistance**: Gemini integration

## Changes in This Patch
1. Updated `claude_desktop_config.json` to point to `dobbs_unified`
2. Added comprehensive test suite in `tests/test_unified_server_config.py`
3. Proper documentation following development standards

## Testing Instructions

### 1. Clone and checkout the branch
```bash
git clone https://github.com/SSBLA01/00-MCP-MASTER-CONTROL.git
cd 00-MCP-MASTER-CONTROL
git checkout fix/unified-server-config
```

### 2. Install dependencies
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Set up environment variables
Copy `.env.example` to `.env` and fill in your API keys:
```bash
cp .env.example .env
# Edit .env with your API keys
```

### 4. Run the test suite
```bash
python tests/test_unified_server_config.py
```

### 5. Apply the configuration
```bash
cp claude_desktop_config.json ~/Library/Application\ Support/Claude/
```

### 6. Restart Claude Desktop
Completely quit and restart Claude Desktop for the changes to take effect.

## Expected Results
- The test suite should show all tests passing
- Claude Desktop should recognize "Dobbs-Unified" as an available MCP server
- All tools (file operations, GitHub, visualization, etc.) should be accessible

## Rollback Plan
If issues occur, restore the previous configuration:
```bash
git checkout main -- claude_desktop_config.json
cp claude_desktop_config.json ~/Library/Application\ Support/Claude/
```

## Related Documentation
- See Obsidian note: "MCP Unified Server Issue - 2025-07-14"
- GitHub Issue: (to be created after testing)

## Next Steps
1. Run the test suite
2. Verify the fix works
3. Create pull request for code review
4. Merge to main after approval
5. Update production documentation
