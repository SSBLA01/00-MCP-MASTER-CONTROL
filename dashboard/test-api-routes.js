const http = require('http');

// Configuration
const API_BASE_URL = 'http://localhost:3000/api/mcp';

// Test API Routes
async function testAPIRoutes() {
  console.log('\n🔌 Testing API Routes...\n');
  
  const results = {
    passed: 0,
    failed: 0,
    tests: []
  };

  // Helper to make API requests
  async function makeRequest(method, path, data = null) {
    return new Promise((resolve, reject) => {
      const url = new URL(path, API_BASE_URL);
      const options = {
        method: method,
        headers: {
          'Content-Type': 'application/json',
        }
      };

      const req = http.request(url, options, (res) => {
        let body = '';
        res.on('data', chunk => body += chunk);
        res.on('end', () => {
          try {
            const json = JSON.parse(body);
            resolve({ status: res.statusCode, data: json });
          } catch (e) {
            resolve({ status: res.statusCode, data: body });
          }
        });
      });

      req.on('error', reject);
      
      if (data) {
        req.write(JSON.stringify(data));
      }
      
      req.end();
    });
  }

  // Test helper
  function logTest(name, passed, error = null) {
    const status = passed ? '✅ PASS' : '❌ FAIL';
    console.log(`${status}: ${name}`);
    if (error) console.log(`   Error: ${error}`);
    results.tests.push({ name, passed, error });
    if (passed) results.passed++;
    else results.failed++;
  }

  // Test 1: Health Check (GET)
  try {
    const response = await makeRequest('GET', '/api/mcp');
    const passed = response.status === 200 && 
                   response.data.status === 'ok' &&
                   response.data.mcp_server === 'Dobbs-MCP';
    logTest('GET /api/mcp - Health check', passed);
  } catch (error) {
    logTest('GET /api/mcp - Health check', false, error.message);
  }

  // Test 2: Search Perplexity
  try {
    const response = await makeRequest('POST', '/api/mcp', {
      action: 'search_perplexity',
      data: { query: 'test query' },
      timestamp: new Date().toISOString()
    });
    const passed = response.status === 200 && response.data.success !== undefined;
    logTest('POST /api/mcp - Search Perplexity', passed);
  } catch (error) {
    logTest('POST /api/mcp - Search Perplexity', false, error.message);
  }

  // Test 3: Search File System
  try {
    const response = await makeRequest('POST', '/api/mcp', {
      action: 'search_file_system',
      data: { path: '/test/path', query: 'test' },
      timestamp: new Date().toISOString()
    });
    const passed = response.status === 200 && 
                   response.data.success === true &&
                   Array.isArray(response.data.files);
    logTest('POST /api/mcp - Search File System', passed);
  } catch (error) {
    logTest('POST /api/mcp - Search File System', false, error.message);
  }

  // Test 4: Save to Obsidian
  try {
    const response = await makeRequest('POST', '/api/mcp', {
      action: 'save_to_obsidian',
      data: { 
        title: 'Test Note',
        content: 'Test content',
        category: 'test'
      },
      timestamp: new Date().toISOString()
    });
    const passed = response.status === 200 && response.data.success !== undefined;
    logTest('POST /api/mcp - Save to Obsidian', passed);
  } catch (error) {
    logTest('POST /api/mcp - Save to Obsidian', false, error.message);
  }

  // Test 5: Send to Claude
  try {
    const response = await makeRequest('POST', '/api/mcp', {
      action: 'send_to_claude',
      data: { 
        text: 'Test message',
        target: 'Claude Desktop'
      },
      timestamp: new Date().toISOString()
    });
    const passed = response.status === 200 && 
                   response.data.success === true &&
                   response.data.data.mcpMessage !== undefined;
    logTest('POST /api/mcp - Send to Claude', passed);
  } catch (error) {
    logTest('POST /api/mcp - Send to Claude', false, error.message);
  }

  // Test 6: Get System Status
  try {
    const response = await makeRequest('POST', '/api/mcp', {
      action: 'get_system_status',
      data: {},
      timestamp: new Date().toISOString()
    });
    const passed = response.status === 200 && 
                   response.data.success === true &&
                   response.data.data.cpu !== undefined;
    logTest('POST /api/mcp - Get System Status', passed);
  } catch (error) {
    logTest('POST /api/mcp - Get System Status', false, error.message);
  }

  // Test 7: Invalid Action
  try {
    const response = await makeRequest('POST', '/api/mcp', {
      action: 'invalid_action',
      data: {},
      timestamp: new Date().toISOString()
    });
    const passed = response.status === 200 && 
                   response.data.success === false &&
                   response.data.error.includes('Unknown action');
    logTest('POST /api/mcp - Invalid action handling', passed);
  } catch (error) {
    logTest('POST /api/mcp - Invalid action handling', false, error.message);
  }

  // Test 8: Missing Body
  try {
    const response = await makeRequest('POST', '/api/mcp');
    const passed = response.status === 500;
    logTest('POST /api/mcp - Missing body handling', passed);
  } catch (error) {
    logTest('POST /api/mcp - Missing body handling', false, error.message);
  }

  // Print summary
  console.log('\n' + '='.repeat(50));
  console.log('API TEST SUMMARY');
  console.log('='.repeat(50));
  console.log(`Total Tests: ${results.passed + results.failed}`);
  console.log(`✅ Passed: ${results.passed}`);
  console.log(`❌ Failed: ${results.failed}`);
  
  return results;
}

// Run tests
testAPIRoutes().catch(console.error);