#!/usr/bin/env python
"""Launch script for Knowledge Ingestion Agent"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.servers.knowledge_ingestion import main

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())