#!/usr/bin/env python3
"""
MCP Security Test Suite
Tests all security restrictions to ensure they work properly
"""

import asyncio
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.servers.file_operations_secured import (
    validate_dropbox_path, 
    sanitize_file_path,
    list_dropbox_folder,
    read_dropbox_file,
    save_to_dropbox,
    search_dropbox
)

class SecurityTester:
    def __init__(self):
        self.tests_passed = 0
        self.tests_failed = 0
        
    def assert_allowed(self, path: str, description: str):
        """Test that a path SHOULD be allowed"""
        is_valid, msg = validate_dropbox_path(path)
        if is_valid:
            print(f"✅ PASS: {description} - '{path}' correctly allowed")
            self.tests_passed += 1
        else:
            print(f"❌ FAIL: {description} - '{path}' should be allowed but was blocked: {msg}")
            self.tests_failed += 1
    
    def assert_blocked(self, path: str, description: str):
        """Test that a path SHOULD be blocked"""
        is_valid, msg = validate_dropbox_path(path)
        if not is_valid:
            print(f"✅ PASS: {description} - '{path}' correctly blocked")
            self.tests_passed += 1
        else:
            print(f"❌ FAIL: {description} - '{path}' should be blocked but was allowed")
            self.tests_failed += 1
    
    def test_path_validation(self):
        """Test core path validation logic"""
        print("\n🔒 Testing Path Validation")
        print("=" * 50)
        
        # Test allowed paths
        self.assert_allowed("00_MCP_Living_Knowledge_System", "Knowledge system access")
        self.assert_allowed("00_MCP_Living_Knowledge_System/5_Mathematical_Physics", "Math physics folder")
        self.assert_allowed("00_MCP_SYSTEM", "MCP system folder")
        self.assert_allowed("Media", "Media folder")
        self.assert_allowed("Media/animations", "Media subfolder")
        self.assert_allowed("MathematicalResearch", "Math research folder")
        self.assert_allowed("", "Root directory listing")
        
        # Test blocked paths
        self.assert_blocked("01_Totem_Networks", "Totem Networks folder (forbidden)")
        self.assert_blocked("01_Totem_Networks/secret.txt", "File in Totem Networks")
        self.assert_blocked("../../../etc/passwd", "Path traversal to system files")
        self.assert_blocked("../../System/important", "Path traversal to System")
        self.assert_blocked("/etc/passwd", "Direct system access")
        self.assert_blocked("Library/Keychains", "Keychain access")
        self.assert_blocked("SomeRandomFolder", "Unknown folder")
    
    def test_path_sanitization(self):
        """Test input sanitization"""
        print("\n🧽 Testing Path Sanitization")
        print("=" * 50)
        
        test_cases = [
            ("../../../etc/passwd", "etc/passwd"),
            ("00_MCP_SYSTEM/../01_Totem_Networks", "00_MCP_SYSTEM/01_Totem_Networks"),
            ("  /Media/test.mp4  ", "Media/test.mp4"),
            ("Media\\\\test.mp4", "Media/test.mp4"),
            ("Media/test<script>", "Media/testscript"),
            ("~/.ssh/id_rsa", ".ssh/id_rsa")
        ]
        
        for input_path, expected in test_cases:
            result = sanitize_file_path(input_path)
            if result == expected:
                print(f"✅ PASS: '{input_path}' -> '{result}'")
                self.tests_passed += 1
            else:
                print(f"❌ FAIL: '{input_path}' -> '{result}' (expected '{expected}')")
                self.tests_failed += 1
    
    async def test_file_operations(self):
        """Test actual file operations"""
        print("\n📁 Testing File Operations")
        print("=" * 50)
        
        # Test allowed folder listing
        result = await list_dropbox_folder("00_MCP_SYSTEM")
        if "security_block" not in result:
            print("✅ PASS: Can list allowed folder (00_MCP_SYSTEM)")
            self.tests_passed += 1
        else:
            print(f"❌ FAIL: Cannot list allowed folder: {result['error']}")
            self.tests_failed += 1
        
        # Test blocked folder listing
        result = await list_dropbox_folder("01_Totem_Networks")
        if "security_block" in result:
            print("✅ PASS: Blocked access to forbidden folder (01_Totem_Networks)")
            self.tests_passed += 1
        else:
            print(f"❌ FAIL: Should block Totem Networks access but didn't: {result}")
            self.tests_failed += 1
        
        # Test path traversal attack
        result = await list_dropbox_folder("../../../etc")
        if "security_block" in result:
            print("✅ PASS: Blocked path traversal attack")
            self.tests_passed += 1
        else:
            print(f"❌ FAIL: Path traversal attack succeeded: {result}")
            self.tests_failed += 1
    
    async def test_search_security(self):
        """Test search operation security"""
        print("\n🔍 Testing Search Security")
        print("=" * 50)
        
        # Test search in allowed path
        result = await search_dropbox("test", "filename", "00_MCP_SYSTEM")
        if "security_block" not in result:
            print("✅ PASS: Search allowed in permitted folder")
            self.tests_passed += 1
        else:
            print(f"❌ FAIL: Search blocked in allowed folder: {result}")
            self.tests_failed += 1
        
        # Test search in forbidden path
        result = await search_dropbox("test", "filename", "01_Totem_Networks")
        if "security_block" in result:
            print("✅ PASS: Search blocked in forbidden folder")
            self.tests_passed += 1
        else:
            print(f"❌ FAIL: Search allowed in forbidden folder: {result}")
            self.tests_failed += 1
    
    async def test_create_security_log(self):
        """Test that we can create a security test log"""
        print("\n📝 Testing Security Logging")
        print("=" * 50)
        
        test_content = f"""# Security Test Results
Date: {asyncio.get_event_loop().time()}
Tests Passed: {self.tests_passed}
Tests Failed: {self.tests_failed}
Status: {'PASS' if self.tests_failed == 0 else 'FAIL'}

This file was created by the security test suite to verify that
the MCP system can write to allowed directories while blocking
access to forbidden ones.
"""
        
        result = await save_to_dropbox(test_content, "00_MCP_SYSTEM/security_test_log.md", overwrite=True)
        if result.get("status") == "success":
            print("✅ PASS: Can write to allowed directory")
            self.tests_passed += 1
        else:
            print(f"❌ FAIL: Cannot write to allowed directory: {result}")
            self.tests_failed += 1
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 60)
        print("🛡️  SECURITY TEST SUMMARY")
        print("=" * 60)
        print(f"Tests Passed: {self.tests_passed}")
        print(f"Tests Failed: {self.tests_failed}")
        print(f"Total Tests: {self.tests_passed + self.tests_failed}")
        
        if self.tests_failed == 0:
            print("\n🎉 ALL SECURITY TESTS PASSED!")
            print("✅ Your MCP system is properly secured")
            print("✅ Forbidden paths are blocked")
            print("✅ Allowed paths work correctly")
            print("✅ Path traversal attacks are prevented")
            return True
        else:
            print(f"\n⚠️  {self.tests_failed} SECURITY TESTS FAILED!")
            print("❌ Security implementation needs fixes")
            print("❌ Do not deploy until all tests pass")
            return False

async def main():
    """Run all security tests"""
    print("🔒 MCP SECURITY TEST SUITE")
    print("Testing all security restrictions...")
    
    tester = SecurityTester()
    
    # Run all tests
    tester.test_path_validation()
    tester.test_path_sanitization()
    await tester.test_file_operations()
    await tester.test_search_security()
    await tester.test_create_security_log()
    
    # Print results
    success = tester.print_summary()
    
    if success:
        print("\n🚀 READY FOR DEPLOYMENT")
        print("You can safely replace file_operations.py with file_operations_secured.py")
    else:
        print("\n🛑 NOT READY FOR DEPLOYMENT")
        print("Fix the failing tests before deploying security changes")
    
    return success

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
