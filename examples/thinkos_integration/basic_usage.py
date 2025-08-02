"""Example: Using CrewAI with ThinkOS Token Storage - REAL INTEGRATION"""
import asyncio
import sys
import os

# Add ThinkOS backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../backend'))

from crewai import Agent, Task, Crew
from crewai.llm.factory import LLMFactory
from services.llm.token_manager import get_token_manager

async def create_crew_with_tokens():
    # Get the REAL token manager - no mocks!
    token_manager = await get_token_manager()
    
    # Create LLM factory with token manager
    llm_factory = LLMFactory(token_manager)
    
    # IMPORTANT: Before running this example, you must:
    # 1. Have the ThinkOS LLM service running
    # 2. Store your API keys via the token management API:
    #    curl -X POST http://localhost:8000/api/v1/tokens/store \
    #      -H "Content-Type: application/json" \
    #      -d '{"service": "llm_provider_openai_api_key", "token": "sk-...", "token_type": "api-key"}'
    
    try:
        # Create agents with custom LLMs - will fail if tokens not stored!
        researcher = Agent(
            role="Senior Research Analyst",
            goal="Uncover cutting-edge developments in AI",
            backstory="You're a seasoned researcher with a knack for uncovering the latest developments in AI.",
            llm=llm_factory.create_llm(provider="openai", model="gpt-4"),
            verbose=True
        )
        
        writer = Agent(
            role="Tech Content Strategist",
            goal="Craft compelling content about AI developments",
            backstory="You're a renowned content strategist known for creating engaging narratives around tech topics.",
            llm=llm_factory.create_llm(provider="anthropic", model="claude-3-opus-20240229"),
            verbose=True
        )
    except ValueError as e:
        print(f"\n❌ ERROR: {e}")
        print("\n💡 Make sure you've stored your API keys using the token management API!")
        print("   See the comments above for the exact curl command.")
        return None
    
    # Create tasks
    research_task = Task(
        description="Research the latest breakthroughs in AI for 2024",
        expected_output="A comprehensive report with at least 5 key developments",
        agent=researcher
    )
    
    write_task = Task(
        description="Create an engaging blog post about the AI breakthroughs",
        expected_output="A 1000-word blog post that's both informative and entertaining",
        agent=writer
    )
    
    # Create and run crew
    crew = Crew(
        agents=[researcher, writer],
        tasks=[research_task, write_task],
        verbose=True
    )
    
    result = crew.kickoff()
    return result

if __name__ == "__main__":
    # Run the example
    result = asyncio.run(create_crew_with_tokens())
    if result:
        print("\n" + "="*50)
        print("FINAL RESULT:")
        print("="*50)
        print(result)
    else:
        print("\n⚠️  Example failed. Please check the prerequisites above.")