"""
Hive-Mind Natural Language Status Tool
Provides plain English status summaries for Claude Flow swarms
"""

import json
import os
from pathlib import Path

class HiveStatusTool:
    """Natural language interface for Claude Flow hive-mind status"""
    
    def __init__(self):
        self.base_path = Path.home() / "Dropbox" / "MathematicalResearch" / "claude-flow-integration"
        
    def get_comprehensive_summary(self):
        """Generate a comprehensive hive-mind summary"""
        summary = {
            "queen_config": self._get_queen_config(),
            "active_sessions": self._get_active_sessions(),
            "swarm_composition": self._get_swarm_composition(),
            "memory_status": self._get_memory_status(),
            "system_info": self._get_system_info()
        }
        return self._format_summary(summary)
    
    def _get_queen_config(self):
        """Read queen configuration"""
        config_path = self.base_path / ".hive-mind" / "config.json"
        if config_path.exists():
            with open(config_path) as f:
                return json.load(f)
        return {}
    
    def _get_active_sessions(self):
        """List all active sessions"""
        sessions_dir = self.base_path / ".hive-mind" / "sessions"
        sessions = []
        if sessions_dir.exists():
            for session_file in sessions_dir.glob("*.json"):
                with open(session_file) as f:
                    sessions.append(json.load(f))
        return sessions
    
    def _get_swarm_composition(self):
        """Get current swarm agents and states"""
        # Parse from latest session data
        sessions = self._get_active_sessions()
        if sessions:
            latest = max(sessions, key=lambda x: x.get('timestamp', ''))
            return latest.get('data', {})
        return {}
    
    def _get_memory_status(self):
        """Get memory system statistics"""
        memory_path = self.base_path / "memory" / "memory-store.json"
        if memory_path.exists():
            with open(memory_path) as f:
                data = json.load(f)
                return {
                    "total_entries": sum(len(v) for v in data.values()),
                    "namespaces": list(data.keys())
                }
        return {}
    
    def _get_system_info(self):
        """Get system configuration info"""
        return {
            "version": "v2.0.0-alpha.53",
            "mcp_tools": 87,
            "integration_phase": "Phase 2 Complete"
        }
    
    def _format_summary(self, data):
        """Format summary for display"""
        return f"""
🐝 Comprehensive Hive-Mind Summary
═══════════════════════════════════════════

👑 Queen Configuration:
- Type: {data['queen_config'].get('defaults', {}).get('queenType', 'Unknown')}
- Max Workers: {data['queen_config'].get('defaults', {}).get('maxWorkers', 0)}
- Auto-scaling: {data['queen_config'].get('defaults', {}).get('autoScale', False)}

📊 Active Sessions: {len(data['active_sessions'])}
🐝 Memory Entries: {data['memory_status'].get('total_entries', 0)}
🔧 System Version: {data['system_info']['version']}
✅ Integration Status: {data['system_info']['integration_phase']}
"""

# MCP Tool Definition
tool_definition = {
    "name": "hive_status",
    "description": "Get comprehensive hive-mind status in plain English",
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Natural language query about hive status",
                "enum": ["summary", "sessions", "agents", "memory", "all"]
            }
        }
    }
}
