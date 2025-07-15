#!/usr/bin/env python3
"""
Test Script for Dobbs Unified Server Configuration
==================================================

This script tests the unified server configuration after the Flow upgrade.
It verifies that dobbs_unified loads correctly with all required components.

Author: MCP Development Team
Date: 2025-07-14
Issue: Unified server falling back to master_coordinator
"""

import json
import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime


class UnifiedServerTester:
    """Test harness for the Dobbs Unified Server"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.results = []
        self.test_start = datetime.now()
        
    def log_result(self, test_name: str, status: bool, message: str):
        """Log test results"""
        self.results.append({
            "test": test_name,
            "status": "PASS" if status else "FAIL",
            "message": message,
            "timestamp": datetime.now().isoformat()
        })
        
        # Print immediate feedback
        status_emoji = "✅" if status else "❌"
        print(f"{status_emoji} {test_name}: {message}")
    
    def test_configuration(self):
        """Test 1: Verify configuration file is correct"""
        print("\n=== Test 1: Configuration File ===")
        
        config_path = self.project_root / "claude_desktop_config.json"
        
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            # Check if Dobbs-Unified exists
            if "Dobbs-Unified" in config.get("mcpServers", {}):
                server_config = config["mcpServers"]["Dobbs-Unified"]
                
                # Verify it points to dobbs_unified
                args = server_config.get("args", [])
                if args and args[-1] == "src.servers.dobbs_unified":
                    self.log_result("Configuration", True, "Points to dobbs_unified correctly")
                else:
                    self.log_result("Configuration", False, f"Points to {args[-1] if args else 'nothing'}")
            else:
                self.log_result("Configuration", False, "Dobbs-Unified not found in config")
                
        except Exception as e:
            self.log_result("Configuration", False, f"Error reading config: {e}")
    
    def test_imports(self):
        """Test 2: Verify all required modules can be imported"""
        print("\n=== Test 2: Module Imports ===")
        
        # Add project root to path
        sys.path.insert(0, str(self.project_root))
        
        modules_to_test = [
            ("MCP SDK", "mcp.server"),
            ("Utils", "src.utils.common"),
            ("File Operations", "src.servers.file_operations"),
            ("GitHub Operations", "src.servers.github_operations"),
            ("Master Coordinator", "src.servers.master_coordinator"),
            ("Research Discovery", "src.servers.research_discovery"),
            ("Mathematical Visualization", "src.servers.mathematical_visualization"),
            ("Knowledge Ingestion", "src.servers.knowledge_ingestion"),
            ("Obsidian Enhanced", "src.servers.obsidian_enhanced"),
            ("Notion Operations", "src.servers.notion_operations"),
            ("Gemini Operations", "src.servers.gemini_operations"),
        ]
        
        for name, module in modules_to_test:
            try:
                __import__(module)
                self.log_result(f"Import {name}", True, f"{module} imported successfully")
            except ImportError as e:
                self.log_result(f"Import {name}", False, f"Failed to import {module}: {e}")
    
    def test_environment(self):
        """Test 3: Verify environment variables"""
        print("\n=== Test 3: Environment Variables ===")
        
        required_vars = [
            "DROPBOX_APP_KEY",
            "DROPBOX_APP_SECRET",
            "DROPBOX_REFRESH_TOKEN",
            "GITHUB_TOKEN",
            "WOLFRAM_ALPHA_APP_ID",
            "PERPLEXITY_API_KEY",
            "NOTION_API_KEY",
            "GEMINI_API_KEY"
        ]
        
        # Load .env if exists
        env_path = self.project_root / ".env"
        if env_path.exists():
            from dotenv import load_dotenv
            load_dotenv(env_path)
            self.log_result("Environment File", True, ".env file loaded")
        else:
            self.log_result("Environment File", False, ".env file not found")
        
        missing_vars = []
        for var in required_vars:
            if os.environ.get(var):
                self.log_result(f"Env {var}", True, "Set")
            else:
                self.log_result(f"Env {var}", False, "Not set")
                missing_vars.append(var)
        
        if missing_vars:
            print(f"\n⚠️  Missing environment variables: {', '.join(missing_vars)}")
    
    def test_server_startup(self):
        """Test 4: Try to start the server"""
        print("\n=== Test 4: Server Startup Test ===")
        
        # Test if we can import and create the server
        try:
            sys.path.insert(0, str(self.project_root))
            from src.servers.dobbs_unified import server, ALL_TOOLS
            
            self.log_result("Server Import", True, "dobbs_unified imported successfully")
            self.log_result("Server Instance", True, f"Server created with {len(ALL_TOOLS)} tools")
            
            # List tool categories
            tool_categories = {
                "File Operations": 0,
                "GitHub Operations": 0,
                "Research Tools": 0,
                "Visualization": 0,
                "Knowledge Management": 0,
                "Notion": 0,
                "Gemini": 0
            }
            
            for tool in ALL_TOOLS:
                if "dropbox" in tool.name.lower() or "file" in tool.name.lower():
                    tool_categories["File Operations"] += 1
                elif "github" in tool.name.lower():
                    tool_categories["GitHub Operations"] += 1
                elif "research" in tool.name.lower() or "discover" in tool.name.lower():
                    tool_categories["Research Tools"] += 1
                elif "manim" in tool.name.lower() or "visual" in tool.name.lower():
                    tool_categories["Visualization"] += 1
                elif "obsidian" in tool.name.lower() or "index" in tool.name.lower():
                    tool_categories["Knowledge Management"] += 1
                elif "notion" in tool.name.lower():
                    tool_categories["Notion"] += 1
                elif "gemini" in tool.name.lower():
                    tool_categories["Gemini"] += 1
            
            print("\n📊 Tool Categories:")
            for category, count in tool_categories.items():
                if count > 0:
                    print(f"   - {category}: {count} tools")
            
        except Exception as e:
            self.log_result("Server Startup", False, f"Failed to start server: {e}")
    
    def generate_report(self):
        """Generate a test report"""
        print("\n" + "="*60)
        print("TEST REPORT")
        print("="*60)
        
        passed = sum(1 for r in self.results if r["status"] == "PASS")
        failed = sum(1 for r in self.results if r["status"] == "FAIL")
        
        print(f"Total Tests: {len(self.results)}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        print(f"Success Rate: {(passed/len(self.results)*100):.1f}%")
        
        if failed > 0:
            print("\n❌ Failed Tests:")
            for result in self.results:
                if result["status"] == "FAIL":
                    print(f"   - {result['test']}: {result['message']}")
        
        # Save report to file
        report_path = self.project_root / "test_results" / f"unified_server_test_{self.test_start.strftime('%Y%m%d_%H%M%S')}.json"
        report_path.parent.mkdir(exist_ok=True)
        
        with open(report_path, 'w') as f:
            json.dump({
                "test_run": self.test_start.isoformat(),
                "summary": {
                    "total": len(self.results),
                    "passed": passed,
                    "failed": failed
                },
                "results": self.results
            }, f, indent=2)
        
        print(f"\n📄 Report saved to: {report_path}")
        
        return failed == 0


def main():
    """Main test runner"""
    print("🧪 Dobbs Unified Server Test Suite")
    print("=" * 60)
    
    tester = UnifiedServerTester()
    
    # Run all tests
    tester.test_configuration()
    tester.test_imports()
    tester.test_environment()
    tester.test_server_startup()
    
    # Generate report
    success = tester.generate_report()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
