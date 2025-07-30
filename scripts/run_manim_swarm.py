#!/usr/bin/env python3
"""
Run Manim Swarm - Quick command to deploy the pattern discovery system
Usage:
    python run_manim_swarm.py --concept gyrovector
    python run_manim_swarm.py --batch
    python run_manim_swarm.py --full-scan
"""

import argparse
import asyncio
import json
from datetime import datetime
from pathlib import Path

# Add src to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from manim_swarm import ManimSwarm, run_manim_swarm

def main():
    parser = argparse.ArgumentParser(
        description="Deploy the Manim Swarm to discover animation patterns from GitHub"
    )
    
    # Command options
    parser.add_argument(
        "--concept",
        type=str,
        default=None,
        help="Specific mathematical concept to search for (e.g., gyrovector, topology)"
    )
    
    parser.add_argument(
        "--batch",
        action="store_true",
        help="Run batch discovery for common concepts"
    )
    
    parser.add_argument(
        "--full-scan",
        action="store_true",
        help="Run full swarm deployment across all categories"
    )
    
    parser.add_argument(
        "--max-patterns",
        type=int,
        default=20,
        help="Maximum number of patterns to discover per category"
    )
    
    parser.add_argument(
        "--output",
        type=str,
        default="manim_swarm_report.json",
        help="Output file for the discovery report"
    )
    
    args = parser.parse_args()
    
    print(f"""
╔═══════════════════════════════════════════════════════════╗
║                      MANIM SWARM                          ║
║         GitHub-Wide Animation Pattern Discovery           ║
╚═══════════════════════════════════════════════════════════╝
    """)
    
    if args.full_scan:
        print("🚀 Deploying FULL MANIM SWARM across all categories...")
        print("This may take several minutes.\n")
        
        # Run full deployment
        patterns = asyncio.run(run_manim_swarm(deploy_full=True))
        
    elif args.batch:
        print("📦 Running BATCH DISCOVERY for common concepts...")
        
        batch_concepts = ["gyrovector", "topology", "geometry", "calculus"]
        all_patterns = []
        
        for concept in batch_concepts:
            print(f"\n{'='*60}")
            print(f"Discovering: {concept.upper()}")
            print('='*60)
            
            patterns = asyncio.run(run_manim_swarm(concept, deploy_full=False))
            all_patterns.extend(patterns)
        
        patterns = all_patterns
        
    elif args.concept:
        print(f"🔍 Searching for {args.concept.upper()} patterns...")
        
        patterns = asyncio.run(run_manim_swarm(args.concept, deploy_full=False))
        
    else:
        print("❌ Please specify --concept, --batch, or --full-scan")
        parser.print_help()
        return
    
    # Generate report
    if patterns:
        report = {
            "deployment_date": datetime.now().isoformat(),
            "mode": "full-scan" if args.full_scan else "batch" if args.batch else "single",
            "concept": args.concept if args.concept else "multiple",
            "patterns_discovered": len(patterns),
            "patterns": [
                {
                    "id": p.pattern_id,
                    "concept": p.mathematical_concept,
                    "source": p.source_url,
                    "quality": p.quality_score,
                    "reusability": p.reusability
                }
                for p in patterns
            ]
        }
        
        # Save report
        with open(args.output, "w") as f:
            json.dump(report, f, indent=2)
        
        print(f"\n✅ Report saved to: {args.output}")
        
        # Generate MCP commands
        print("\n" + "="*60)
        print("MCP INTEGRATION COMMANDS")
        print("="*60)
        print("\nExecute these in Claude Desktop to integrate patterns:\n")
        
        for i, pattern in enumerate(patterns[:3], 1):
            print(f"{i}. Fetch and analyze pattern:")
            print(f'   web_fetch("{pattern.source_url}")')
            print(f'   gemini_analyze_code(code=fetched_code, analysis_type="quality")\n')
        
        print("\nTo save all patterns to Obsidian:")
        print("   # Run after fetching patterns")
        print("   for pattern in discovered_patterns:")
        print('       ingest_to_obsidian(content=pattern.to_obsidian_note(), '
              'title=f"Manim Pattern - {pattern.mathematical_concept}", '
              'category="concepts")')
        
        # Show summary statistics
        print("\n" + "="*60)
        print("DISCOVERY SUMMARY")
        print("="*60)
        
        # Count by concept
        concept_counts = {}
        for p in patterns:
            concept = p.mathematical_concept
            concept_counts[concept] = concept_counts.get(concept, 0) + 1
        
        print("\nPatterns by Concept:")
        for concept, count in sorted(concept_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  • {concept}: {count}")
        
        # Quality distribution
        high_quality = sum(1 for p in patterns if p.quality_score >= 0.8)
        medium_quality = sum(1 for p in patterns if 0.6 <= p.quality_score < 0.8)
        low_quality = sum(1 for p in patterns if p.quality_score < 0.6)
        
        print(f"\nQuality Distribution:")
        print(f"  • High Quality (≥0.8): {high_quality}")
        print(f"  • Medium Quality (0.6-0.8): {medium_quality}")
        print(f"  • Low Quality (<0.6): {low_quality}")
        
        # Reusability
        high_reuse = sum(1 for p in patterns if p.reusability == "high")
        print(f"\nHighly Reusable Patterns: {high_reuse}/{len(patterns)}")
        
    else:
        print("\n❌ No patterns discovered. Try different search terms or check your connection.")

    print("\n🎯 Manim Swarm deployment complete!")


if __name__ == "__main__":
    main()
