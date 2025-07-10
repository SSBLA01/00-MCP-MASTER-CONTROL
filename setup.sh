#!/bin/bash

echo "Setting up Mathematical Research MCP System (Dobbs-MCP)..."

# Create directories
echo "Creating data directories..."
mkdir -p data/obsidian_vault/{Concepts,Papers,Proofs,Examples,Notebooks,Daily_notes}
mkdir -p data/manim_outputs
mkdir -p data/dropbox_sync

# Check for .env file
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo ""
    echo "⚠️  Please edit .env and add your API keys:"
    echo "   - PERPLEXITY_API_KEY"
    echo "   - WOLFRAM_ALPHA_APP_ID"
    echo "   - DROPBOX_APP_KEY and DROPBOX_APP_SECRET"
    echo "   - GITHUB_TOKEN"
    echo ""
    echo "Then run this script again."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Test imports
echo "Testing Python imports..."
python -c "
try:
    import mcp
    import aiohttp
    import aiofiles
    import yaml
    from dotenv import load_dotenv
    print('✓ All core imports successful!')
except ImportError as e:
    print(f'✗ Import error: {e}')
    exit(1)
"

# Check for Manim installation
echo "Checking Manim installation..."
if command -v manim &> /dev/null; then
    echo "✓ Manim is installed"
else
    echo "⚠️  Manim is not installed or not in PATH"
    echo "   You may need to install system dependencies:"
    echo "   - macOS: brew install ffmpeg py3cairo"
    echo "   - Ubuntu: sudo apt install ffmpeg libcairo2-dev"
fi

# Display Claude Desktop configuration instructions
echo ""
echo "=========================================="
echo "Setup complete! Next steps:"
echo "=========================================="
echo ""
echo "1. Add Dobbs-MCP to Claude Desktop configuration:"
echo ""
echo "   On macOS: ~/Library/Application Support/Claude/claude_desktop_config.json"
echo "   On Windows: %APPDATA%\\Claude\\claude_desktop_config.json"
echo ""
echo "2. Add this configuration:"
echo ""
cat << 'EOF'
{
  "mcpServers": {
    "Dobbs-MCP": {
      "command": "python",
      "args": ["-m", "src.servers.master_coordinator"],
      "cwd": "$(pwd)",
      "env": {
        "PYTHONPATH": "$(pwd)"
      }
    }
  }
}
EOF
echo ""
echo "3. Restart Claude Desktop"
echo ""
echo "4. Test by typing: 'Initialize a research session on topology'"
echo ""
echo "=========================================="