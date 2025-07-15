#!/bin/bash
# Automated Hive Status Tool Integration Script

echo "🐝 Claude Flow Hive Status Tool Integration"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Step 1: Check if we're in the right directory
if [ ! -f "src/servers/dobbs_unified.py" ]; then
    echo -e "${RED}❌ Error: Not in the 00-MCP-MASTER-CONTROL directory${NC}"
    echo "Please run this script from the root of your MCP repository"
    exit 1
fi

echo -e "${GREEN}✅ Found MCP repository${NC}"
echo ""

# Step 2: Apply the patch
echo "📋 Applying integration patch..."
if git apply patches/add_hive_status_tool.patch 2>/dev/null; then
    echo -e "${GREEN}✅ Patch applied successfully${NC}"
else
    # Check if already applied
    if grep -q "hive_status" src/servers/dobbs_unified.py; then
        echo -e "${YELLOW}⚠️  Patch already applied${NC}"
    else
        echo -e "${RED}❌ Failed to apply patch${NC}"
        echo "You may need to apply it manually"
    fi
fi
echo ""

# Step 3: Run the test
echo "🧪 Running integration test..."
python3 tests/test_hive_status_integration.py
TEST_RESULT=$?

if [ $TEST_RESULT -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✅ Integration successful!${NC}"
    echo ""
    echo "🎯 Next Steps:"
    echo "1. Restart Claude Desktop"
    echo "2. Try these commands:"
    echo "   - 'What's my hive status?'"
    echo "   - 'Show me active swarms'"
    echo "   - 'Give me a hive summary'"
    echo ""
    echo "The tool will now work in ALL future Claude sessions!"
else
    echo ""
    echo -e "${RED}❌ Test failed${NC}"
    echo "Please check the error messages above"
fi

echo ""
echo "📝 Integration Summary:"
echo "- Tool location: src/tools/hive_status_tool.py"
echo "- Patch file: patches/add_hive_status_tool.patch"
echo "- Test script: tests/test_hive_status_integration.py"
echo ""
echo "=========================================="
