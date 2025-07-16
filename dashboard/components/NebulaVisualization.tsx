"use client"

import React, { useEffect, useRef, useState } from 'react'

interface ServiceNode {
  id: string
  name: string
  status: 'healthy' | 'warning' | 'error' | 'offline'
  connections: string[]
  x?: number
  y?: number
  vx?: number
  vy?: number
}

interface NebulaVisualizationProps {
  services: ServiceNode[]
  onNodeClick?: (node: ServiceNode) => void
}

export function NebulaVisualization({ services, onNodeClick }: NebulaVisualizationProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const animationRef = useRef<number>()
  const [hoveredNode, setHoveredNode] = useState<string | null>(null)
  const nodesRef = useRef<Map<string, ServiceNode>>(new Map())

  // Initialize node positions
  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    const width = canvas.width
    const height = canvas.height
    const centerX = width / 2
    const centerY = height / 2

    services.forEach((service, index) => {
      const angle = (index / services.length) * Math.PI * 2
      const radius = 150 + Math.random() * 100
      
      if (!service.x || !service.y) {
        service.x = centerX + Math.cos(angle) * radius
        service.y = centerY + Math.sin(angle) * radius
        service.vx = (Math.random() - 0.5) * 0.5
        service.vy = (Math.random() - 0.5) * 0.5
      }
      
      nodesRef.current.set(service.id, service)
    })
  }, [services])

  // Animation loop
  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    const ctx = canvas.getContext('2d')
    if (!ctx) return

    const width = canvas.width
    const height = canvas.height

    const getStatusColor = (status: string) => {
      switch (status) {
        case 'healthy': return '#10b981' // green
        case 'warning': return '#f59e0b' // yellow
        case 'error': return '#ef4444' // red
        case 'offline': return '#6b7280' // gray
        default: return '#6b7280'
      }
    }

    const drawNode = (node: ServiceNode) => {
      if (!node.x || !node.y) return

      const radius = hoveredNode === node.id ? 20 : 15
      const color = getStatusColor(node.status)

      // Glow effect
      const gradient = ctx.createRadialGradient(node.x, node.y, 0, node.x, node.y, radius * 2)
      gradient.addColorStop(0, color + '80')
      gradient.addColorStop(0.5, color + '40')
      gradient.addColorStop(1, 'transparent')
      
      ctx.fillStyle = gradient
      ctx.beginPath()
      ctx.arc(node.x, node.y, radius * 2, 0, Math.PI * 2)
      ctx.fill()

      // Node core
      ctx.fillStyle = color
      ctx.beginPath()
      ctx.arc(node.x, node.y, radius, 0, Math.PI * 2)
      ctx.fill()

      // Label
      ctx.fillStyle = '#ffffff'
      ctx.font = '12px sans-serif'
      ctx.textAlign = 'center'
      ctx.fillText(node.name, node.x, node.y + radius + 20)
    }

    const drawConnection = (from: ServiceNode, to: ServiceNode) => {
      if (!from.x || !from.y || !to.x || !to.y) return

      ctx.strokeStyle = '#06b6d480' // cyan with transparency
      ctx.lineWidth = 1
      ctx.beginPath()
      ctx.moveTo(from.x, from.y)
      
      // Create curved path
      const dx = to.x - from.x
      const dy = to.y - from.y
      const mx = from.x + dx / 2
      const my = from.y + dy / 2
      const offset = 30
      
      ctx.quadraticCurveTo(
        mx + dy / offset,
        my - dx / offset,
        to.x,
        to.y
      )
      
      ctx.stroke()
    }

    const animate = () => {
      ctx.fillStyle = '#111827' // dark background
      ctx.fillRect(0, 0, width, height)

      // Draw starfield background
      for (let i = 0; i < 100; i++) {
        const x = (i * 73) % width
        const y = (i * 37) % height
        const size = ((i * 7) % 3) + 1
        const opacity = ((i * 13) % 50) / 100 + 0.2
        
        ctx.fillStyle = `rgba(255, 255, 255, ${opacity})`
        ctx.fillRect(x, y, size, size)
      }

      // Update positions
      nodesRef.current.forEach(node => {
        if (!node.x || !node.y || !node.vx || !node.vy) return

        // Apply velocity
        node.x += node.vx
        node.y += node.vy

        // Bounce off edges
        if (node.x < 20 || node.x > width - 20) node.vx *= -1
        if (node.y < 20 || node.y > height - 20) node.vy *= -1

        // Keep within bounds
        node.x = Math.max(20, Math.min(width - 20, node.x))
        node.y = Math.max(20, Math.min(height - 20, node.y))

        // Apply slight damping
        node.vx *= 0.999
        node.vy *= 0.999

        // Add subtle drift
        node.vx += (Math.random() - 0.5) * 0.02
        node.vy += (Math.random() - 0.5) * 0.02
      })

      // Draw connections
      nodesRef.current.forEach(node => {
        node.connections.forEach(targetId => {
          const target = nodesRef.current.get(targetId)
          if (target) {
            drawConnection(node, target)
          }
        })
      })

      // Draw nodes
      nodesRef.current.forEach(drawNode)

      animationRef.current = requestAnimationFrame(animate)
    }

    animate()

    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current)
      }
    }
  }, [hoveredNode])

  // Handle mouse interactions
  const handleMouseMove = (e: React.MouseEvent<HTMLCanvasElement>) => {
    const canvas = canvasRef.current
    if (!canvas) return

    const rect = canvas.getBoundingClientRect()
    const x = e.clientX - rect.left
    const y = e.clientY - rect.top

    let foundNode: string | null = null

    nodesRef.current.forEach(node => {
      if (!node.x || !node.y) return
      
      const distance = Math.sqrt(
        Math.pow(x - node.x, 2) + Math.pow(y - node.y, 2)
      )
      
      if (distance < 20) {
        foundNode = node.id
      }
    })

    setHoveredNode(foundNode)
    canvas.style.cursor = foundNode ? 'pointer' : 'default'
  }

  const handleClick = (e: React.MouseEvent<HTMLCanvasElement>) => {
    if (hoveredNode && onNodeClick) {
      const node = nodesRef.current.get(hoveredNode)
      if (node) {
        onNodeClick(node)
      }
    }
  }

  return (
    <canvas
      ref={canvasRef}
      width={800}
      height={600}
      className="rounded-lg shadow-2xl shadow-cyan-500/20"
      onMouseMove={handleMouseMove}
      onClick={handleClick}
    />
  )
}