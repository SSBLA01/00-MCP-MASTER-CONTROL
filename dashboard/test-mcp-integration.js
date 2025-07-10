const { chromium } = require('@playwright/test');
const { test, expect } = require('@playwright/test');

// Configuration
const BASE_URL = 'http://localhost:3000';
const TEST_TIMEOUT = 30000;

// Test Suite for MCP Dashboard Integration
async function runTests() {
  console.log('🧪 Starting MCP Dashboard Integration Tests...\n');
  
  const browser = await chromium.launch({ 
    headless: process.env.CI === 'true',
    slowMo: 100 // Slow down for visibility
  });
  
  const context = await browser.newContext();
  const page = await context.newPage();
  
  // Test results tracker
  const results = {
    passed: 0,
    failed: 0,
    tests: []
  };

  // Helper function to log test results
  function logTest(name, passed, error = null) {
    const status = passed ? '✅ PASS' : '❌ FAIL';
    console.log(`${status}: ${name}`);
    if (error) console.log(`   Error: ${error.message}`);
    results.tests.push({ name, passed, error: error?.message });
    if (passed) results.passed++;
    else results.failed++;
  }

  try {
    // Navigate to dashboard
    await page.goto(BASE_URL);
    await page.waitForLoadState('networkidle');
    logTest('Dashboard loads successfully', true);

    // Test 1: Search Perplexity Button
    console.log('\n📍 Testing Search Perplexity...');
    try {
      const searchBtn = page.getByTestId('search-perplexity-btn');
      await expect(searchBtn).toBeVisible();
      await expect(searchBtn).toHaveText(/Search Perplexity/);
      
      // Type query in input
      await page.getByTestId('main-input').fill('gyrovector mathematics');
      await searchBtn.click();
      
      // Wait for output log update
      await page.waitForTimeout(1500);
      const codeOutput = await page.getByTestId('code-output').textContent();
      expect(codeOutput).toContain('Sent: search_perplexity');
      
      logTest('Search Perplexity button functionality', true);
    } catch (error) {
      logTest('Search Perplexity button functionality', false, error);
    }

    // Test 2: Search File System Button
    console.log('\n📍 Testing Search File System...');
    try {
      const fileBtn = page.getByTestId('search-files-btn');
      await expect(fileBtn).toBeVisible();
      
      await page.getByTestId('main-input').fill('research papers');
      await fileBtn.click();
      
      await page.waitForTimeout(1500);
      const codeOutput = await page.getByTestId('code-output').textContent();
      expect(codeOutput).toContain('Sent: search_file_system');
      
      logTest('Search File System button functionality', true);
    } catch (error) {
      logTest('Search File System button functionality', false, error);
    }

    // Test 3: Save to Obsidian Button
    console.log('\n📍 Testing Save to Obsidian...');
    try {
      const obsidianBtn = page.getByTestId('save-obsidian-btn');
      await expect(obsidianBtn).toBeVisible();
      
      await page.getByTestId('main-input').fill('Important research note about hyperbolic geometry');
      await obsidianBtn.click();
      
      await page.waitForTimeout(1500);
      const codeOutput = await page.getByTestId('code-output').textContent();
      expect(codeOutput).toContain('Sent: save_to_obsidian');
      
      logTest('Save to Obsidian button functionality', true);
    } catch (error) {
      logTest('Save to Obsidian button functionality', false, error);
    }

    // Test 4: Claude Desktop/Code Toggle
    console.log('\n📍 Testing Claude Desktop/Code toggle...');
    try {
      const toggleBtn = page.getByTestId('mode-toggle-btn');
      await expect(toggleBtn).toBeVisible();
      
      // Check initial state (Claude Desktop)
      await expect(toggleBtn).toHaveText(/Claude Desktop/);
      
      // Toggle to Claude Code
      await toggleBtn.click();
      await expect(toggleBtn).toHaveText(/Claude Code/);
      
      // Toggle back
      await toggleBtn.click();
      await expect(toggleBtn).toHaveText(/Claude Desktop/);
      
      logTest('Claude Desktop/Code toggle', true);
    } catch (error) {
      logTest('Claude Desktop/Code toggle', false, error);
    }

    // Test 5: Send to Claude Desktop
    console.log('\n📍 Testing Send to Claude Desktop...');
    try {
      // Ensure we're in Desktop mode
      const toggleBtn = page.getByTestId('mode-toggle-btn');
      if (!(await toggleBtn.textContent()).includes('Claude Desktop')) {
        await toggleBtn.click();
      }
      
      await page.getByTestId('main-input').fill('Test message to Claude Desktop');
      await page.getByTestId('send-btn').click();
      
      await page.waitForTimeout(1500);
      const codeOutput = await page.getByTestId('code-output').textContent();
      expect(codeOutput).toContain('Sent to Claude Desktop');
      expect(codeOutput).toContain('Test message to Claude Desktop');
      
      logTest('Send to Claude Desktop', true);
    } catch (error) {
      logTest('Send to Claude Desktop', false, error);
    }

    // Test 6: Send to Claude Code
    console.log('\n📍 Testing Send to Claude Code...');
    try {
      // Switch to Code mode
      const toggleBtn = page.getByTestId('mode-toggle-btn');
      await toggleBtn.click();
      await expect(toggleBtn).toHaveText(/Claude Code/);
      
      await page.getByTestId('main-input').fill('Test message to Claude Code');
      await page.getByTestId('send-btn').click();
      
      await page.waitForTimeout(1500);
      const codeOutput = await page.getByTestId('code-output').textContent();
      expect(codeOutput).toContain('Sent to Claude Code');
      expect(codeOutput).toContain('Test message to Claude Code');
      
      logTest('Send to Claude Code', true);
    } catch (error) {
      logTest('Send to Claude Code', false, error);
    }

    // Test 7: Keyboard Shortcut (Cmd/Ctrl + Enter)
    console.log('\n📍 Testing keyboard shortcut...');
    try {
      await page.getByTestId('main-input').fill('Keyboard shortcut test');
      
      // Press Cmd+Enter (Mac) or Ctrl+Enter (Windows/Linux)
      const modifier = process.platform === 'darwin' ? 'Meta' : 'Control';
      await page.keyboard.press(`${modifier}+Enter`);
      
      await page.waitForTimeout(1500);
      const codeOutput = await page.getByTestId('code-output').textContent();
      expect(codeOutput).toContain('Keyboard shortcut test');
      
      logTest('Keyboard shortcut (Cmd/Ctrl + Enter)', true);
    } catch (error) {
      logTest('Keyboard shortcut (Cmd/Ctrl + Enter)', false, error);
    }

    // Test 8: View Switching
    console.log('\n📍 Testing view switching...');
    try {
      // Test Code view (default)
      const codeViewBtn = page.getByTestId('view-code-btn');
      await codeViewBtn.click();
      await expect(page.getByTestId('code-output')).toBeVisible();
      
      // Test Files view
      const filesViewBtn = page.getByTestId('view-files-btn');
      await filesViewBtn.click();
      await expect(page.getByTestId('files-output')).toBeVisible();
      const filesContent = await page.getByTestId('files-output').textContent();
      expect(filesContent).toContain('Dropbox');
      
      // Test Logs view
      const logsViewBtn = page.getByTestId('view-logs-btn');
      await logsViewBtn.click();
      await expect(page.getByTestId('logs-output')).toBeVisible();
      const logsContent = await page.getByTestId('logs-output').textContent();
      expect(logsContent).toContain('System operational');
      
      logTest('View switching (Code/Files/Logs)', true);
    } catch (error) {
      logTest('View switching (Code/Files/Logs)', false, error);
    }

    // Test 9: Status Indicator
    console.log('\n📍 Testing status indicator...');
    try {
      const statusIndicator = page.getByTestId('status-indicator');
      await expect(statusIndicator).toBeVisible();
      
      // Check that it has one of the status colors
      const className = await statusIndicator.getAttribute('class');
      expect(className).toMatch(/bg-(green|yellow|red)-500/);
      
      logTest('Status indicator visibility', true);
    } catch (error) {
      logTest('Status indicator visibility', false, error);
    }

    // Test 10: Settings Dropdown
    console.log('\n📍 Testing settings dropdown...');
    try {
      // Click settings button
      await page.click('button[aria-label*="Settings"]');
      
      // Check dark mode toggle
      const darkModeSwitch = page.getByRole('switch');
      await expect(darkModeSwitch).toBeVisible();
      
      // Check font size options
      await expect(page.getByText('Font Size')).toBeVisible();
      
      // Close dropdown
      await page.keyboard.press('Escape');
      
      logTest('Settings dropdown functionality', true);
    } catch (error) {
      logTest('Settings dropdown functionality', false, error);
    }

    // Test 11: Tab Navigation
    console.log('\n📍 Testing tab navigation...');
    try {
      const tabs = ['Research', 'Visualization', 'Knowledge', 'Publish'];
      
      for (const tab of tabs) {
        const tabBtn = page.getByRole('tab', { name: tab });
        await expect(tabBtn).toBeVisible();
        await tabBtn.click();
        await expect(tabBtn).toHaveAttribute('data-state', 'active');
      }
      
      logTest('Tab navigation', true);
    } catch (error) {
      logTest('Tab navigation', false, error);
    }

    // Test 12: System Resource Meters
    console.log('\n📍 Testing system resource meters...');
    try {
      // Check CPU meter
      await expect(page.getByText('CPU')).toBeVisible();
      const cpuBar = page.locator('.bg-cyan-500').first();
      await expect(cpuBar).toBeVisible();
      
      // Check Memory meter
      await expect(page.getByText('Memory')).toBeVisible();
      
      // Check Disk meter
      await expect(page.getByText('Disk')).toBeVisible();
      
      logTest('System resource meters display', true);
    } catch (error) {
      logTest('System resource meters display', false, error);
    }

  } catch (error) {
    console.error('Test suite error:', error);
  } finally {
    // Print summary
    console.log('\n' + '='.repeat(50));
    console.log('📊 TEST SUMMARY');
    console.log('='.repeat(50));
    console.log(`Total Tests: ${results.passed + results.failed}`);
    console.log(`✅ Passed: ${results.passed}`);
    console.log(`❌ Failed: ${results.failed}`);
    console.log(`Success Rate: ${((results.passed / (results.passed + results.failed)) * 100).toFixed(1)}%`);
    
    // Save detailed results
    const fs = require('fs');
    fs.writeFileSync('test-results.json', JSON.stringify(results, null, 2));
    console.log('\n📄 Detailed results saved to test-results.json');
    
    await browser.close();
  }
}

// Run tests
runTests().catch(console.error);