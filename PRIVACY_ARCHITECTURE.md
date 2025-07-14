# MCP Privacy Architecture

## Core Principle
**Obsidian content is PRIVATE by default. Nothing syncs to Notion automatically.**

## System Design

### 🔒 Obsidian (Private Knowledge Base)
- **What**: Local markdown files in Dropbox
- **Purpose**: Personal research, drafts, work-in-progress
- **Access**: Local only via Obsidian app or file system
- **Privacy**: Complete - nothing leaves without explicit command

### 🌐 Notion (Public Website Frontend)
- **What**: Cloud-based content platform
- **Purpose**: Public website, team collaboration
- **Access**: Web-based, intended for sharing
- **Content**: Only what you explicitly publish

## Privacy Rules

1. **No Automatic Syncing**
   - The `sync_obsidian_to_notion` tool is MANUAL ONLY
   - Requires explicit user command
   - Requires specific file selection
   - Never runs as part of automation

2. **Inbox Processing**
   - Files are processed to Obsidian (local)
   - Nothing goes to Notion automatically
   - All research stays private by default

3. **Search Priority**
   - Searches check cloud sources first
   - But never expose private Obsidian content
   - Obsidian searches are local only

## Usage

### ✅ Correct Commands
```bash
# These keep content private
"Process my inbox files"  # → Goes to Obsidian
"Create research note"    # → Stays in Obsidian
"Search my notes"         # → Searches locally

# These require explicit publishing
"Publish roadmap to Notion website"
"Copy final article to Notion"
"Share this research publicly"
```

### ❌ Never Happens Automatically
- Obsidian → Notion sync
- Research auto-publishing
- Private notes becoming public

## Architecture Benefits

1. **Privacy First**: Research stays private unless explicitly shared
2. **Selective Publishing**: Full control over what becomes public
3. **Clear Boundaries**: Obsidian = private, Notion = public
4. **No Accidents**: Impossible to accidentally publish private content

## Implementation

All MCP tools respect this architecture:
- `mcp_inbox_processor.py` - Sends to Obsidian only
- `mcp_search_priority.py` - Respects privacy boundaries  
- `sync_obsidian_to_notion` - Manual command only

## Summary

Your research workflow:
1. 🔒 Private research in Obsidian
2. 🔨 Refine and polish locally
3. 📢 Explicitly publish to Notion when ready
4. 🌐 Content appears on website

This ensures complete control over your intellectual property and research privacy.