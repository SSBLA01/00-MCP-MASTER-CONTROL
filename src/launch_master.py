#!/usr/bin/env python
"""Launch script for Master Coordinator"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.servers.master_coordinator import main

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())