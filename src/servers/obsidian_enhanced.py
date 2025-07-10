#!/usr/bin/env python3
"""
Enhanced Obsidian integration for atomic Zettelkasten notes
Maps to your existing folder structure
"""

from datetime import datetime
from typing import Dict, Any, List, Optional
import re

# Your Obsidian folder structure mapping
OBSIDIAN_FOLDERS = {
    "sources": "01_Sources",
    "literature": "02_Literature_Notes", 
    "permanent": "03_Permanent_Notes",
    "index": "04_Index",
    "patterns": "05_Patterns",
    "insights": "06_Insights",
    "synthesis": "07_Synthesis",
    "visualizations": "08_Visualizations",
    "daily": "09_Daily_Notes",
    "templates": "10_Templates",
    # Legacy folders (for backward compatibility)
    "concepts": "03_Permanent_Notes",  # Map concepts to permanent notes
    "papers": "02_Literature_Notes",   # Map papers to literature notes
    "daily_notes": "09_Daily_Notes"    # Map to numbered daily notes
}

def generate_zettel_id() -> str:
    """Generate a unique Zettelkasten ID based on timestamp"""
    return datetime.now().strftime("%Y%m%d%H%M%S")

def format_zettel_title(zettel_id: str, title: str) -> str:
    """Format title in Zettelkasten style"""
    # Remove special characters for filename
    safe_title = re.sub(r'[^\w\s-]', '', title)
    safe_title = re.sub(r'[-\s]+', '_', safe_title)
    return f"{zettel_id}_{safe_title}"

async def create_atomic_note(
    content: str,
    title: str,
    note_type: str = "permanent",
    tags: List[str] = None,
    links: List[str] = None,
    source: Optional[str] = None
) -> Dict[str, Any]:
    """Create an atomic Zettelkasten note"""
    from src.servers.knowledge_ingestion import ingest_to_obsidian
    
    zettel_id = generate_zettel_id()
    
    # Determine folder based on note type
    folder_mapping = {
        "source": "sources",
        "literature": "literature",
        "permanent": "permanent",
        "pattern": "patterns",
        "insight": "insights",
        "synthesis": "synthesis",
        "daily": "daily"
    }
    
    category = folder_mapping.get(note_type, "permanent")
    
    # Build metadata
    metadata = {
        "zettel_id": zettel_id,
        "note_type": note_type,
        "atomic": True,
        "created_by": "Dobbs-MCP"
    }
    
    if source:
        metadata["source"] = source
    
    # Enhance content with Zettelkasten structure
    enhanced_content = f"""## Atomic Idea

{content}

## Development
<!-- Space for developing this idea further -->

## Questions
<!-- What questions does this raise? -->

## Implications
<!-- What does this mean for other ideas? -->
"""
    
    # Format title
    formatted_title = format_zettel_title(zettel_id, title)
    
    # Create the note
    result = await ingest_to_obsidian(
        content=enhanced_content,
        title=formatted_title,
        category=category,
        tags=tags or ["atomic-note"],
        links=links or [],
        metadata=metadata
    )
    
    return {
        **result,
        "zettel_id": zettel_id,
        "formatted_title": formatted_title
    }

async def create_literature_note(
    source_title: str,
    author: str,
    content: str,
    source_type: str = "article",
    year: Optional[int] = None,
    tags: List[str] = None,
    related_notes: List[str] = None
) -> Dict[str, Any]:
    """Create a literature note from a source"""
    
    zettel_id = generate_zettel_id()
    
    # Build structured literature note
    literature_content = f"""## Source Information
- **Title**: {source_title}
- **Author**: {author}
- **Type**: {source_type}
- **Year**: {year or 'Unknown'}
- **Zettel ID**: {zettel_id}

## Summary
{content}

## Key Concepts
<!-- Extract main concepts as bullet points -->

## Notable Quotes
<!-- Important quotes with page numbers -->

## My Analysis
<!-- Personal thoughts and connections -->

## Questions Raised
<!-- What questions does this source raise? -->

## Action Items
<!-- Follow-up reading or research needed -->
"""
    
    # Create the note
    result = await create_atomic_note(
        content=literature_content,
        title=f"{author} - {source_title}",
        note_type="literature",
        tags=tags or ["literature-note", source_type],
        links=related_notes
    )
    
    return result

async def create_pattern_note(
    pattern_name: str,
    description: str,
    examples: List[str],
    category: str = "general",
    tags: List[str] = None
) -> Dict[str, Any]:
    """Create a pattern recognition note"""
    
    # Build pattern content
    examples_text = "\n".join([f"- {ex}" for ex in examples])
    
    pattern_content = f"""## Pattern: {pattern_name}

### Description
{description}

### Category
{category}

### Examples
{examples_text}

### Connections
<!-- How does this pattern relate to others? -->

### Applications
<!-- Where can this pattern be applied? -->

### Counter-Examples
<!-- When does this pattern NOT apply? -->
"""
    
    result = await create_atomic_note(
        content=pattern_content,
        title=f"Pattern - {pattern_name}",
        note_type="pattern",
        tags=tags or ["pattern", category],
        links=[]
    )
    
    return result

async def update_daily_note(
    content: str,
    section: str = "captured"
) -> Dict[str, Any]:
    """Add content to today's daily note"""
    from src.servers.knowledge_ingestion import ingest_to_obsidian
    from pathlib import Path
    import aiofiles
    
    # Get today's date
    today = datetime.now().strftime("%Y-%m-%d")
    vault_path = "/Users/scottbroock/Dropbox/01_Totem_Networks/04_Obsidian"
    daily_path = Path(vault_path) / "09_Daily_Notes" / f"{today}.md"
    
    # Check if daily note exists
    if daily_path.exists():
        # Read existing content
        async with aiofiles.open(daily_path, 'r', encoding='utf-8') as f:
            existing_content = await f.read()
        
        # Find the section or append
        section_headers = {
            "captured": "## 📝 Captured Ideas",
            "insights": "## 💡 Insights", 
            "questions": "## ❓ Questions",
            "tasks": "## 🔄 Tasks"
        }
        
        header = section_headers.get(section, "## 📝 Captured Ideas")
        
        if header in existing_content:
            # Insert after the header
            parts = existing_content.split(header)
            new_content = parts[0] + header + f"\n- {content}\n" + parts[1]
        else:
            # Append to end
            new_content = existing_content + f"\n\n{header}\n- {content}\n"
        
        # Write back
        async with aiofiles.open(daily_path, 'w', encoding='utf-8') as f:
            await f.write(new_content)
        
        return {
            "status": "updated",
            "file_path": str(daily_path),
            "section": section
        }
    else:
        # Create new daily note
        daily_content = f"""# {datetime.now().strftime('%A, %B %d, %Y')}

## 🎯 Focus


## 📝 Captured Ideas
- {content}

## 💡 Insights


## ❓ Questions


## 🔄 Tasks
- [ ] Review and process captured ideas
- [ ] Create permanent notes from insights

## 🔗 Created Notes


## 📚 Reading List


---
*Daily note created by Dobbs-MCP*
"""
        
        result = await ingest_to_obsidian(
            content=daily_content,
            title=today,
            category="daily",
            tags=["daily-note"],
            links=[],
            metadata={"type": "daily_note"}
        )
        
        return result

# Export enhanced functions
__all__ = [
    'create_atomic_note',
    'create_literature_note', 
    'create_pattern_note',
    'update_daily_note',
    'generate_zettel_id',
    'OBSIDIAN_FOLDERS'
]