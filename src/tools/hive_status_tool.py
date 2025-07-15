"""
Hive-Mind Natural Language Status Tool
Provides plain English status summaries for Claude Flow swarms
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime

class HiveStatusTool:
    """Natural language interface for Claude Flow hive-mind status"""
    
    def __init__(self):
        self.base_path = Path.home() / "Dropbox" / "MathematicalResearch" / "claude-flow-integration"
        
    def get_comprehensive_summary(self, query_type: str = "all") -> str:
        """Generate a comprehensive hive-mind summary"""
        if query_type == "summary" or query_type == "all":
            summary = {
                "queen_config": self._get_queen_config(),
                "active_sessions": self._get_active_sessions(),
                "swarm_composition": self._get_swarm_composition(),
                "memory_status": self._get_memory_status(),
                "system_info": self._get_system_info()
            }
            return self._format_summary(summary)
        elif query_type == "sessions":
            return self._format_sessions(self._get_active_sessions())
        elif query_type == "agents":
            return self._format_agents(self._get_swarm_composition())
        elif query_type == "memory":
            return self._format_memory(self._get_memory_status())
        else:
            return self._format_summary({
                "queen_config": self._get_queen_config(),
                "active_sessions": self._get_active_sessions(),
                "swarm_composition": self._get_swarm_composition(),
                "memory_status": self._get_memory_status(),
                "system_info": self._get_system_info()
            })
    
    def _get_queen_config(self) -> Dict[str, Any]:
        """Read queen configuration"""
        config_path = self.base_path / ".hive-mind" / "config.json"
        if config_path.exists():
            try:
                with open(config_path) as f:
                    return json.load(f)
            except Exception:
                pass
        return {}
    
    def _get_active_sessions(self) -> List[Dict[str, Any]]:
        """List all active sessions"""
        sessions_dir = self.base_path / ".hive-mind" / "sessions"
        sessions = []
        if sessions_dir.exists():
            for session_file in sessions_dir.glob("*.json"):
                try:
                    with open(session_file) as f:
                        sessions.append(json.load(f))
                except Exception:
                    continue
        return sessions
    
    def _get_swarm_composition(self) -> Dict[str, Any]:
        """Get current swarm agents and states"""
        sessions = self._get_active_sessions()
        if sessions:
            latest = max(sessions, key=lambda x: x.get('timestamp', ''))
            return latest.get('data', {})
        return {}
    
    def _get_memory_status(self) -> Dict[str, Any]:
        """Get memory system statistics"""
        memory_path = self.base_path / "memory" / "memory-store.json"
        if memory_path.exists():
            try:
                with open(memory_path) as f:
                    data = json.load(f)
                    return {
                        "total_entries": sum(len(v) for v in data.values()),
                        "namespaces": list(data.keys()),
                        "entries_by_namespace": {k: len(v) for k, v in data.items()}
                    }
            except Exception:
                pass
        return {"total_entries": 0, "namespaces": []}
    
    def _get_system_info(self) -> Dict[str, Any]:
        """Get system configuration info"""
        return {
            "version": "v2.0.0-alpha.53",
            "mcp_tools": 87,
            "integration_phase": "Phase 2 Complete",
            "base_path": str(self.base_path)
        }
    
    def _format_summary(self, data: Dict[str, Any]) -> str:
        """Format comprehensive summary for display"""
        config = data.get('queen_config', {}).get('defaults', {})
        sessions = data.get('active_sessions', [])
        memory = data.get('memory_status', {})
        system = data.get('system_info', {})
        swarm_data = data.get('swarm_composition', {})
        
        # Extract swarm info from latest session
        swarm_info = "No active swarms"
        agents_info = "No agents spawned"
        
        if sessions:
            latest_session = sessions[-1]
            session_data = latest_session.get('data', {})
            changes = session_data.get('changesByType', {})
            
            # Get swarm info
            swarm_created = changes.get('swarm_created', [])
            if swarm_created:
                swarm = swarm_created[0]['data']
                swarm_info = f"ID: {swarm.get('swarmId', 'Unknown')}\\nObjective: {swarm.get('objective', 'Unknown')}"
            
            # Get agent info
            agent_activities = changes.get('agent_activity', [])
            if agent_activities:
                agents = []
                for activity in agent_activities:
                    agent_data = activity['data']
                    agent_info = agent_data.get('data', {})
                    agents.append(f"  - {agent_info.get('name', 'Unknown')} ({agent_info.get('type', 'unknown')})")
                agents_info = "\\n".join(agents)
        
        return f"""🐝 Comprehensive Hive-Mind Summary
