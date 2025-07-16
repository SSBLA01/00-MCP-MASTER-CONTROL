import { useEffect, useState, useRef, useCallback } from 'react'

export interface MCPMessage {
  id?: string
  action: string
  data: any
  timestamp: string
}

export interface MCPResponse {
  id?: string
  status: 'success' | 'error' | 'pending'
  data?: any
  error?: string
  timestamp: string
}

interface WebSocketConfig {
  url: string
  reconnectDelay?: number
  maxReconnectAttempts?: number
  onMessage?: (data: MCPResponse) => void
  onStatusChange?: (status: 'connected' | 'disconnected' | 'reconnecting') => void
}

export function useMCPWebSocket({
  url,
  reconnectDelay = 1000,
  maxReconnectAttempts = 10,
  onMessage,
  onStatusChange
}: WebSocketConfig) {
  const [isConnected, setIsConnected] = useState(false)
  const [connectionStatus, setConnectionStatus] = useState<'connected' | 'disconnected' | 'reconnecting'>('disconnected')
  const socketRef = useRef<WebSocket | null>(null)
  const reconnectAttemptsRef = useRef(0)
  const reconnectTimeoutRef = useRef<NodeJS.Timeout | null>(null)

  const connect = useCallback(() => {
    try {
      const ws = new WebSocket(url)
      
      ws.onopen = () => {
        console.log('Connected to MCP server')
        setIsConnected(true)
        setConnectionStatus('connected')
        reconnectAttemptsRef.current = 0
        onStatusChange?.('connected')
      }

      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data) as MCPResponse
          onMessage?.(data)
        } catch (error) {
          console.error('Failed to parse WebSocket message:', error)
        }
      }

      ws.onclose = () => {
        console.log('Disconnected from MCP server')
        setIsConnected(false)
        setConnectionStatus('disconnected')
        socketRef.current = null
        onStatusChange?.('disconnected')
        
        // Implement exponential backoff reconnection
        if (reconnectAttemptsRef.current < maxReconnectAttempts) {
          setConnectionStatus('reconnecting')
          onStatusChange?.('reconnecting')
          
          const delay = Math.min(
            reconnectDelay * Math.pow(2, reconnectAttemptsRef.current),
            60000 // Max 60 seconds
          )
          
          reconnectTimeoutRef.current = setTimeout(() => {
            reconnectAttemptsRef.current++
            connect()
          }, delay)
        }
      }

      ws.onerror = (error) => {
        console.error('WebSocket error:', error)
      }

      socketRef.current = ws
    } catch (error) {
      console.error('Failed to create WebSocket connection:', error)
    }
  }, [url, reconnectDelay, maxReconnectAttempts, onMessage, onStatusChange])

  const disconnect = useCallback(() => {
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current)
      reconnectTimeoutRef.current = null
    }
    
    if (socketRef.current) {
      socketRef.current.close()
      socketRef.current = null
    }
  }, [])

  const sendMessage = useCallback((message: MCPMessage) => {
    if (!socketRef.current || socketRef.current.readyState !== WebSocket.OPEN) {
      console.error('WebSocket is not connected')
      return false
    }

    try {
      socketRef.current.send(JSON.stringify(message))
      return true
    } catch (error) {
      console.error('Failed to send message:', error)
      return false
    }
  }, [])

  useEffect(() => {
    connect()
    return () => disconnect()
  }, [connect, disconnect])

  return {
    isConnected,
    connectionStatus,
    sendMessage,
    reconnect: connect,
    disconnect
  }
}