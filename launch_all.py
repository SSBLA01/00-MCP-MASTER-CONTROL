#!/usr/bin/env python
"""Launch all MCP servers"""
import subprocess
import sys
import time
from pathlib import Path

def launch_servers():
    """Launch all MCP servers in separate processes"""
    servers = [
        "src/launch_master.py",
        "src/launch_discovery.py",
        "src/launch_visualization.py",
        "src/launch_ingestion.py"
    ]
    
    processes = []
    
    for server in servers:
        print(f"Launching {server}...")
        process = subprocess.Popen([sys.executable, server])
        processes.append(process)
        time.sleep(2)  # Give each server time to start
    
    print("All servers launched. Press Ctrl+C to stop.")
    
    try:
        # Wait for all processes
        for process in processes:
            process.wait()
    except KeyboardInterrupt:
        print("\nShutting down servers...")
        for process in processes:
            process.terminate()
        print("All servers stopped.")

if __name__ == "__main__":
    launch_servers()