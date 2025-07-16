"use client"

import React, { useState, useEffect, useRef, useCallback } from 'react'
import { Button } from './ui/button'
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs'
import { Switch } from './ui/switch'
import { ResizableHandle } from './ResizableHandle'
import { NebulaVisualization } from './NebulaVisualization'
import { useMCPWebSocket } from '@/lib/websocket'
import { useObsidian } from '@/lib/obsidian'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuRadioGroup,
  DropdownMenuRadioItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from './ui/dropdown-menu'
import { 
  Search, 
  FolderTree, 
  Save, 
  Settings, 
  Moon, 
  Sun,
  FileCode2,
  FolderOpen,
  AlertCircle,
  Cpu,
  HardDrive,
  Activity,
  Monitor,
  Code,
  Send,
  X,
  Play,
  Wifi,
  WifiOff,
  RefreshCw,
  Command,
  Brain,
  Network
} from 'lucide-react'

interface SystemStats {
  cpu: number
  memory: number
  disk: number
}

interface ServiceNode {
  id: string
  name: string
  status: 'healthy' | 'warning' | 'error' | 'offline'
  connections: string[]
}

export default function EnhancedDashboard() {
  const [isDarkMode, setIsDarkMode] = useState(true)
  const [fontSize, setFontSize] = useState('medium')
  const [fontFamily, setFontFamily] = useState('sans')
  const [activeView, setActiveView] = useState<'code' | 'files' | 'logs'>('code')
  const [logStatus, setLogStatus] = useState<'ok' | 'warning' | 'error'>('ok')
  const [inputMode, setInputMode] = useState<'desktop' | 'code'>('desktop')
  const [inputText, setInputText] = useState('')
  const [outputLog, setOutputLog] = useState<string[]>([])
  const [fileTree, setFileTree] = useState<string[]>([])
  const [debugLogs, setDebugLogs] = useState<string[]>([])
  const [activeTab, setActiveTab] = useState<'research' | 'visualization' | 'knowledge' | 'publish'>('research')
  const [searchResults, setSearchResults] = useState<string>('')
  const [isLoading, setIsLoading] = useState(false)
  const [showVideo, setShowVideo] = useState(false)
  const [videoUrl, setVideoUrl] = useState('')
  const [leftSidebarWidth, setLeftSidebarWidth] = useState(80)
  const [rightSidebarWidth, setRightSidebarWidth] = useState(320)
  const [outputMonitorHeight, setOutputMonitorHeight] = useState(50)
  const [settingsChanged, setSettingsChanged] = useState(false)
  const [showCommandPalette, setShowCommandPalette] = useState(false)
  const [commandSearch, setCommandSearch] = useState('')
  const inputRef = useRef<HTMLTextAreaElement>(null)
  const containerRef = useRef<HTMLDivElement>(null)
  
  const [systemStats, setSystemStats] = useState<SystemStats>({
    cpu: 45,
    memory: 62,
    disk: 78
  })

  const [services, setServices] = useState<ServiceNode[]>([
    { id: 'mcp-core', name: 'MCP Core', status: 'healthy', connections: ['obsidian', 'github'] },
    { id: 'obsidian', name: 'Obsidian', status: 'healthy', connections: ['mcp-core'] },
    { id: 'github', name: 'GitHub', status: 'healthy', connections: ['mcp-core'] },
    { id: 'dropbox', name: 'Dropbox', status: 'healthy', connections: ['mcp-core', 'obsidian'] },
    { id: 'gemini', name: 'Gemini AI', status: 'healthy', connections: ['mcp-core'] },
    { id: 'manim', name: 'Manim', status: 'warning', connections: ['mcp-core'] },
  ])

  // WebSocket connection
  const { 
    isConnected, 
    connectionStatus, 
    sendMessage, 
    reconnect 
  } = useMCPWebSocket({
    url: process.env.NEXT_PUBLIC_MCP_WS_URL || 'ws://localhost:8080',
    onMessage: (data) => {
      handleMCPResponse(data)
    },
    onStatusChange: (status) => {
      setOutputLog(prev => [...prev, `[WebSocket] Status: ${status}`])
    }
  })

  // Obsidian integration
  const obsidian = useObsidian({
    vaultPath: '/Users/scottbroock/Dropbox/Knowledge',
    apiPort: 27124
  })

  // Command palette commands
  const commands = [
    { id: 'search-perplexity', name: 'Search Perplexity', icon: Search, action: handleSearchPerplexity },
    { id: 'search-files', name: 'Search File System', icon: FolderTree, action: handleSearchFileSystem },
    { id: 'save-obsidian', name: 'Save to Obsidian', icon: Save, action: handleSaveToObsidian },
    { id: 'create-daily-note', name: 'Create Daily Note', icon: FileCode2, action: () => createDailyNote() },
    { id: 'toggle-theme', name: 'Toggle Theme', icon: Moon, action: () => setIsDarkMode(!isDarkMode) },
    { id: 'reconnect-mcp', name: 'Reconnect to MCP', icon: RefreshCw, action: reconnect },
  ]

  const filteredCommands = commands.filter(cmd => 
    cmd.name.toLowerCase().includes(commandSearch.toLowerCase())
  )

  // Enhanced MCP communication
  const sendToMCP = async (message: any) => {
    const timestamp = new Date().toISOString()
    const mcpMessage = {
      id: Math.random().toString(36).substr(2, 9),
      ...message,
      timestamp
    }
    
    setOutputLog(prev => [...prev, `[${timestamp}] Sent: ${message.action}`])
    
    if (isConnected) {
      sendMessage(mcpMessage)
    } else {
      // Fallback to HTTP API
      try {
        const response = await fetch('/api/mcp', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(mcpMessage)
        })
        
        if (response.ok) {
          const data = await response.json()
          handleMCPResponse(data)
        }
      } catch (error) {
        console.error('MCP communication error:', error)
        setDebugLogs(prev => [...prev, `Error: ${error}`])
        setLogStatus('error')
      }
    }
  }

  const handleMCPResponse = (data: any) => {
    console.log('MCP Response:', data)
    
    if (data.files) {
      setFileTree(data.files)
    }
    
    if (data.status) {
      setLogStatus(data.status)
    }
    
    if (data.data?.results) {
      setSearchResults(data.data.results)
    }
    
    if (data.data?.videoPath) {
      setVideoUrl(data.data.videoPath)
      setShowVideo(true)
    }
    
    if (data.services) {
      updateServiceStatus(data.services)
    }
    
    setIsLoading(false)
  }

  const updateServiceStatus = (serviceUpdates: any) => {
    setServices(prev => prev.map(service => {
      const update = serviceUpdates[service.id]
      if (update) {
        return { ...service, status: update.status }
      }
      return service
    }))
  }

  // Button Actions
  const handleSearchPerplexity = () => {
    setIsLoading(true)
    setActiveTab('research')
    setSearchResults('Searching Perplexity for: ' + (inputText || 'mathematical research') + '...')
    sendToMCP({
      action: 'search_perplexity',
      data: { query: inputText || 'mathematical research' }
    })
  }

  const handleSearchFileSystem = () => {
    setIsLoading(true)
    setActiveTab('knowledge')
    setSearchResults('Searching file system for: ' + inputText + '...')
    sendToMCP({
      action: 'search_file_system',
      data: { path: '/Users/scottbroock/Dropbox', query: inputText }
    })
  }

  const handleSaveToObsidian = async () => {
    setIsLoading(true)
    setActiveTab('knowledge')
    
    const noteTitle = `Note_${new Date().getTime()}`
    const result = await obsidian.createNote({
      title: noteTitle,
      content: inputText,
      tags: ['mcp-dashboard', 'auto-generated'],
      folder: 'MCP_Notes'
    })
    
    if (result) {
      setSearchResults(`Successfully saved to Obsidian: ${noteTitle}`)
    } else {
      setSearchResults(`Failed to save to Obsidian: ${obsidian.error}`)
    }
    
    setIsLoading(false)
  }

  const createDailyNote = async () => {
    const content = `# Daily Note - ${new Date().toLocaleDateString()}\n\n## MCP Activity\n\n${outputLog.slice(-10).join('\n')}`
    const result = await obsidian.createDailyNote(content)
    
    if (result) {
      setOutputLog(prev => [...prev, '> Created daily note in Obsidian'])
    }
  }

  const handleSendInput = () => {
    if (!inputText.trim()) return
    
    const target = inputMode === 'desktop' ? 'Claude Desktop' : 'Claude Code'
    sendToMCP({
      action: 'send_to_claude',
      data: { 
        text: inputText,
        target: target
      }
    })
    
    setOutputLog(prev => [...prev, `> Sent to ${target}: ${inputText}`])
    setInputText('')
  }

  const handleNodeClick = (node: ServiceNode) => {
    setOutputLog(prev => [...prev, `> Service clicked: ${node.name} (${node.status})`])
  }

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault()
        setShowCommandPalette(!showCommandPalette)
      }
    }

    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [showCommandPalette])

  // System stats simulation
  useEffect(() => {
    const interval = setInterval(() => {
      setSystemStats({
        cpu: Math.floor(Math.random() * 30 + 40),
        memory: Math.floor(Math.random() * 20 + 60),
        disk: 78 + Math.floor(Math.random() * 5)
      })
    }, 3000)

    return () => clearInterval(interval)
  }, [])

  // Resize handlers (same as before)
  const handleLeftResize = useCallback((e: React.MouseEvent) => {
    e.preventDefault()
    const startX = e.pageX
    const startWidth = leftSidebarWidth

    const handleMouseMove = (e: MouseEvent) => {
      const delta = e.pageX - startX
      const newWidth = Math.max(60, Math.min(200, startWidth + delta))
      setLeftSidebarWidth(newWidth)
    }

    const handleMouseUp = () => {
      document.removeEventListener('mousemove', handleMouseMove)
      document.removeEventListener('mouseup', handleMouseUp)
    }

    document.addEventListener('mousemove', handleMouseMove)
    document.addEventListener('mouseup', handleMouseUp)
  }, [leftSidebarWidth])

  const handleRightResize = useCallback((e: React.MouseEvent) => {
    e.preventDefault()
    const startX = e.pageX
    const startWidth = rightSidebarWidth

    const handleMouseMove = (e: MouseEvent) => {
      const delta = startX - e.pageX
      const newWidth = Math.max(240, Math.min(480, startWidth + delta))
      setRightSidebarWidth(newWidth)
    }

    const handleMouseUp = () => {
      document.removeEventListener('mousemove', handleMouseMove)
      document.removeEventListener('mouseup', handleMouseUp)
    }

    document.addEventListener('mousemove', handleMouseMove)
    document.addEventListener('mouseup', handleMouseUp)
  }, [rightSidebarWidth])

  const handleOutputResize = useCallback((e: React.MouseEvent) => {
    e.preventDefault()
    const startY = e.pageY
    const startHeight = outputMonitorHeight

    const handleMouseMove = (e: MouseEvent) => {
      if (!containerRef.current) return
      const containerHeight = containerRef.current.getBoundingClientRect().height
      const delta = ((startY - e.pageY) / containerHeight) * 100
      const newHeight = Math.max(20, Math.min(80, startHeight + delta))
      setOutputMonitorHeight(newHeight)
    }

    const handleMouseUp = () => {
      document.removeEventListener('mousemove', handleMouseMove)
      document.removeEventListener('mouseup', handleMouseUp)
    }

    document.addEventListener('mousemove', handleMouseMove)
    document.addEventListener('mouseup', handleMouseUp)
  }, [outputMonitorHeight])

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'error': return 'bg-red-500'
      case 'warning': return 'bg-yellow-500'
      default: return 'bg-green-500'
    }
  }

  const StatBar = ({ label, value, icon }: { label: string; value: number; icon: React.ReactNode }) => (
    <div className="flex items-center space-x-2 mb-2">
      <div className="w-8">{icon}</div>
      <div className="flex-1">
        <div className="flex justify-between text-xs mb-1">
          <span>{label}</span>
          <span>{value}%</span>
        </div>
        <div className="w-full bg-gray-700 rounded-full h-2">
          <div 
            className="bg-gradient-to-r from-cyan-500 to-blue-500 h-2 rounded-full transition-all duration-500"
            style={{ width: `${value}%` }}
          />
        </div>
      </div>
    </div>
  )

  const getFontSizeClass = () => {
    switch (fontSize) {
      case 'small': return 'text-xs'
      case 'large': return 'text-xl'
      default: return 'text-base'
    }
  }

  const getFontFamilyClass = () => {
    switch (fontFamily) {
      case 'serif': return 'font-serif'
      case 'mono': return 'font-mono'
      default: return 'font-sans'
    }
  }

  return (
    <div className={`${isDarkMode ? 'dark' : ''} min-h-screen bg-background text-foreground ${getFontSizeClass()} ${getFontFamilyClass()}`}>
      <div className="flex flex-col h-screen">
        {/* Header */}
        <div className="border-b border-border bg-card">
          <div className="flex items-center justify-between px-4 py-2">
            <div className="flex items-center space-x-4">
              <h1 className="text-xl font-bold bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">
                Dobbs MCP Dashboard
              </h1>
              
              {/* Connection Status */}
              <div className="flex items-center space-x-2">
                {isConnected ? (
                  <Wifi className="h-4 w-4 text-green-400" />
                ) : (
                  <WifiOff className="h-4 w-4 text-red-400" />
                )}
                <span className={`text-sm ${isConnected ? 'text-green-400' : 'text-red-400'}`}>
                  {connectionStatus}
                </span>
              </div>
            </div>
            
            <div className="flex items-center space-x-2">
              {/* Command Palette Button */}
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setShowCommandPalette(!showCommandPalette)}
                className="flex items-center space-x-2"
              >
                <Command className="h-4 w-4" />
                <span className="text-xs">⌘K</span>
              </Button>
              
              {/* Settings Dropdown */}
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="ghost" size="icon">
                    <Settings className="h-5 w-5" />
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end" className="w-56">
                  <DropdownMenuLabel>Appearance</DropdownMenuLabel>
                  <DropdownMenuSeparator />
                  
                  <div className="flex items-center justify-between px-2 py-2">
                    <div className="flex items-center space-x-2">
                      <Sun className="h-4 w-4" />
                      <span className="text-sm">Dark Mode</span>
                      <Moon className="h-4 w-4" />
                    </div>
                    <Switch
                      checked={isDarkMode}
                      onCheckedChange={(checked) => {
                        setIsDarkMode(checked)
                        setSettingsChanged(true)
                        setTimeout(() => setSettingsChanged(false), 2000)
                      }}
                    />
                  </div>
                  
                  <DropdownMenuSeparator />
                  <DropdownMenuLabel>Font Size</DropdownMenuLabel>
                  <DropdownMenuRadioGroup value={fontSize} onValueChange={(value) => {
                    setFontSize(value)
                    setSettingsChanged(true)
                    setTimeout(() => setSettingsChanged(false), 2000)
                  }}>
                    <DropdownMenuRadioItem value="small">Small</DropdownMenuRadioItem>
                    <DropdownMenuRadioItem value="medium">Medium</DropdownMenuRadioItem>
                    <DropdownMenuRadioItem value="large">Large</DropdownMenuRadioItem>
                  </DropdownMenuRadioGroup>
                  
                  <DropdownMenuSeparator />
                  <DropdownMenuLabel>Font Family</DropdownMenuLabel>
                  <DropdownMenuRadioGroup value={fontFamily} onValueChange={(value) => {
                    setFontFamily(value)
                    setSettingsChanged(true)
                    setTimeout(() => setSettingsChanged(false), 2000)
                  }}>
                    <DropdownMenuRadioItem value="sans">Sans-serif</DropdownMenuRadioItem>
                    <DropdownMenuRadioItem value="serif">Serif</DropdownMenuRadioItem>
                    <DropdownMenuRadioItem value="mono">Monospace</DropdownMenuRadioItem>
                  </DropdownMenuRadioGroup>
                </DropdownMenuContent>
              </DropdownMenu>
            </div>
          </div>
        </div>

        {/* Command Palette */}
        {showCommandPalette && (
          <div className="absolute inset-0 bg-black/50 z-50 flex items-start justify-center pt-20">
            <div className="bg-card border border-border rounded-lg shadow-2xl w-full max-w-2xl">
              <input
                type="text"
                value={commandSearch}
                onChange={(e) => setCommandSearch(e.target.value)}
                placeholder="Type a command..."
                className="w-full px-4 py-3 bg-transparent border-b border-border focus:outline-none"
                autoFocus
              />
              <div className="max-h-96 overflow-y-auto">
                {filteredCommands.map(cmd => (
                  <button
                    key={cmd.id}
                    onClick={() => {
                      cmd.action()
                      setShowCommandPalette(false)
                      setCommandSearch('')
                    }}
                    className="w-full px-4 py-3 flex items-center space-x-3 hover:bg-gray-800 transition-colors"
                  >
                    <cmd.icon className="h-4 w-4 text-cyan-400" />
                    <span>{cmd.name}</span>
                  </button>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Main Content Area */}
        <div className="flex flex-1 overflow-hidden" ref={containerRef}>
          {/* Left Sidebar - Quick Actions */}
          <div className="border-r border-border bg-card p-2 flex flex-col space-y-2" style={{ width: `${leftSidebarWidth}px` }}>
            <Button 
              variant="ghost" 
              size="icon"
              className="w-full h-16 flex flex-col items-center justify-center text-cyan-400 hover:text-cyan-300 hover:bg-gray-800"
              onClick={handleSearchPerplexity}
              title="Search Perplexity"
            >
              <Search className="h-6 w-6 mb-1" />
              {leftSidebarWidth > 100 && <span className="text-xs">Search</span>}
            </Button>
            
            <Button 
              variant="ghost" 
              size="icon"
              className="w-full h-16 flex flex-col items-center justify-center text-cyan-400 hover:text-cyan-300 hover:bg-gray-800"
              onClick={handleSearchFileSystem}
              title="Search File System"
            >
              <FolderTree className="h-6 w-6 mb-1" />
              {leftSidebarWidth > 100 && <span className="text-xs">Files</span>}
            </Button>
            
            <Button 
              variant="ghost" 
              size="icon"
              className="w-full h-16 flex flex-col items-center justify-center text-cyan-400 hover:text-cyan-300 hover:bg-gray-800"
              onClick={handleSaveToObsidian}
              title="Save to Obsidian"
            >
              <Save className="h-6 w-6 mb-1" />
              {leftSidebarWidth > 100 && <span className="text-xs">Save</span>}
            </Button>
            
            <Button 
              variant="ghost" 
              size="icon"
              className="w-full h-16 flex flex-col items-center justify-center text-purple-400 hover:text-purple-300 hover:bg-gray-800"
              onClick={() => setActiveTab('visualization')}
              title="Service Network"
            >
              <Network className="h-6 w-6 mb-1" />
              {leftSidebarWidth > 100 && <span className="text-xs">Network</span>}
            </Button>
          </div>

          {/* Left Resize Handle */}
          <ResizableHandle orientation="horizontal" onMouseDown={handleLeftResize} />

          {/* Center Content - Tab Based */}
          <div className="flex-1 flex flex-col bg-gray-900">
            {/* Tab Content */}
            <Tabs value={activeTab} onValueChange={(v) => setActiveTab(v as any)} className="flex-1 flex flex-col">
              <TabsList className="bg-secondary m-4">
                <TabsTrigger value="research">Research</TabsTrigger>
                <TabsTrigger value="visualization">Visualization</TabsTrigger>
                <TabsTrigger value="knowledge">Knowledge</TabsTrigger>
                <TabsTrigger value="publish">Publish</TabsTrigger>
              </TabsList>
              
              <div className="flex-1 relative">
                <TabsContent value="research" className="h-full m-0 data-[state=active]:flex data-[state=active]:flex-col">
                  <div className="flex-1 bg-gray-800 rounded-lg border border-cyan-500/30 shadow-2xl shadow-cyan-500/20 m-4 p-8 overflow-auto">
                    {isLoading ? (
                      <div className="text-cyan-400 animate-pulse">Loading...</div>
                    ) : searchResults ? (
                      <div className="text-white whitespace-pre-wrap">{searchResults}</div>
                    ) : (
                      <div>
                        <h2 className="text-2xl font-bold text-cyan-400 mb-4">Research Results</h2>
                        <p className="text-gray-400">Search results will appear here. Use the search button or type a query below.</p>
                      </div>
                    )}
                  </div>
                </TabsContent>
                
                <TabsContent value="visualization" className="h-full m-0 data-[state=active]:flex data-[state=active]:flex-col">
                  <div className="flex-1 bg-gray-800 rounded-lg border border-cyan-500/30 shadow-2xl shadow-cyan-500/20 m-4 p-8 flex items-center justify-center">
                    <NebulaVisualization services={services} onNodeClick={handleNodeClick} />
                  </div>
                </TabsContent>
                
                <TabsContent value="knowledge" className="h-full m-0 data-[state=active]:flex data-[state=active]:flex-col">
                  <div className="flex-1 bg-gray-800 rounded-lg border border-cyan-500/30 shadow-2xl shadow-cyan-500/20 m-4 p-8 overflow-auto">
                    {isLoading ? (
                      <div className="text-cyan-400 animate-pulse">Processing...</div>
                    ) : searchResults && activeTab === 'knowledge' ? (
                      <div className="text-white whitespace-pre-wrap">{searchResults}</div>
                    ) : (
                      <div>
                        <h2 className="text-2xl font-bold text-cyan-400 mb-4">Knowledge Management</h2>
                        <p className="text-gray-400">File search results and Obsidian notes will appear here.</p>
                        
                        {obsidian.error && (
                          <div className="mt-4 p-4 bg-red-500/20 border border-red-500/50 rounded-lg">
                            <p className="text-red-400">Obsidian Error: {obsidian.error}</p>
                          </div>
                        )}
                        
                        {fileTree.length > 0 && (
                          <div className="mt-6">
                            <h3 className="text-lg font-semibold text-cyan-400 mb-2">File Tree</h3>
                            <div className="font-mono text-sm">
                              {fileTree.map((file, i) => (
                                <p key={i} className="text-gray-400">{file}</p>
                              ))}
                            </div>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                </TabsContent>
                
                <TabsContent value="publish" className="h-full m-0 data-[state=active]:flex data-[state=active]:flex-col">
                  <div className="flex-1 bg-gray-800 rounded-lg border border-cyan-500/30 shadow-2xl shadow-cyan-500/20 m-4 p-8">
                    <h2 className="text-2xl font-bold text-cyan-400 mb-4">Publish & Export</h2>
                    <p className="text-gray-400">Document compilation and publishing tools.</p>
                  </div>
                </TabsContent>
                
                {/* Video Overlay */}
                {showVideo && (
                  <div className="absolute inset-0 bg-black/90 flex items-center justify-center z-50">
                    <div className="relative w-full max-w-4xl">
                      <Button
                        variant="ghost"
                        size="icon"
                        className="absolute top-4 right-4 text-white hover:bg-white/20"
                        onClick={() => setShowVideo(false)}
                      >
                        <X className="h-6 w-6" />
                      </Button>
                      <video
                        src={videoUrl}
                        controls
                        autoPlay
                        className="w-full rounded-lg"
                      />
                    </div>
                  </div>
                )}
              </div>
            </Tabs>
            
            {/* Input Area at Bottom */}
            <div className="bg-gray-800 border-t border-cyan-500/30 p-4">
              <div className="flex items-center space-x-2">
                {/* Mode Toggle Button */}
                <Button
                  variant={inputMode === 'desktop' ? 'default' : 'secondary'}
                  size="sm"
                  onClick={() => setInputMode(inputMode === 'desktop' ? 'code' : 'desktop')}
                  className="flex items-center space-x-2"
                >
                  {inputMode === 'desktop' ? <Monitor className="h-4 w-4" /> : <Code className="h-4 w-4" />}
                  <span>{inputMode === 'desktop' ? 'Claude Desktop' : 'Claude Code'}</span>
                </Button>
                
                {/* Text Input */}
                <textarea
                  ref={inputRef}
                  value={inputText}
                  onChange={(e) => setInputText(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) {
                      handleSendInput()
                    }
                  }}
                  placeholder={`Type here to send to ${inputMode === 'desktop' ? 'Claude Desktop' : 'Claude Code'}...`}
                  className="flex-1 bg-gray-700 text-white px-4 py-2 rounded-md resize-none focus:outline-none focus:ring-2 focus:ring-cyan-500"
                  rows={2}
                />
                
                {/* Send Button */}
                <Button
                  onClick={handleSendInput}
                  size="icon"
                  className="bg-gradient-to-r from-cyan-500 to-blue-500 hover:from-cyan-600 hover:to-blue-600"
                >
                  <Send className="h-4 w-4" />
                </Button>
              </div>
              <p className="text-xs text-gray-500 mt-2">Press Cmd/Ctrl + Enter to send • Cmd/Ctrl + K for commands</p>
            </div>
          </div>

          {/* Right Resize Handle */}
          <ResizableHandle orientation="horizontal" onMouseDown={handleRightResize} />

          {/* Right Sidebar */}
          <div className="border-l border-border bg-card" style={{ width: `${rightSidebarWidth}px` }}>
            {/* Output Monitor */}
            <div className="border-b border-border p-4" style={{ height: `${outputMonitorHeight}%` }}>
              <h3 className="text-sm font-semibold text-muted-foreground mb-4">Output Monitor</h3>
              
              <div className="bg-gray-800 rounded-lg p-4 h-[calc(100%-4rem)] overflow-auto">
                {activeView === 'code' && (
                  <div className="font-mono text-sm text-cyan-400">
                    {outputLog.length === 0 ? (
                      <>
                        <p>&gt; MCP Server {isConnected ? 'Connected' : 'Disconnected'}</p>
                        <p>&gt; 27 tools available</p>
                        <p>&gt; Ready for commands...</p>
                      </>
                    ) : (
                      outputLog.map((log, i) => <p key={i}>{log}</p>)
                    )}
                  </div>
                )}
                
                {activeView === 'files' && (
                  <div className="text-sm">
                    {fileTree.map((file, i) => (
                      <p key={i} className="text-gray-400">{file}</p>
                    ))}
                  </div>
                )}
                
                {activeView === 'logs' && (
                  <div className="font-mono text-xs">
                    <p className="text-gray-400">[{new Date().toLocaleTimeString()}] System operational</p>
                    {debugLogs.map((log, i) => (
                      <p key={i} className={log.includes('ERROR') ? 'text-red-400' : log.includes('WARN') ? 'text-yellow-400' : 'text-gray-400'}>
                        {log}
                      </p>
                    ))}
                  </div>
                )}
              </div>
              
              {/* View Selector */}
              <div className="flex justify-center space-x-4 mt-4">
                <button
                  onClick={() => setActiveView('code')}
                  className={`p-2 rounded-full transition-colors ${
                    activeView === 'code' ? 'bg-gradient-to-r from-cyan-500 to-blue-500 text-white' : 'bg-gray-700 text-gray-400'
                  }`}
                >
                  <FileCode2 className="h-4 w-4" />
                </button>
                <button
                  onClick={() => setActiveView('files')}
                  className={`p-2 rounded-full transition-colors ${
                    activeView === 'files' ? 'bg-gradient-to-r from-cyan-500 to-blue-500 text-white' : 'bg-gray-700 text-gray-400'
                  }`}
                >
                  <FolderOpen className="h-4 w-4" />
                </button>
                <button
                  onClick={() => setActiveView('logs')}
                  className={`p-2 rounded-full transition-colors relative ${
                    activeView === 'logs' ? 'bg-gradient-to-r from-cyan-500 to-blue-500 text-white' : 'bg-gray-700 text-gray-400'
                  }`}
                >
                  <AlertCircle className="h-4 w-4" />
                  <span className={`absolute -top-1 -right-1 h-2 w-2 rounded-full ${getStatusColor(logStatus)}`} />
                </button>
              </div>
            </div>

            {/* Output Resize Handle */}
            <ResizableHandle orientation="vertical" onMouseDown={handleOutputResize} />

            {/* System Stats */}
            <div className="flex-1 p-4" style={{ height: `${100 - outputMonitorHeight}%` }}>
              <h3 className="text-sm font-semibold text-muted-foreground mb-4">System Resources</h3>
              
              <div className="space-y-4">
                <StatBar 
                  label="CPU" 
                  value={systemStats.cpu} 
                  icon={<Cpu className="h-4 w-4 text-cyan-400" />}
                />
                <StatBar 
                  label="Memory" 
                  value={systemStats.memory} 
                  icon={<Activity className="h-4 w-4 text-cyan-400" />}
                />
                <StatBar 
                  label="Disk" 
                  value={systemStats.disk} 
                  icon={<HardDrive className="h-4 w-4 text-cyan-400" />}
                />
              </div>
              
              <div className="mt-6">
                <h3 className="text-sm font-semibold text-muted-foreground mb-2">AI Services</h3>
                <div className="space-y-2">
                  <div className="flex items-center justify-between text-xs">
                    <span className="flex items-center space-x-2">
                      <Brain className="h-3 w-3 text-purple-400" />
                      <span>Gemini AI</span>
                    </span>
                    <span className="text-green-400">Active</span>
                  </div>
                  <div className="flex items-center justify-between text-xs">
                    <span className="flex items-center space-x-2">
                      <Brain className="h-3 w-3 text-blue-400" />
                      <span>Kimi K2</span>
                    </span>
                    <span className="text-green-400">Active</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default EnhancedDashboard