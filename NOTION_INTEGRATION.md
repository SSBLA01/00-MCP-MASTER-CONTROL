# Notion Integration for Dobbs-MCP

## Overview
Full Notion workspace control is now available through Claude Desktop! You can search, create, update pages, work with databases, and sync from Obsidian.

## Setup

1. **Get your Notion Integration Token**:
   - Go to https://www.notion.so/my-integrations
   - Create a new integration (or use existing)
   - Copy the "Internal Integration Token"

2. **Add to .env file**:
   ```
   NOTION_TOKEN=your_token_here
   ```

3. **Grant Access to Pages**:
   - In Notion, go to any page/database you want to access
   - Click "..." menu → "Add connections" → Select your integration

4. **Restart Claude Desktop**

## Available Tools (6 New!)

### 1. Search Notion
```
Search Notion for "mathematical research"
Search Notion databases only
Find all pages containing "gyrovector"
```

### 2. Create Notion Page
```
Create a new Notion page titled "Hyperbolic Geometry Research" with content from today's work
Create a page about Mobius transformations under the Mathematics parent page
```

### 3. Update Notion Page
```
Update the "Research Notes" page with new findings
Add content to page [page-id] about complex analysis
Replace all content in "Old Notes" page with updated version
```

### 4. Work with Databases
```
List all my Notion databases
Add a new entry to the Research Papers database with title "Gyrovector Spaces" and status "In Progress"
```

### 5. Sync from Obsidian
```
Sync my Obsidian note "Daily Notes/2024-01-11" to Notion
Create a new Notion page from "Concepts/Hyperbolic_Rotation.md"
Update existing Notion page with latest version from Obsidian
```

### 6. Database Operations
```
Add to Research database: {"Title": "New Paper", "Status": "Draft", "Topic": "Topology"}
```

## Features

### Rich Content Support
- Markdown formatting is automatically converted to Notion blocks
- Headers, bullet points, code blocks, quotes all supported
- LaTeX equations preserved
- Links and formatting maintained

### Smart Sync
- Automatically detects if a page exists when syncing
- Can create new or update existing pages
- Preserves Obsidian structure in Notion

### Page Hierarchy
- Create pages under specific parent pages
- Organize content in Notion's tree structure
- Search returns page URLs for easy access

## Usage Examples

### Example 1: Create Research Page
```
Create a Notion page titled "Manim Animation Guide" with this content:
# Manim Animation Guide
## Overview
This guide covers creating mathematical animations.

### Key Concepts
- Vector spaces
- Transformations
- 3D visualizations

```python
# Example code
scene = Scene()
```
```

### Example 2: Sync Research Workflow
```
1. Search Notion for existing "Research Log" page
2. Sync today's Obsidian daily note to that page
3. Add new findings to the Research Database
```

### Example 3: Organize by Topic
```
Create a new page "Gyrovector Addition" under the "Gyrovector Theory" parent page with diagrams and equations
```

## Integration with Other Tools

### Obsidian → Notion Pipeline
1. Create atomic notes in Obsidian
2. Process and develop ideas
3. Sync polished content to Notion for sharing

### Manim → Notion
1. Create animation with custom output path
2. Create Notion page with embedded video link
3. Add explanation and equations

### Research → Publication
1. Collect research in Obsidian
2. Sync summaries to Notion
3. Collaborate with others
4. Export for publication

## Total Tools Now: 37!
- 8 Dropbox file operations
- 7 GitHub operations  
- 4 Research discovery tools
- 4 Mathematical visualization tools
- 4 Knowledge management tools
- 4 Research coordination tools
- **6 Notion operations** ✨

## Important Notes

1. **Permissions**: You must share pages/databases with your integration
2. **Parent Pages**: When creating pages, you need a parent page ID (use search to find)
3. **Rate Limits**: Notion API has rate limits - avoid rapid bulk operations
4. **Content Types**: Currently supports text/markdown (images via URLs only)

## Troubleshooting

- **"Parent page ID required"**: Use search_notion to find a page to create under
- **"Unauthorized"**: Make sure page is shared with your integration
- **"Not found"**: Check that the page/database ID is correct

Happy Notion integration! 🚀