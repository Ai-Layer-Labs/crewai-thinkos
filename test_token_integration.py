"""Test script to verify CrewAI token storage integration"""
import asyncio
import sys
import os

# Add backend to path to import token manager
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from crewai import Agent, Task, Crew
from backend.services.llm.token_manager import get_token_manager


async def test_token_integration():
    """Test that CrewAI can use tokens from secure storage"""
    print("🔧 Testing CrewAI Token Storage Integration...")
    
    # Get token manager
    token_manager = await get_token_manager()
    print("✅ Token manager initialized")
    
    # Create an agent with token manager
    researcher = Agent(
        role="Researcher",
        goal="Research the latest AI developments",
        backstory="You are an expert AI researcher with deep knowledge of the field",
        llm="gpt-4",  # Will use token from storage
        token_manager=token_manager,
        verbose=True
    )
    print("✅ Agent created with token manager")
    
    # Create a task
    research_task = Task(
        description="Research the latest developments in AI safety and summarize key findings",
        expected_output="A brief summary of recent AI safety developments",
        agent=researcher
    )
    print("✅ Task created")
    
    # Create crew with token manager
    crew = Crew(
        agents=[researcher],
        tasks=[research_task],
        token_manager=token_manager,
        verbose=True
    )
    print("✅ Crew created with token manager")
    
    # Test that agent received token manager
    if hasattr(researcher, 'token_manager') and researcher.token_manager:
        print("✅ Agent has token manager")
    else:
        print("❌ Agent does not have token manager")
    
    # Test LLM creation
    print("\n🔧 Testing LLM creation...")
    try:
        # Trigger LLM initialization
        result = crew.kickoff()
        print(f"\n✅ Crew execution successful!")
        print(f"Result: {result}")
        return True
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False


async def test_multiple_providers():
    """Test using multiple LLM providers with token storage"""
    print("\n🔧 Testing Multiple Providers...")
    
    token_manager = await get_token_manager()
    
    # Create agents with different providers
    agents = []
    
    # OpenAI agent
    try:
        openai_agent = Agent(
            role="OpenAI Analyst",
            goal="Analyze data using OpenAI models",
            backstory="Expert analyst using GPT models",
            llm="gpt-4",
            token_manager=token_manager
        )
        agents.append(openai_agent)
        print("✅ OpenAI agent created")
    except Exception as e:
        print(f"⚠️  OpenAI agent failed: {e}")
    
    # Anthropic agent
    try:
        anthropic_agent = Agent(
            role="Anthropic Analyst",
            goal="Analyze data using Anthropic models",
            backstory="Expert analyst using Claude models",
            llm="claude-3-opus-20240229",
            token_manager=token_manager
        )
        agents.append(anthropic_agent)
        print("✅ Anthropic agent created")
    except Exception as e:
        print(f"⚠️  Anthropic agent failed: {e}")
    
    if agents:
        print(f"\n✅ Successfully created {len(agents)} agents with different providers")
    else:
        print("\n❌ No agents were created successfully")
    
    return len(agents) > 0


async def test_env_var_rejection():
    """Test that environment variables are properly rejected"""
    print("\n🔧 Testing Environment Variable Rejection...")
    
    # Test 1: Try to create agent without token manager (should fail)
    print("\nTest 1: Agent without token_manager...")
    try:
        agent = Agent(
            role="Test Agent",
            goal="Test goal",
            backstory="Test backstory",
            llm="gpt-4"  # String config without token_manager
        )
        print("❌ FAIL: Agent creation should have failed without token_manager")
        return False
    except ValueError as e:
        if "token_manager" in str(e).lower():
            print(f"✅ PASS: Correctly rejected with error: {e}")
        else:
            print(f"❌ FAIL: Wrong error message: {e}")
            return False
    
    # Test 2: Set environment variable and verify it's not used
    print("\nTest 2: Environment variables should be ignored...")
    os.environ["OPENAI_API_KEY"] = "fake-key-should-not-work"
    
    try:
        from crewai.utilities.llm_utils import create_llm
        llm = create_llm(None)  # Should fail even with env var set
        print("❌ FAIL: create_llm should have failed with None")
        return False
    except ValueError as e:
        if "environment variables are not supported" in str(e).lower():
            print(f"✅ PASS: Environment variables correctly rejected: {e}")
        else:
            print(f"❌ FAIL: Wrong error message: {e}")
            return False
    finally:
        # Clean up
        del os.environ["OPENAI_API_KEY"]
    
    # Test 3: Crew without token manager should fail
    print("\nTest 3: Crew without token_manager...")
    try:
        # Create a mock agent with already initialized LLM
        from crewai.llm import LLM
        mock_llm = LLM(model="gpt-4", api_key="test")  # This should work
        
        agent_with_llm = Agent(
            role="Test",
            goal="Test",
            backstory="Test",
            llm=mock_llm  # Already initialized LLM
        )
        
        # But creating agent with string should fail
        agent_with_string = Agent(
            role="Test2",
            goal="Test2",
            backstory="Test2",
            llm="gpt-4"  # String without token_manager
        )
        print("❌ FAIL: Agent with string LLM should have failed")
        return False
    except ValueError as e:
        print(f"✅ PASS: Correctly rejected string LLM without token_manager: {e}")
    
    print("\n✅ All environment variable rejection tests passed!")
    return True


async def main():
    """Run all tests"""
    print("=" * 60)
    print("CrewAI Token Storage Integration Tests")
    print("=" * 60)
    
    # Test basic integration
    basic_test = await test_token_integration()
    
    # Test multiple providers
    multi_test = await test_multiple_providers()
    
    # Test environment variable rejection
    env_test = await test_env_var_rejection()
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary:")
    print(f"  Basic Integration: {'✅ PASS' if basic_test else '❌ FAIL'}")
    print(f"  Multiple Providers: {'✅ PASS' if multi_test else '❌ FAIL'}")
    print(f"  Environment Variable Rejection: {'✅ PASS' if env_test else '❌ FAIL'}")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())