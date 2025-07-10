"""
Common utilities for MCP servers
"""
import os
import logging
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
def setup_logging(name: str) -> logging.Logger:
    """Setup logging for MCP server"""
    log_level = os.getenv('LOG_LEVEL', 'INFO')
    
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level))
    
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger

# Path utilities
def ensure_directory(path: str) -> Path:
    """Ensure directory exists"""
    dir_path = Path(path)
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path

# Configuration loader
def load_config() -> Dict[str, Any]:
    """Load configuration from environment and files"""
    return {
        'api_keys': {
            'perplexity': os.getenv('PERPLEXITY_API_KEY', ''),
            'wolfram': os.getenv('WOLFRAM_ALPHA_APP_ID', ''),
            'dropbox_app_key': os.getenv('DROPBOX_APP_KEY', ''),
            'dropbox_app_secret': os.getenv('DROPBOX_APP_SECRET', ''),
            'dropbox_access_token': os.getenv('DROPBOX_ACCESS_TOKEN', ''),
            'github': os.getenv('GITHUB_TOKEN', '')
        },
        'paths': {
            'obsidian_vault': os.getenv('OBSIDIAN_VAULT_PATH', './data/obsidian_vault'),
            'manim_output': os.getenv('MANIM_OUTPUT_DIR', './data/manim_outputs'),
            'dropbox_base': os.getenv('DROPBOX_BASE_PATH', '/MathematicalResearch')
        },
        'settings': {
            'manim_quality': os.getenv('MANIM_QUALITY', 'medium_quality'),
            'log_level': os.getenv('LOG_LEVEL', 'INFO')
        }
    }