═══════════════════════════════════════════════════════════

👑 Queen Configuration:
  Type: {config.get('queenType', 'Unknown')}
  Max Workers: {config.get('maxWorkers', 0)}
  Auto-scaling: {'Enabled' if config.get('autoScale', False) else 'Disabled'}
  Consensus: {config.get('consensusAlgorithm', 'Unknown')}

📊 Active Sessions: {len(sessions)}
{swarm_info}

🐝 Active Agents:
{agents_info}

💾 Memory Status:
  Total Entries: {memory.get('total_entries', 0)}
  Namespaces: {', '.join(memory.get('namespaces', [])) or 'None'}

🔧 System Information:
  Version: {system.get('version', 'Unknown')}
  MCP Tools: {system.get('mcp_tools', 0)}
  Integration: {system.get('integration_phase', 'Unknown')}
  
📁 Data Location: {system.get('base_path', 'Unknown')}"""
    
    def _format_sessions(self, sessions: List[Dict[str, Any]]) -> str:
        """Format sessions list"""
        if not sessions:
            return "No active sessions found."
        
        output = f"📊 Active Sessions ({len(sessions)}):\\n"
        output += "═" * 50 + "\\n\\n"
        
        for session in sessions:
            session_id = session.get('sessionId', 'Unknown')
            timestamp = session.get('timestamp', 'Unknown')
            data = session.get('data', {})
            stats = data.get('statistics', {})
            
            output += f"Session: {session_id}\\n"
            output += f"Created: {timestamp}\\n"
            output += f"Tasks: {stats.get('tasksProcessed', 0)} processed, {stats.get('tasksCompleted', 0)} completed\\n"
            output += f"Agents: {stats.get('agentActivities', 0)} activities\\n"
            output += "-" * 40 + "\\n"
        
        return output
    
    def _format_agents(self, swarm_data: Dict[str, Any]) -> str:
        """Format agent information"""
        if not swarm_data:
            return "No agent data available."
        
        changes = swarm_data.get('changesByType', {})
        agent_activities = changes.get('agent_activity', [])
        
        if not agent_activities:
            return "No agents currently active."
        
        output = f"🐝 Active Agents ({len(agent_activities)}):\\n"
        output += "═" * 50 + "\\n\\n"
        
        for activity in agent_activities:
            agent_data = activity['data']
            agent_info = agent_data.get('data', {})
            
            output += f"Agent: {agent_info.get('name', 'Unknown')}\\n"
            output += f"Type: {agent_info.get('type', 'unknown')}\\n"
            output += f"ID: {agent_data.get('agentId', 'Unknown')}\\n"
            output += f"Status: {agent_data.get('activity', 'unknown')}\\n"
            output += "-" * 40 + "\\n"
        
        return output
    
    def _format_memory(self, memory_data: Dict[str, Any]) -> str:
        """Format memory statistics"""
        output = "💾 Memory System Status:\\n"
        output += "═" * 50 + "\\n\\n"
        
        output += f"Total Entries: {memory_data.get('total_entries', 0)}\\n"
        output += f"Namespaces: {len(memory_data.get('namespaces', []))}\\n\\n"
        
        entries_by_ns = memory_data.get('entries_by_namespace', {})
        if entries_by_ns:
            output += "Entries by Namespace:\\n"
            for ns, count in entries_by_ns.items():
                output += f"  - {ns}: {count} entries\\n"
        
        return output

# MCP Tool Definition
tool_definition = {
    "name": "hive_status",
    "description": "Get comprehensive hive-mind status in plain English. Responds to natural language queries about swarms, agents, memory, and sessions.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Natural language query about hive status (e.g., 'summary', 'sessions', 'agents', 'memory', 'all')",
                "default": "all"
            }
        },
        "required": []
    }
}

# Async wrapper for MCP compatibility
async def get_hive_status(query: str = "all") -> Dict[str, Any]:
    """Async wrapper for hive status tool"""
    tool = HiveStatusTool()
    try:
        summary = tool.get_comprehensive_summary(query)
        return {
            "status": "success",
            "summary": summary,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "suggestion": "Check if Claude Flow is properly initialized"
        }
