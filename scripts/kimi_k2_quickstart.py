#!/usr/bin/env python3
"""
Kimi K2 Integration Quick Start Script
=====================================

This script helps you quickly test and explore the Kimi K2 integration
with example queries and visualizations.
"""

import asyncio
import os
import json
import sys
from datetime import datetime

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from src.servers.kimi_k2_integration import KimiK2Agent, KimiK2Config
    from dotenv import load_dotenv
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Please ensure you're in the project directory and dependencies are installed.")
    sys.exit(1)

# Load environment variables
load_dotenv()

# Example queries and problems
EXAMPLES = {
    "basic_query": {
        "description": "Basic mathematical query",
        "prompt": "Explain the fundamental theorem of gyrovector spaces and its implications for hyperbolic geometry"
    },
    "gyrovector_calculation": {
        "description": "Gyrovector calculation with validation",
        "problem": """
        In the Poincaré ball model with c=1, calculate:
        1. u ⊕ v where u = [0.3, 0.4, 0] and v = [0.1, 0.2, 0.5]
        2. Verify ||u ⊕ v|| < 1
        3. Calculate the gyrodistance d(u, v)
        """,
        "domain": "gyrovector"
    },
    "lattice_problem": {
        "description": "Lattice theory problem",
        "problem": "Prove that every finite lattice has a greatest element (top) and a least element (bottom)",
        "domain": "lattice"
    },
    "visualization": {
        "description": "Generate Manim visualization code",
        "concept": "Gyrovector addition in the Poincaré disk model showing geodesic paths",
        "animation_type": "geometric_construction"
    },
    "recursive_harmonic": {
        "description": "Recursive harmonic analysis",
        "problem": "Analyze the harmonic structure of the Sierpinski gasket using recursive decomposition",
        "domain": "harmonic"
    },
    "orbifold": {
        "description": "Orbifold computation",
        "problem": "Calculate the orbifold Euler characteristic of the quotient of the 2-sphere by the icosahedral group action",
        "domain": "orbifold"
    }
}

