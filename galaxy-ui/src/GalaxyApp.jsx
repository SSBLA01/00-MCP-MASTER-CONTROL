// Galaxy UI Dashboard Integration
// Based on arXiv:2508.03991 - Agent-Self and Agent-User Architecture

import React from 'react';
import GalaxyDashboard from './GalaxyDashboard';

// Mock API service for development
class GalaxyAPIService {
  constructor() {
    this.agentId = 'galaxy-001';
    this.wsConnection = null;
  }

  // Connect to Galaxy backend
  async connect(endpoint = 'ws://localhost:8080/galaxy') {
    return new Promise((resolve, reject) => {
      this.wsConnection = new WebSocket(endpoint);
      
      this.wsConnection.onopen = () => {
        console.log('Connected to Galaxy backend');
        resolve(this.wsConnection);
      };
      
      this.wsConnection.onerror = (error) => {
        console.error('Galaxy connection error:', error);
        reject(error);
      };
    });
  }

  // Fetch agent capabilities
  async getCapabilities() {
    const response = await fetch(`/api/agent/${this.agentId}/capabilities`);
    return response.json();
  }

  // Get current cognition phase
  async getCurrentPhase() {
    const response = await fetch('/api/cognition/phase');
    return response.json();
  }

  // Trigger reflection phase
  async triggerReflection() {
    const response = await fetch('/api/cognition/reflect', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ agentId: this.agentId })
    });
    return response.json();
  }

  // Get evolution metrics
  async getEvolutionMetrics(timeframe = '24h') {
    const response = await fetch(`/api/evolution/metrics?timeframe=${timeframe}`);
    return response.json();
  }

  // Force adaptation
  async forceAdaptation(parameters = {}) {
    const response = await fetch('/api/control/adapt', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ agentId: this.agentId, ...parameters })
    });
    return response.json();
  }

  // Set new goal
  async setGoal(goal) {
    const response = await fetch('/api/control/goal', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ agentId: this.agentId, goal })
    });
    return response.json();
  }

  // Subscribe to real-time updates
  subscribe(callback) {
    if (this.wsConnection) {
      this.wsConnection.onmessage = (event) => {
        const data = JSON.parse(event.data);
        callback(data);
      };
    }
  }

  // Disconnect from backend
  disconnect() {
    if (this.wsConnection) {
      this.wsConnection.close();
      this.wsConnection = null;
    }
  }
}

// Galaxy Context Provider for React
const GalaxyContext = React.createContext(null);

export const GalaxyProvider = ({ children }) => {
  const [apiService] = React.useState(() => new GalaxyAPIService());
  const [connected, setConnected] = React.useState(false);

  React.useEffect(() => {
    // Auto-connect in development mode
    if (process.env.NODE_ENV === 'development') {
      apiService.connect()
        .then(() => setConnected(true))
        .catch(() => {
          console.log('Running in standalone mode (no backend)');
          setConnected(false);
        });
    }

    return () => apiService.disconnect();
  }, [apiService]);

  return (
    <GalaxyContext.Provider value={{ apiService, connected }}>
      {children}
    </GalaxyContext.Provider>
  );
};

// Hook to use Galaxy API
export const useGalaxy = () => {
  const context = React.useContext(GalaxyContext);
  if (!context) {
    throw new Error('useGalaxy must be used within GalaxyProvider');
  }
  return context;
};

// Main App Component
const App = () => {
  return (
    <GalaxyProvider>
      <GalaxyDashboard />
    </GalaxyProvider>
  );
};

export default App;