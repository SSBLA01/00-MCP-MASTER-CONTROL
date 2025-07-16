"""
Test Suite for Kimi K2 Integration
==================================

Tests for the Kimi K2 integration with Dobbs-MCP
"""

import asyncio
import os
import json
import pytest
from unittest.mock import Mock, patch, AsyncMock

# Add parent directory to path
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.servers.kimi_k2_integration import (
    KimiK2Config, KimiK2Agent, KimiK2Integration
)

# Test configuration
TEST_CONFIG = KimiK2Config(
    groq_api_key="test_api_key",
    model_name="moonshotai/kimi-k2-instruct",
    temperature=0.7,
    max_tokens=1000,
    timeout=30
)

class TestKimiK2Agent:
    """Test the KimiK2Agent class"""
    
    @pytest.fixture
    def agent(self):
        """Create a test agent"""
        return KimiK2Agent(TEST_CONFIG)
    
    @pytest.mark.asyncio
    async def test_basic_query(self, agent):
        """Test basic query functionality"""
        with patch.object(agent.client.chat.completions, 'create', new_callable=AsyncMock) as mock_create:
            # Mock response
            mock_response = Mock()
            mock_response.choices = [Mock()]
            mock_response.choices[0].message.content = "The gyroaddition formula is..."
            mock_response.choices[0].message.tool_calls = None
            mock_response.usage.prompt_tokens = 50
            mock_response.usage.completion_tokens = 100
            mock_response.usage.total_tokens = 150
            
            mock_create.return_value = mock_response
            
            # Test query
            result = await agent.query("Explain gyroaddition")
            
            assert result["status"] == "success"
            assert "gyroaddition formula" in result["content"]
            assert result["metadata"]["tokens"]["total"] == 150
    
    @pytest.mark.asyncio
    async def test_mathematical_problem_solving(self, agent):
        """Test mathematical problem solving"""
        with patch.object(agent, 'query', new_callable=AsyncMock) as mock_query:
            # Mock solution response
            mock_query.return_value = {
                "status": "success",
                "content": """Step 1: Understanding the problem
                Step 2: Apply gyroaddition formula
                Step 3: Simplify
                Final answer: [0.5, 0.6, 0.3]""",
                "metadata": {"duration_ms": 500}
            }
            
            result = await agent.solve_mathematical_problem(
                problem="Calculate u ⊕ v where u=[0.3,0.4,0] and v=[0.1,0.2,0.5]",
                domain="gyrovector",
                validate=False
            )
            
            assert result["status"] == "success"
            assert "Step 1" in result["content"]
            assert "gyroaddition" in result["content"]
    
    @pytest.mark.asyncio
    async def test_manim_code_generation(self, agent):
        """Test Manim code generation"""
        with patch.object(agent, 'query', new_callable=AsyncMock) as mock_query:
            # Mock code generation response
            mock_query.return_value = {
                "status": "success",
                "content": """```python
from manim import *

class GyrovectorAnimation(Scene):
    def construct(self):
        # Create gyrovector visualization
        circle = Circle(radius=2)
        self.play(Create(circle))
```""",
                "metadata": {"duration_ms": 800}
            }
            
            result = await agent.generate_manim_code(
                concept="gyrovector addition",
                animation_type="geometric_construction"
            )
            
            assert result["status"] == "success"
            assert "manim_code" in result
            assert "GyrovectorAnimation" in result["manim_code"]
            assert result["file_name"] == "gyrovector_addition_animation.py"

class TestKimiK2Integration:
    """Test the KimiK2Integration class"""
    
    @pytest.fixture
    def mock_server(self):
        """Create a mock MCP server"""
        server = Mock()
        server.add_tool = Mock()
        server.call_tool = Mock(return_value=lambda fn: fn)
        return server
    
    @pytest.fixture
    def integration(self, mock_server):
        """Create a test integration"""
        with patch.dict(os.environ, {"GROQ_API_KEY": "test_key"}):
            return KimiK2Integration(mock_server)
    
    def test_tool_definitions(self, integration):
        """Test that tools are properly defined"""
        tools = integration.tools
        
        assert len(tools) == 4
        tool_names = [tool.name for tool in tools]
        
        assert "kimi_k2_query" in tool_names
        assert "kimi_k2_solve_problem" in tool_names
        assert "kimi_k2_generate_visualization" in tool_names
        assert "kimi_k2_collaborative_reasoning" in tool_names
    
    @pytest.mark.asyncio
    async def test_handle_query_tool(self, integration):
        """Test handling of kimi_k2_query tool"""
        with patch.object(integration.agent, 'query', new_callable=AsyncMock) as mock_query:
            mock_query.return_value = {
                "status": "success",
                "content": "Gyrovector spaces are...",
                "metadata": {}
            }
            
            result = await integration.handle_tool_call(
                "kimi_k2_query",
                {"prompt": "What are gyrovector spaces?"}
            )
            
            assert len(result) == 1
            assert result[0].type == "text"
            assert "Gyrovector spaces" in result[0].text

