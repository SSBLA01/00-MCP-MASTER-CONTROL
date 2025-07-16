# MCP Dashboard Setup Guide

## Enhanced Features

The enhanced MCP Dashboard now includes:

- **Real-time WebSocket Connection**: Live updates from the MCP server
- **Obsidian Integration**: Direct note creation and management
- **Nebula Visualization**: Beautiful service status network display
- **Command Palette**: Quick access to all functions (Cmd/Ctrl + K)
- **Enhanced UI**: Gradient effects, smooth animations, and modern design
- **Browser Launcher**: Simple HTML file for easy access from Brave

## Quick Start

### 1. Easy Launch from Brave Browser

Simply open the `dashboard/launch.html` file in Brave browser, or run:

```bash
chmod +x launch-dashboard-brave.sh
./launch-dashboard-brave.sh
```

### 2. Manual Setup

#### Install Dependencies
```bash
cd dashboard
npm install
```

#### Configure Environment
Create a `.env.local` file in the dashboard directory:

```env
NEXT_PUBLIC_MCP_WS_URL=ws://localhost:8080
NEXT_PUBLIC_OBSIDIAN_API_PORT=27124
NEXT_PUBLIC_OBSIDIAN_VAULT_PATH=/Users/scottbroock/Dropbox/Knowledge
```

#### Start the Dashboard
```bash
npm run dev
```

Open http://localhost:3000 in Brave browser.

## Architecture Overview

### WebSocket Integration
- Real-time bidirectional communication with MCP server
- Automatic reconnection with exponential backoff
- Status indicators for connection health

### Obsidian Integration
- HTTP API communication with Obsidian
- Create, update, and search notes
- Automatic daily note creation
- Tag and folder organization

### UI Components

1. **NebulaVisualization**: Interactive service network display
   - Animated nodes representing services
   - Connection pathways showing relationships
   - Color-coded status indicators

2. **Command Palette**: Quick command access
   - Keyboard shortcut: Cmd/Ctrl + K
   - Fuzzy search for commands
   - Extensible command system

3. **Enhanced Dashboard**: Main interface
   - WebSocket status indicator
   - Gradient UI elements
   - Smooth animations
   - Responsive layout

## Configuration

### MCP Server Connection
The dashboard expects the MCP server to expose a WebSocket endpoint at `ws://localhost:8080`. 

Ensure your MCP server includes:
```python
# Example WebSocket handler
async def handle_websocket(websocket, path):
    async for message in websocket:
        data = json.loads(message)
        # Process message and send response
        await websocket.send(json.dumps(response))
```

### Obsidian API Setup
Enable the Obsidian API plugin and configure it to listen on port 27124.

## Troubleshooting

### Dashboard won't connect to MCP server
1. Check if MCP server is running
2. Verify WebSocket URL in `.env.local`
3. Check browser console for errors

### Obsidian integration not working
1. Ensure Obsidian API plugin is enabled
2. Verify the API port matches your configuration
3. Check vault path is correct

### Brave browser won't open
1. Ensure Brave is installed
2. On macOS: Check if "Brave Browser" is the correct app name
3. On Linux: Verify `brave` or `brave-browser` command exists

## Development

### Adding New Commands
Add to the `commands` array in `EnhancedDashboard.tsx`:

```typescript
const commands = [
  {
    id: 'your-command',
    name: 'Your Command Name',
    icon: YourIcon,
    action: () => {
      // Your command logic
    }
  },
  // ... other commands
]
```

### Adding New Services
Update the `services` state in `EnhancedDashboard.tsx`:

```typescript
const [services, setServices] = useState<ServiceNode[]>([
  {
    id: 'new-service',
    name: 'New Service',
    status: 'healthy',
    connections: ['mcp-core']
  },
  // ... other services
])
```

### Customizing the Nebula Visualization
Modify `NebulaVisualization.tsx` to adjust:
- Node colors and sizes
- Animation speeds
- Connection styles
- Background effects

## API Endpoints

### Health Check
```
GET /api/health
```
Returns dashboard and service status.

### MCP Communication
```
POST /api/mcp
```
Sends commands to the MCP server.

## Keyboard Shortcuts

- `Cmd/Ctrl + K`: Open command palette
- `Cmd/Ctrl + Enter`: Send input to Claude
- `Cmd/Ctrl + S`: Save to Obsidian (when focused on input)

## Future Enhancements

- [ ] 3D visualization mode
- [ ] Voice command integration
- [ ] Mobile responsive design
- [ ] Plugin system for custom tools
- [ ] Export/import dashboard configurations