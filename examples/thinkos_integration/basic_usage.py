"""Example: Using CrewAI with ThinkOS Token Storage"""
import asyncio
from crewai import Agent, Task, Crew
from crewai.llm.factory import LLMFactory

# This would come from your ThinkOS backend
class MockTokenManager:
    """Mock token manager for example"""
    async def get_token(self, key: str):
        # In real usage, this connects to your token storage
        tokens = {
            "llm_provider_openai_api_key": "sk-mock-key",
            "llm_provider_anthropic_api_key": "sk-ant-mock-key"
        }
        if key in tokens:
            return type('TokenInfo', (), {'token': tokens[key]})()
        return None

async def create_crew_with_tokens():
    # Initialize your token manager
    token_manager = MockTokenManager()
    
    # Create LLM factory with token manager
    llm_factory = LLMFactory(token_manager)
    
    # Create agents with custom LLMs
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
    print("\n" + "="*50)
    print("FINAL RESULT:")
    print("="*50)
    print(result)