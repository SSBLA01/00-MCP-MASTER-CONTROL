#!/usr/bin/env python
"""Launch script for Research Discovery Agent"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.servers.research_discovery import main

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())