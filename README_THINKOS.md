# CrewAI - ThinkOS Fork

This is a customized fork of CrewAI that integrates with ThinkOS's unified token storage system.

## Key Modifications

1. **Token Storage Integration**: All LLM API keys are retrieved from ThinkOS's secure token storage. **NO ENVIRONMENT VARIABLES**.

2. **LLM Factory**: A new factory pattern for creating LLM instances with automatic token retrieval from secure storage only.

3. **No Fallbacks**: This fork enforces secure token storage - environment variables are NOT supported.

## Installation

```bash
# Build from source
pip install -e .

# Or install built package
pip install dist/crewai_thinkos-*.whl
```

## Usage

```python
from crewai import Agent, Task, Crew
from crewai.llm.factory import LLMFactory
from your_app.token_manager import get_token_manager

# Get your token manager
token_manager = await get_token_manager()

# Create LLM factory
llm_factory = LLMFactory(token_manager)

# Create agents with token-managed LLMs
agent = Agent(
    role="Researcher",
    goal="Research topics",
    llm=llm_factory.create_llm(provider="openai", model="gpt-4")
)
```

## Differences from Upstream

- Added `src/crewai/integrations/token_storage.py`
- Added `src/crewai/llm/factory.py`
- Modified package name to `crewai-thinkos`
- Added ThinkOS integration examples

## Syncing with Upstream

```bash
git fetch upstream
git checkout main
git merge upstream/main
git checkout unified-storage-integration
git merge main
```

## Contributing

Please submit issues and PRs to the ThinkOS fork repository.