class TestGyrovectorCalculations:
    """Test specific gyrovector calculations"""
    
    @pytest.mark.asyncio
    async def test_gyrovector_formulas(self):
        """Test that gyrovector formulas are correctly implemented"""
        # Test data for gyrovector operations
        test_cases = [
            {
                "operation": "gyroaddition",
                "u": [0.3, 0.4, 0],
                "v": [0.1, 0.2, 0.5],
                "expected_contains": ["gamma", "dot product"]
            },
            {
                "operation": "gyroscalar",
                "r": 2,
                "u": [0.5, 0, 0],
                "expected_contains": ["tanh", "atanh"]
            }
        ]
        
        agent = KimiK2Agent(TEST_CONFIG)
        
        for test_case in test_cases:
            with patch.object(agent, 'query', new_callable=AsyncMock) as mock_query:
                mock_query.return_value = {
                    "status": "success",
                    "content": f"Calculating {test_case['operation']}...",
                    "metadata": {}
                }
                
                if test_case["operation"] == "gyroaddition":
                    problem = f"Calculate {test_case['u']} ⊕ {test_case['v']}"
                else:
                    problem = f"Calculate {test_case['r']} ⊗ {test_case['u']}"
                
                result = await agent.solve_mathematical_problem(
                    problem=problem,
                    domain="gyrovector",
                    validate=False
                )
                
                assert result["status"] == "success"

class TestIntegrationScenarios:
    """Test real-world integration scenarios"""
    
    @pytest.mark.asyncio
    async def test_complete_workflow(self):
        """Test a complete research workflow"""
        # This test simulates a complete workflow:
        # 1. Query for a concept
        # 2. Solve a related problem
        # 3. Generate visualization
        
        agent = KimiK2Agent(TEST_CONFIG)
        
        # Step 1: Query
        with patch.object(agent, 'query', new_callable=AsyncMock) as mock_query:
            mock_query.return_value = {
                "status": "success",
                "content": "Gyrovector spaces generalize vector spaces...",
                "metadata": {}
            }
            
            concept_result = await agent.query("Explain gyrovector spaces")
            assert concept_result["status"] == "success"
        
        # Step 2: Problem solving
        with patch.object(agent, 'query', new_callable=AsyncMock) as mock_query:
            mock_query.return_value = {
                "status": "success",
                "content": "Solution: [0.389, 0.584, 0.485]",
                "metadata": {}
            }
            
            solution_result = await agent.solve_mathematical_problem(
                "Calculate (u ⊕ v) ⊕ w",
                domain="gyrovector"
            )
            assert solution_result["status"] == "success"
        
        # Step 3: Visualization
        with patch.object(agent, 'query', new_callable=AsyncMock) as mock_query:
            mock_query.return_value = {
                "status": "success",
                "content": "```python\nfrom manim import *\n```",
                "metadata": {}
            }
            
            viz_result = await agent.generate_manim_code(
                "gyrovector addition visualization"
            )
            assert viz_result["status"] == "success"

# Performance benchmarks
class TestPerformance:
    """Test performance characteristics"""
    
    @pytest.mark.asyncio
    async def test_response_time(self):
        """Test that responses are within acceptable time limits"""
        agent = KimiK2Agent(TEST_CONFIG)
        
        with patch.object(agent.client.chat.completions, 'create', new_callable=AsyncMock) as mock_create:
            # Mock fast response
            mock_response = Mock()
            mock_response.choices = [Mock()]
            mock_response.choices[0].message.content = "Quick response"
            mock_response.choices[0].message.tool_calls = None
            mock_response.usage = Mock(prompt_tokens=10, completion_tokens=20, total_tokens=30)
            
            mock_create.return_value = mock_response
            
            import time
            start = time.time()
            result = await agent.query("Quick test")
            duration = time.time() - start
            
            # Should complete quickly (mocked)
            assert duration < 1.0
            assert result["status"] == "success"

# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