class KimiK2QuickStart:
    def __init__(self):
        # Check for API key
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            print("❌ GROQ_API_KEY not found in environment variables")
            print("Please add it to your .env file:")
            print("GROQ_API_KEY=your_api_key_here")
            sys.exit(1)
        
        # Initialize Kimi K2
        self.config = KimiK2Config(groq_api_key=api_key)
        self.agent = KimiK2Agent(self.config)
        print("✅ Kimi K2 initialized successfully")
    
    async def run_example(self, example_name: str):
        """Run a specific example"""
        if example_name not in EXAMPLES:
            print(f"❌ Unknown example: {example_name}")
            print(f"Available examples: {', '.join(EXAMPLES.keys())}")
            return
        
        example = EXAMPLES[example_name]
        print(f"\n{'='*60}")
        print(f"Running: {example['description']}")
        print(f"{'='*60}\n")
        
        try:
            if example_name == "basic_query":
                result = await self.agent.query(example["prompt"])
                
            elif example_name in ["gyrovector_calculation", "lattice_problem", 
                                 "recursive_harmonic", "orbifold"]:
                result = await self.agent.solve_mathematical_problem(
                    problem=example["problem"],
                    domain=example["domain"],
                    validate=True
                )
                
            elif example_name == "visualization":
                result = await self.agent.generate_manim_code(
                    concept=example["concept"],
                    animation_type=example["animation_type"]
                )
                
                # Save the generated code if successful
                if result.get("status") == "success" and result.get("manim_code"):
                    output_dir = "generated_animations"
                    os.makedirs(output_dir, exist_ok=True)
                    
                    file_path = os.path.join(output_dir, result["file_name"])
                    with open(file_path, "w") as f:
                        f.write(result["manim_code"])
                    
                    print(f"✅ Manim code saved to: {file_path}")
                    print("\nTo render the animation, run:")
                    print(f"manim -pql {file_path}")
            
            # Display results
            if result.get("status") == "success":
                print("✅ Success!\n")
                print("Response:")
                print("-" * 40)
                print(result.get("content", "No content"))
                
                if result.get("validation"):
                    print("\nValidation:")
                    print("-" * 40)
                    print(result["validation"].get("content", "No validation content"))
                
                print(f"\nMetadata:")
                print(f"- Duration: {result['metadata'].get('duration_ms', 'N/A')} ms")
                print(f"- Tokens: {result['metadata'].get('tokens', {}).get('total', 'N/A')}")
                
            else:
                print(f"❌ Error: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
    
    async def interactive_mode(self):
        """Run in interactive mode"""
        print("\n🚀 Kimi K2 Interactive Mode")
        print("Type 'help' for commands, 'exit' to quit\n")
        
        while True:
            try:
                user_input = input("kimi> ").strip()
                
                if user_input.lower() == "exit":
                    break
                    
                elif user_input.lower() == "help":
                    print("\nAvailable commands:")
                    print("- help: Show this help")
                    print("- examples: List available examples")
                    print("- run <example>: Run a specific example")
                    print("- query <prompt>: Send a custom query")
                    print("- solve <problem>: Solve a mathematical problem")
                    print("- visualize <concept>: Generate visualization code")
                    print("- exit: Quit\n")
                    
                elif user_input.lower() == "examples":
                    print("\nAvailable examples:")
                    for name, example in EXAMPLES.items():
                        print(f"- {name}: {example['description']}")
                    print()
                    
                elif user_input.startswith("run "):
                    example_name = user_input[4:].strip()
                    await self.run_example(example_name)
                    
                elif user_input.startswith("query "):
                    prompt = user_input[6:].strip()
                    result = await self.agent.query(prompt)
                    print(f"\n{result.get('content', 'No response')}\n")
                    
                elif user_input.startswith("solve "):
                    problem = user_input[6:].strip()
                    result = await self.agent.solve_mathematical_problem(problem)
                    print(f"\n{result.get('content', 'No solution')}\n")
                    
                elif user_input.startswith("visualize "):
                    concept = user_input[10:].strip()
                    result = await self.agent.generate_manim_code(concept)
                    if result.get("manim_code"):
                        print(f"\n✅ Generated Manim code for: {concept}")
                        print("Code preview:")
                        print("-" * 40)
                        print(result["manim_code"][:500] + "..." if len(result["manim_code"]) > 500 else result["manim_code"])
                    else:
                        print("❌ Failed to generate visualization code")
                    
                elif user_input:
                    print("Unknown command. Type 'help' for available commands.")
                    
            except KeyboardInterrupt:
                print("\n\nExiting...")
                break
            except Exception as e:
                print(f"Error: {e}")
    
    async def benchmark_performance(self):
        """Run a simple performance benchmark"""
        print("\n⏱️  Running Performance Benchmark...")
        
        test_queries = [
            "What is 2+2?",
            "Explain the Pythagorean theorem",
            "Calculate the derivative of x^2 + 3x + 1",
            "What is the fundamental theorem of calculus?",
            "Solve the equation x^2 - 5x + 6 = 0"
        ]
        
        total_time = 0
        total_tokens = 0
        
        for i, query in enumerate(test_queries, 1):
            print(f"\nQuery {i}/{len(test_queries)}: {query[:50]}...")
            result = await self.agent.query(query)
            
            if result.get("status") == "success":
                duration = result["metadata"].get("duration_ms", 0)
                tokens = result["metadata"].get("tokens", {}).get("total", 0)
                
                total_time += duration
                total_tokens += tokens
                
                print(f"✅ Completed in {duration}ms ({tokens} tokens)")
            else:
                print("❌ Failed")
        
        if total_tokens > 0:
            avg_time = total_time / len(test_queries)
            tokens_per_second = (total_tokens / total_time) * 1000 if total_time > 0 else 0
            
            print(f"\n📊 Benchmark Results:")
            print(f"- Average response time: {avg_time:.2f}ms")
            print(f"- Total tokens processed: {total_tokens}")
            print(f"- Tokens per second: {tokens_per_second:.2f}")
        else:
            print("\n❌ Benchmark failed - no successful queries")

async def main():
    """Main entry point"""
    quickstart = KimiK2QuickStart()
    
    print("\n🎯 Kimi K2 Integration Quick Start")
    print("==================================\n")
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "benchmark":
            await quickstart.benchmark_performance()
            
        elif command == "interactive":
            await quickstart.interactive_mode()
            
        elif command in EXAMPLES:
            await quickstart.run_example(command)
            
        elif command == "all":
            # Run all examples
            for example_name in EXAMPLES:
                await quickstart.run_example(example_name)
                await asyncio.sleep(1)  # Brief pause between examples
        else:
            print(f"Unknown command: {command}")
            print("\nUsage:")
            print("  python kimi_k2_quickstart.py [command]")
            print("\nCommands:")
            print("  benchmark    - Run performance benchmark")
            print("  interactive  - Start interactive mode")
            print("  all         - Run all examples")
            print("  <example>   - Run specific example")
            print(f"\nExamples: {', '.join(EXAMPLES.keys())}")
    else:
        # Default: run interactive mode
        await quickstart.interactive_mode()

if __name__ == "__main__":
    asyncio.run(main())
