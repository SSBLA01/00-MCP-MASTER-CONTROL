# MCP Dashboard Testing Guide

This document explains how to test the MCP Dashboard integration with Claude Desktop and Claude Code.

## Quick Start

To run all tests:

```bash
cd dashboard
./run-tests.sh
```

This will:
1. Install dependencies
2. Build the Next.js app
3. Start the development server
4. Run all integration tests
5. Generate test reports

## Test Coverage

### UI Integration Tests (`test-mcp-integration.js`)

Tests all dashboard functionality:

1. **Search Perplexity Button**
   - Verifies button visibility and click functionality
   - Checks that MCP messages are sent correctly
   - Validates output log updates

2. **Search File System Button**
   - Tests Dropbox file search integration
   - Verifies proper query handling

3. **Save to Obsidian Button**
   - Tests note creation workflow
   - Validates atomic note ID generation

4. **Claude Desktop/Code Toggle**
   - Tests mode switching between Desktop and Code
   - Verifies UI updates correctly

5. **Send to Claude Desktop**
   - Tests message formatting for Claude Desktop
   - Validates MCP protocol compliance

6. **Send to Claude Code**
   - Tests message formatting for Claude Code
   - Ensures proper target switching

7. **Keyboard Shortcuts**
   - Tests Cmd/Ctrl + Enter functionality
   - Verifies shortcut message sending

8. **View Switching**
   - Tests Code/Files/Logs view toggling
   - Validates content display for each view

9. **Status Indicator**
   - Verifies status light functionality
   - Tests green/yellow/red states

10. **Settings Dropdown**
    - Tests dark mode toggle
    - Verifies font size/family options

11. **Tab Navigation**
    - Tests Research/Visualization/Knowledge/Publish tabs
    - Validates active state tracking

12. **System Resource Meters**
    - Tests CPU/Memory/Disk display
    - Validates animated progress bars

### API Route Tests (`test-api-routes.js`)

Tests all API endpoints:

1. **GET /api/mcp** - Health check
2. **POST /api/mcp** - All MCP actions:
   - search_perplexity
   - search_file_system
   - save_to_obsidian
   - send_to_claude
   - get_system_status
3. **Error Handling** - Invalid actions and missing data

## Test Output

After running tests, you'll find:

- `test-report.txt` - Human-readable test results
- `test-results.json` - Machine-readable results
- `dev-server.log` - Server output for debugging

## Manual Testing

### Testing with Real MCP Server

1. Ensure Python MCP server is running:
   ```bash
   cd ..
   ./run_dobbs_mcp.sh
   ```

2. Update API route to use real server (uncomment spawn commands in `route.ts`)

3. Start dashboard:
   ```bash
   npm run dev
   ```

4. Test each button manually

### Testing Claude Integration

1. Open Claude Desktop
2. Type in dashboard input field
3. Toggle between Desktop/Code modes
4. Click Send or press Cmd/Ctrl+Enter
5. Verify message appears in Claude

## Mock MCP Server

For isolated testing without Python backend:

```bash
node mock-mcp-server.js
```

This starts a mock server on port 3001 that simulates MCP responses.

## Troubleshooting

### Tests Failing

1. Check if port 3000 is already in use
2. Ensure Node.js version >= 18
3. Check `dev-server.log` for startup errors
4. Verify all dependencies installed

### MCP Connection Issues

1. Check Python environment is activated
2. Verify paths in `.env` file
3. Check SSL certificates are valid
4. Review MCP server logs

### UI Not Updating

1. Clear browser cache
2. Check React Developer Tools
3. Verify WebSocket connections
4. Check browser console for errors

## CI/CD Integration

To run tests in CI:

```bash
export CI=true  # Run in headless mode
npm install
npm run build
npm test
```

## Performance Testing

Monitor dashboard performance:

1. Open Chrome DevTools
2. Go to Performance tab
3. Record while interacting with dashboard
4. Check for:
   - Frame drops
   - Long tasks
   - Memory leaks
   - Network delays