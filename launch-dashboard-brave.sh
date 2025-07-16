#!/bin/bash

# Launch MCP Dashboard in Brave Browser
# This script starts the dashboard server and opens it in Brave

echo "🚀 Launching MCP Dashboard..."

# Change to dashboard directory
cd "$(dirname "$0")/dashboard" || exit 1

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# Start the dashboard in the background
echo "🔧 Starting dashboard server..."
npm run dev &
SERVER_PID=$!

# Wait for the server to start
echo "⏳ Waiting for server to start..."
sleep 3

# Check if server is running
if ! curl -s http://localhost:3000/api/health > /dev/null; then
    echo "❌ Failed to start dashboard server"
    kill $SERVER_PID 2>/dev/null
    exit 1
fi

# Open in Brave browser
echo "🌐 Opening dashboard in Brave..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    open -a "Brave Browser" http://localhost:3000
elif command -v brave-browser &> /dev/null; then
    # Linux with brave-browser command
    brave-browser http://localhost:3000 &
elif command -v brave &> /dev/null; then
    # Linux with brave command
    brave http://localhost:3000 &
else
    echo "⚠️  Brave browser not found. Opening in default browser..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        open http://localhost:3000
    else
        xdg-open http://localhost:3000
    fi
fi

echo "✅ Dashboard launched successfully!"
echo "📍 Dashboard URL: http://localhost:3000"
echo "🛑 Press Ctrl+C to stop the server"

# Wait for user to stop the server
wait $SERVER_PID