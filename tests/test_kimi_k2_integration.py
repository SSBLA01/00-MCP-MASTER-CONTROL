#!/usr/bin/env python3
"""
Test script for Kimi K2 integration
"""

import asyncio
import os
from groq import AsyncGroq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_groq_api():
    """Test basic Groq API connection with Kimi K2"""
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        print("❌ GROQ_API_KEY not found in environment variables")
        return False
    
    print(f"✅ Found GROQ_API_KEY: {api_key[:10]}...")
    
    try:
        client = AsyncGroq(api_key=api_key)
        
        # Test with a simple mathematical query
        response = await client.chat.completions.create(
            model="moonshotai/kimi-k2-instruct",
            messages=[
                {
                    "role": "system",
                    "content": "You are a mathematical reasoning expert."
                },
                {
                    "role": "user",
                    "content": "What is the gyroaddition of [0.3, 0.4, 0] and [0.1, 0.2, 0.5] in the Möbius gyrovector space?"
                }
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        print("✅ Successfully connected to Kimi K2 via Groq API")
        print("\nResponse:")
        print(response.choices[0].message.content)
        print(f"\nTokens used: {response.usage.total_tokens}")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

async def test_mathematical_reasoning():
    """Test more complex mathematical reasoning"""
    api_key = os.getenv("GROQ_API_KEY")
    client = AsyncGroq(api_key=api_key)
    
    try:
        response = await client.chat.completions.create(
            model="moonshotai/kimi-k2-instruct",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert in gyrovector spaces and recursive harmonic analysis."
                },
                {
                    "role": "user",
                    "content": """Explain the relationship between:
1. Möbius gyrovector spaces
2. Recursive harmonic analysis on lattices
3. Applications to orbifold theory

Provide a concrete example showing how these concepts connect."""
                }
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        print("\n" + "="*50)
        print("Mathematical Reasoning Test")
        print("="*50)
        print(response.choices[0].message.content)
        print(f"\nTokens used: {response.usage.total_tokens}")
        return True
        
    except Exception as e:
        print(f"❌ Mathematical reasoning test failed: {e}")
        return False

async def main():
    """Run all tests"""
    print("Testing Kimi K2 Integration")
    print("="*50)
    
    # Test 1: Basic API connection
    if await test_groq_api():
        print("\n✅ Basic API test passed")
    else:
        print("\n❌ Basic API test failed")
        return
    
    # Test 2: Mathematical reasoning
    await asyncio.sleep(1)  # Rate limiting
    if await test_mathematical_reasoning():
        print("\n✅ Mathematical reasoning test passed")
    else:
        print("\n❌ Mathematical reasoning test failed")
    
    print("\n" + "="*50)
    print("All tests completed!")
    print("\nNext steps:")
    print("1. Restart Claude Desktop to load the new tools")
    print("2. Try: 'Use kimi_k2_query to explain gyrovector spaces'")
    print("3. Try: 'Use kimi_k2_solve_problem to calculate [0.3,0.4,0] ⊕ [0.1,0.2,0.5]'")

if __name__ == "__main__":
    asyncio.run(main())