# Context Length Fix for MCP

## Problem
MCP conversations in Claude Desktop were hitting maximum conversation length limits, causing dropped executions.

## Solution
Added context monitoring to track and manage conversation length:

### Features
1. **Automatic Context Tracking**: Monitors character count of all tool responses
2. **Warning System**: 
   - Warns at 70% capacity
   - Minimizes responses at 85% capacity
3. **Response Minimization**: Automatically truncates large responses when approaching limits
4. **Statistics Tracking**: Provides usage stats and message counts

### Implementation
- `src/utils/context_monitor.py`: Core monitoring logic
- Updated `src/servers/dobbs_unified.py` to use context monitoring

### How It Works
- Each tool response is checked before sending
- Large responses are automatically minimized when context is critical
- Warnings are added to responses when approaching limits
- Users are prompted to start new conversations when needed

### Configuration
Default limit: 50,000 characters (conservative estimate)
Adjust in `context_monitor.py` if needed:
```python
context_monitor = MCPContextMonitor(max_chars=50000)
```

## To Deploy
1. Pull this branch
2. Restart your MCP server
3. Monitor logs for context warnings

The fix is transparent to users but prevents conversation drops.
