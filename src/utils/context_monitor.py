"""
Context monitoring utilities for MCP servers
Prevents conversation length from exceeding Claude Desktop limits
"""

import json
from typing import Dict, Any, List, Tuple
from datetime import datetime

class MCPContextMonitor:
    """Monitor and manage conversation context to prevent drops"""
    
    def __init__(self, max_chars: int = 50000):
        """Initialize context monitor with conservative limits"""
        self.MAX_CHARS = max_chars
        self.current_length = 0
        self.message_count = 0
        self.message_history: List[Dict[str, Any]] = []
        self.start_time = datetime.now()
        
    def check_context(self, new_message: Any) -> Dict[str, Any]:
        """Check if adding new message would exceed limits"""
        message_str = json.dumps(new_message) if not isinstance(new_message, str) else new_message
        message_length = len(message_str)
        projected_length = self.current_length + message_length
        
        # Calculate thresholds
        critical_threshold = self.MAX_CHARS * 0.85
        warning_threshold = self.MAX_CHARS * 0.70
        
        if projected_length > critical_threshold:
            return {
                'status': 'CRITICAL',
                'action': 'minimize',
                'message': '⚠️ Context limit reached. Minimizing responses.',
                'stats': {
                    'current': self.current_length,
                    'projected': projected_length,
                    'max': self.MAX_CHARS,
                    'message_count': self.message_count
                }
            }
        elif projected_length > warning_threshold:
            return {
                'status': 'WARNING',
                'action': 'warn',
                'message': '📊 Conversation approaching limit. Consider starting new chat.',
                'stats': {
                    'current': self.current_length,
                    'projected': projected_length,
                    'max': self.MAX_CHARS,
                    'percentage': (projected_length / self.MAX_CHARS) * 100
                }
            }
        
        return {'status': 'OK', 'action': None}
    
    def add_message(self, message: Any, tool_name: str) -> None:
        """Add message to history and update counters"""
        message_str = json.dumps(message) if not isinstance(message, str) else message
        message_length = len(message_str)
        
        self.message_history.append({
            'tool': tool_name,
            'length': message_length,
            'timestamp': datetime.now().isoformat()
        })
        
        self.current_length += message_length
        self.message_count += 1
        
        # Auto-truncate if needed
        while self.current_length > self.MAX_CHARS * 0.8 and len(self.message_history) > 5:
            removed = self.message_history.pop(0)
            self.current_length -= removed['length']
    
    def minimize_response(self, data: Any) -> Any:
        """Minimize response data to essential information"""
        if isinstance(data, dict):
            # Keep only essential fields
            essential_fields = ['status', 'result', 'data', 'error', 'message', 
                              'summary', 'key_results', 'id', 'type']
            
            minimized = {}
            for field in essential_fields:
                if field in data:
                    value = data[field]
                    # Truncate long strings
                    if isinstance(value, str) and len(value) > 500:
                        minimized[field] = value[:500] + '... [truncated]'
                    else:
                        minimized[field] = value
            
            # Add context warning
            minimized['_context_minimized'] = True
            return minimized
        
        elif isinstance(data, list):
            # Limit list size
            if len(data) > 10:
                return data[:10] + [{'message': f'... and {len(data) - 10} more items'}]
            return data
        
        elif isinstance(data, str):
            # Truncate long strings
            if len(data) > 1000:
                return data[:1000] + '... [truncated for context limit]'
            return data
        
        return data
    
    def get_stats(self) -> Dict[str, Any]:
        """Get current context statistics"""
        return {
            'current_length': self.current_length,
            'max_length': self.MAX_CHARS,
            'usage_percentage': (self.current_length / self.MAX_CHARS) * 100,
            'message_count': self.message_count,
            'session_duration': str(datetime.now() - self.start_time),
            'avg_message_size': self.current_length / max(1, self.message_count)
        }

# Global instance for the server
context_monitor = MCPContextMonitor()

def wrap_tool_response(tool_name: str, result: Any) -> Any:
    """Wrap tool responses with context monitoring"""
    # Check context before responding
    check = context_monitor.check_context(result)
    
    if check['status'] == 'CRITICAL':
        # Minimize the response
        minimized_result = context_monitor.minimize_response(result)
        context_monitor.add_message(minimized_result, tool_name)
        
        return {
            'result': minimized_result,
            '_context_warning': check['message'],
            '_context_stats': check.get('stats', {}),
            '_suggestion': 'Please start a new conversation to continue with full functionality.'
        }
    
    elif check['status'] == 'WARNING':
        # Add warning to response
        context_monitor.add_message(result, tool_name)
        
        if isinstance(result, dict):
            result['_context_warning'] = check['message']
            return result
        else:
            return {
                'result': result,
                '_context_warning': check['message']
            }
    
    # Normal response
    context_monitor.add_message(result, tool_name)
    return result
