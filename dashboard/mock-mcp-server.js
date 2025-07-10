// Mock MCP Server for Testing
// This simulates the MCP server responses without needing the Python backend

const http = require('http');

const server = http.createServer((req, res) => {
  console.log(`Mock MCP: ${req.method} ${req.url}`);
  
  res.setHeader('Content-Type', 'application/json');
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  
  if (req.method === 'OPTIONS') {
    res.statusCode = 204;
    res.end();
    return;
  }
  
  let body = '';
  req.on('data', chunk => body += chunk);
  req.on('end', () => {
    try {
      const data = body ? JSON.parse(body) : {};
      
      // Simulate different MCP actions
      let response = {
        success: true,
        timestamp: new Date().toISOString()
      };
      
      switch (data.action) {
        case 'search_perplexity':
          response.data = {
            results: `Found 5 papers about "${data.data.query}":\n1. Gyrovector Spaces and Their Applications\n2. Hyperbolic Geometry in Modern Mathematics\n3. Applications of Mobius Transformations`
          };
          break;
          
        case 'search_file_system':
          response.files = [
            `📁 ${data.data.path}/Research`,
            `  📄 ${data.data.query}_paper.pdf`,
            `  📄 ${data.data.query}_notes.md`,
            `  📁 ${data.data.query}_data`,
            `    📄 results.csv`
          ];
          break;
          
        case 'save_to_obsidian':
          response.data = {
            message: 'Note saved successfully',
            noteId: `${Date.now()}_${data.data.title}`,
            path: `/Obsidian/03_Concepts/${data.data.title}.md`
          };
          break;
          
        case 'send_to_claude':
          response.data = {
            message: `Message sent to ${data.data.target}`,
            processed: true,
            mcpMessage: {
              tool: data.data.target === 'Claude Desktop' ? 'claude_desktop_input' : 'claude_code_input',
              arguments: { text: data.data.text }
            }
          };
          break;
          
        case 'get_system_status':
          response.data = {
            cpu: Math.floor(Math.random() * 30 + 40),
            memory: Math.floor(Math.random() * 20 + 60),
            disk: 78,
            mcp_connected: true,
            tools_available: 27
          };
          response.status = 'ok';
          break;
          
        default:
          response.success = false;
          response.error = `Unknown action: ${data.action}`;
          response.status = 'error';
      }
      
      res.statusCode = 200;
      res.end(JSON.stringify(response));
      
    } catch (error) {
      res.statusCode = 500;
      res.end(JSON.stringify({
        success: false,
        error: error.message
      }));
    }
  });
});

const PORT = 3001;
server.listen(PORT, () => {
  console.log(`🤖 Mock MCP Server running on http://localhost:${PORT}`);
  console.log('This server simulates MCP responses for testing');
});