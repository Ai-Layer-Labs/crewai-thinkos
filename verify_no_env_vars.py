#!/usr/bin/env python3
"""
Verification script to ensure NO environment variables are used for API keys
This script tests various scenarios to confirm env vars are rejected
"""
import os
import sys
import traceback

# Test results
tests_passed = 0
tests_failed = 0

def test_case(name, test_func):
    """Run a test case and track results"""
    global tests_passed, tests_failed
    print(f"\n{'='*60}")
    print(f"TEST: {name}")
    print('='*60)
    try:
        test_func()
        print("❌ FAIL: Expected ValueError but none was raised")
        tests_failed += 1
    except ValueError as e:
        error_msg = str(e).lower()
        if any(phrase in error_msg for phrase in [
            "environment variables are not supported",
            "token manager is required",
            "token_manager"
        ]):
            print(f"✅ PASS: Correctly rejected with: {e}")
            tests_passed += 1
        else:
            print(f"❌ FAIL: Wrong error message: {e}")
            tests_failed += 1
    except Exception as e:
        print(f"❌ FAIL: Unexpected error type {type(e).__name__}: {e}")
        traceback.print_exc()
        tests_failed += 1

def test_agent_without_token_manager():
    """Test that Agent requires token_manager for string LLM"""
    from crewai import Agent
    agent = Agent(
        role="Test",
        goal="Test",
        backstory="Test",
        llm="gpt-4"  # String without token_manager
    )

def test_crew_without_token_manager():
    """Test that Crew requires token_manager for function_calling_llm"""
    from crewai import Crew, Agent
    from crewai.llm import LLM
    
    # Create agent with initialized LLM (this should work)
    agent = Agent(
        role="Test",
        goal="Test",
        backstory="Test",
        llm=LLM(model="gpt-4", api_key="test")
    )
    
    # But Crew with string function_calling_llm should fail
    crew = Crew(
        agents=[agent],
        tasks=[],
        function_calling_llm="gpt-4"  # String without token_manager
    )

def test_create_llm_with_none():
    """Test that create_llm(None) rejects env vars"""
    from crewai.utilities.llm_utils import create_llm
    
    # Set environment variable
    os.environ["OPENAI_API_KEY"] = "sk-fake-key"
    
    try:
        llm = create_llm(None)
    finally:
        # Clean up
        if "OPENAI_API_KEY" in os.environ:
            del os.environ["OPENAI_API_KEY"]

def test_lite_agent_without_token_manager():
    """Test that LiteAgent requires token_manager"""
    from crewai.lite_agent import LiteAgent
    agent = LiteAgent(
        role="Test",
        goal="Test",
        backstory="Test",
        llm="gpt-4"  # String without token_manager
    )

def test_env_var_completely_ignored():
    """Test that env vars are completely ignored even if set"""
    # Set multiple environment variables
    env_vars = {
        "OPENAI_API_KEY": "sk-fake",
        "ANTHROPIC_API_KEY": "sk-ant-fake",
        "GROQ_API_KEY": "gsk-fake",
        "MODEL": "gpt-4",
        "OPENAI_MODEL_NAME": "gpt-4-turbo"
    }
    
    for key, value in env_vars.items():
        os.environ[key] = value
    
    try:
        from crewai import Agent
        # This should fail even with all env vars set
        agent = Agent(
            role="Test",
            goal="Test",
            backstory="Test",
            llm="gpt-4"
        )
    finally:
        # Clean up
        for key in env_vars:
            if key in os.environ:
                del os.environ[key]

def main():
    """Run all verification tests"""
    print("CrewAI Environment Variable Rejection Verification")
    print("="*60)
    print("This script verifies that ALL attempts to use environment")
    print("variables for API keys are properly rejected.")
    
    # Run all tests
    test_case("Agent without token_manager", test_agent_without_token_manager)
    test_case("Crew without token_manager", test_crew_without_token_manager)
    test_case("create_llm(None) with env var", test_create_llm_with_none)
    test_case("LiteAgent without token_manager", test_lite_agent_without_token_manager)
    test_case("Environment variables completely ignored", test_env_var_completely_ignored)
    
    # Summary
    print(f"\n{'='*60}")
    print("VERIFICATION SUMMARY")
    print('='*60)
    print(f"Tests Passed: {tests_passed}")
    print(f"Tests Failed: {tests_failed}")
    
    if tests_failed == 0:
        print("\n✅ SUCCESS: All environment variable usage is properly rejected!")
        print("The system has ZERO tolerance for insecure practices.")
        return 0
    else:
        print("\n❌ FAILURE: Some tests failed. Environment variables might still be used!")
        return 1

if __name__ == "__main__":
    sys.exit(main())