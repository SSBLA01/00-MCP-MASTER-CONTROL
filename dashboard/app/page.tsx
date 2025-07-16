"use client"

import { useState } from 'react'
import Dashboard from '@/components/Dashboard'
import EnhancedDashboard from '@/components/EnhancedDashboard'

export default function Home() {
  // Set to true to use the enhanced dashboard with WebSocket and Obsidian integration
  const useEnhanced = true
  
  return useEnhanced ? <EnhancedDashboard /> : <Dashboard />
}