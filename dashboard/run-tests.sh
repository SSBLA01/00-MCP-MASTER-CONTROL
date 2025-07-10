#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 MCP Dashboard Testing Suite${NC}"
echo "=================================="

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js is not installed. Please install Node.js first.${NC}"
    exit 1
fi

# Check if we're in the dashboard directory
if [ ! -f "package.json" ]; then
    echo -e "${RED}❌ Not in dashboard directory. Please run from the dashboard folder.${NC}"
    exit 1
fi

# Install dependencies if needed
echo -e "\n${YELLOW}📦 Checking dependencies...${NC}"
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
fi

# Install Playwright if not already installed
if [ ! -d "node_modules/@playwright/test" ]; then
    echo -e "\n${YELLOW}🎭 Installing Playwright...${NC}"
    npm install -D @playwright/test
    npx playwright install chromium
fi

# Build the Next.js app
echo -e "\n${YELLOW}🔨 Building Next.js app...${NC}"
npm run build

# Start the dev server in background
echo -e "\n${YELLOW}🌐 Starting development server...${NC}"
npm run dev > dev-server.log 2>&1 &
SERVER_PID=$!

# Function to cleanup on exit
cleanup() {
    echo -e "\n${YELLOW}🧹 Cleaning up...${NC}"
    kill $SERVER_PID 2>/dev/null
    exit
}

# Set trap to cleanup on script exit
trap cleanup EXIT INT TERM

# Wait for server to start
echo "Waiting for server to start..."
sleep 5

# Check if server is running
if ! curl -s http://localhost:3000 > /dev/null; then
    echo -e "${RED}❌ Server failed to start. Check dev-server.log for errors.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Server is running!${NC}"

# Run the tests
echo -e "\n${YELLOW}🧪 Running integration tests...${NC}"
echo "=================================="

# Create test report file
echo "MCP Dashboard Test Report" > test-report.txt
echo "=========================" >> test-report.txt
echo "Date: $(date)" >> test-report.txt
echo "" >> test-report.txt

# Run main integration tests
node test-mcp-integration.js | tee -a test-report.txt

# Run API tests if they exist
if [ -f "test-api-routes.js" ]; then
    echo -e "\n${YELLOW}🔌 Running API route tests...${NC}"
    node test-api-routes.js | tee -a test-report.txt
fi

# Check test results
if [ -f "test-results.json" ]; then
    PASSED=$(grep -o '"passed":[0-9]*' test-results.json | cut -d':' -f2)
    FAILED=$(grep -o '"failed":[0-9]*' test-results.json | cut -d':' -f2)
    
    echo -e "\n${GREEN}📊 FINAL RESULTS${NC}"
    echo "================="
    echo -e "✅ Passed: ${GREEN}$PASSED${NC}"
    echo -e "❌ Failed: ${RED}$FAILED${NC}"
    
    if [ "$FAILED" -eq 0 ]; then
        echo -e "\n${GREEN}🎉 All tests passed!${NC}"
    else
        echo -e "\n${RED}⚠️  Some tests failed. Check test-report.txt for details.${NC}"
    fi
fi

echo -e "\n📄 Full test report saved to: test-report.txt"
echo -e "📊 Test results JSON saved to: test-results.json"
echo -e "📝 Server logs saved to: dev-server.log"