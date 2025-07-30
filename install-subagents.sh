#!/bin/bash

# Claude Code Sub-agents Installation Script
# This script installs all mathematical research sub-agents

echo "🚀 Installing Claude Code Sub-agents for Mathematical Research..."

# Create necessary directories
echo "📁 Creating agent directories..."
mkdir -p ~/.claude/agents
mkdir -p ~/.claude/logs

# Check if we're in the right directory
if [ ! -d "claude-code-subagents" ]; then
    echo "❌ Error: claude-code-subagents directory not found!"
    echo "Please run this script from the repository root."
    exit 1
fi

# Copy all agent files
echo "📋 Copying agent definitions..."
cp claude-code-subagents/*.md ~/.claude/agents/

# Count installed agents
AGENT_COUNT=$(ls ~/.claude/agents/*.md 2>/dev/null | wc -l)

# List installed agents
echo ""
echo "✅ Successfully installed $AGENT_COUNT sub-agents:"
echo ""
for agent in ~/.claude/agents/*.md; do
    if [ -f "$agent" ]; then
        basename "$agent" .md | sed 's/^/  • /'
    fi
done

# Provide usage instructions
echo ""
echo "📖 Usage Instructions:"
echo "1. Open Claude Code"
echo "2. Use the /agents command to see all available agents"
echo "3. Agents will be automatically invoked based on their descriptions"
echo "4. You can also explicitly request an agent: 'Using the math-animator agent...'"

echo ""
echo "🔧 Configuration:"
echo "• Agent definitions: ~/.claude/agents/"
echo "• Logs will appear in: ~/.claude/logs/"
echo "• To update agents, pull latest from GitHub and run this script again"

echo ""
echo "🎯 Key Sub-agents for Your Research:"
echo "• inbox-librarian - Monitors email/drives and ingests to Obsidian"
echo "• math-animator - Creates Manim visualizations"
echo "• jung-symbolist - Analyzes archetypal patterns"
echo "• research-orchestrator - Routes complex tasks optimally"

echo ""
echo "✨ Installation complete! Happy researching!"