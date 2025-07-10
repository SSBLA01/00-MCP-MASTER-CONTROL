import { NextRequest, NextResponse } from 'next/server'
import { spawn } from 'child_process'
import path from 'path'

interface MCPRequest {
  action: string
  data: any
  timestamp: string
}

interface MCPResponse {
  success: boolean
  data?: any
  error?: string
  files?: string[]
  status?: 'ok' | 'warning' | 'error'
}

// Path to the MCP Python server
const MCP_SERVER_PATH = path.join(process.cwd(), '..', 'src', 'servers', 'dobbs_unified.py')
const PYTHON_PATH = path.join(process.cwd(), '..', 'venv', 'bin', 'python')

export async function POST(request: NextRequest) {
  try {
    const body: MCPRequest = await request.json()
    console.log('MCP API received:', body)

    let response: MCPResponse = {
      success: true,
      status: 'ok'
    }

    switch (body.action) {
      case 'search_perplexity':
        response = await handlePerplexitySearch(body.data)
        break

      case 'search_file_system':
        response = await handleFileSystemSearch(body.data)
        break

      case 'save_to_obsidian':
        response = await handleSaveToObsidian(body.data)
        break

      case 'send_to_claude':
        response = await handleSendToClaude(body.data)
        break

      case 'get_system_status':
        response = await handleSystemStatus()
        break

      default:
        response = {
          success: false,
          error: `Unknown action: ${body.action}`,
          status: 'error'
        }
    }

    return NextResponse.json(response)
  } catch (error) {
    console.error('MCP API error:', error)
    return NextResponse.json({
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error',
      status: 'error'
    }, { status: 500 })
  }
}

async function handlePerplexitySearch(data: any): Promise<MCPResponse> {
  return new Promise((resolve) => {
    const args = [
      '-m', 'src.servers.dobbs_unified',
      '--action', 'search_academic',
      '--query', data.query
    ]

    const process = spawn(PYTHON_PATH, args, {
      cwd: path.join(process.cwd(), '..'),
      env: { ...process.env, PYTHONPATH: path.join(process.cwd(), '..') }
    })

    let output = ''
    let error = ''

    process.stdout.on('data', (data) => {
      output += data.toString()
    })

    process.stderr.on('data', (data) => {
      error += data.toString()
    })

    process.on('close', (code) => {
      if (code === 0) {
        resolve({
          success: true,
          data: { results: output },
          status: 'ok'
        })
      } else {
        resolve({
          success: false,
          error: error || 'Search failed',
          status: 'error'
        })
      }
    })

    // Timeout after 30 seconds
    setTimeout(() => {
      process.kill()
      resolve({
        success: false,
        error: 'Search timeout',
        status: 'error'
      })
    }, 30000)
  })
}

async function handleFileSystemSearch(data: any): Promise<MCPResponse> {
  // Simulate file search in Dropbox
  const mockFiles = [
    `📁 ${data.path}/Research`,
    `  📄 paper_${data.query || 'default'}.pdf`,
    `  📄 notes_${data.query || 'default'}.md`,
    `📁 ${data.path}/Projects`,
    `  📁 mathematical-research-mcp`,
    `    📄 README.md`,
    `    📄 ${data.query || 'search'}_results.txt`
  ]

  return {
    success: true,
    files: mockFiles,
    data: {
      searchPath: data.path,
      query: data.query,
      resultsCount: mockFiles.length
    },
    status: 'ok'
  }
}

async function handleSaveToObsidian(data: any): Promise<MCPResponse> {
  return new Promise((resolve) => {
    const args = [
      '-m', 'src.servers.dobbs_unified',
      '--action', 'create_atomic_note',
      '--title', data.title,
      '--content', data.content,
      '--category', data.category || 'concepts'
    ]

    const process = spawn(PYTHON_PATH, args, {
      cwd: path.join(process.cwd(), '..'),
      env: { ...process.env, PYTHONPATH: path.join(process.cwd(), '..') }
    })

    let output = ''
    let error = ''

    process.stdout.on('data', (data) => {
      output += data.toString()
    })

    process.stderr.on('data', (data) => {
      error += data.toString()
    })

    process.on('close', (code) => {
      if (code === 0) {
        resolve({
          success: true,
          data: {
            message: 'Note saved to Obsidian',
            noteId: data.title,
            timestamp: new Date().toISOString()
          },
          status: 'ok'
        })
      } else {
        resolve({
          success: false,
          error: error || 'Failed to save to Obsidian',
          status: 'error'
        })
      }
    })
  })
}

async function handleSendToClaude(data: any): Promise<MCPResponse> {
  // Format the message for MCP protocol
  const mcpMessage = {
    tool: data.target === 'Claude Desktop' ? 'claude_desktop_input' : 'claude_code_input',
    arguments: {
      text: data.text,
      timestamp: new Date().toISOString()
    }
  }

  console.log('Sending to Claude:', mcpMessage)

  // In a real implementation, this would communicate with the MCP server
  // For now, we'll simulate success
  return {
    success: true,
    data: {
      message: `Sent to ${data.target}`,
      text: data.text,
      mcpMessage: mcpMessage
    },
    status: 'ok'
  }
}

async function handleSystemStatus(): Promise<MCPResponse> {
  // Get actual system stats or simulate them
  const stats = {
    cpu: Math.floor(Math.random() * 30 + 40),
    memory: Math.floor(Math.random() * 20 + 60),
    disk: 78 + Math.floor(Math.random() * 5),
    mcp_connected: true,
    tools_available: 27,
    active_sessions: 1
  }

  return {
    success: true,
    data: stats,
    status: stats.cpu > 80 || stats.memory > 80 ? 'warning' : 'ok'
  }
}

export async function GET(request: NextRequest) {
  // Health check endpoint
  return NextResponse.json({
    status: 'ok',
    mcp_server: 'Dobbs-MCP',
    version: '1.0.0',
    tools: 27,
    timestamp: new Date().toISOString()
  })
}