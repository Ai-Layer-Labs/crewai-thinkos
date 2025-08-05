# CrewAI - ThinkOS Fork

This is a customized fork of CrewAI that integrates with ThinkOS's unified token storage system.

## 🔒 Key Security Features

1. **Zero Environment Variables**: All LLM API keys are retrieved from ThinkOS's secure token storage. **NO ENVIRONMENT VARIABLES, NO EXCEPTIONS**.

2. **Secure Token Management**: All tokens are encrypted and stored in a secure database - never in code or environment.

3. **No Fallbacks**: This fork enforces secure token storage with zero tolerance for environment variable usage.

## 🚀 Quick Start

### Installation

```bash
# Build and install from source
cd crewai-thinkos
python -m build
python -m pip install dist/crewai_thinkos-*.whl
```

### Usage with ThinkOSCrew Wrapper (Recommended)

```python
from backend.agents import ThinkOSCrew

# Initialize with automatic token management
crew = ThinkOSCrew()
await crew.initialize()

# Create agents with database-driven configuration
agent = crew.create_agent(
    role="Researcher",
    goal="Research complex topics",
    agent_type="researcher"  # Auto-configures from database!
)

# Or specify model explicitly
agent = crew.create_agent(
    role="Analyst",
    goal="Analyze data",
    llm_provider="openai",
    llm_model="gpt-4"  # No defaults - must be explicit
)
```

### Low-Level Usage (Direct CrewAI)

```python
from crewai import Agent, Task, Crew
from backend.services.llm.token_manager import get_token_manager

# Token manager is required - no exceptions
token_manager = await get_token_manager()

# Create agent with token manager
agent = Agent(
    role="Researcher",
    goal="Research topics",
    token_manager=token_manager,  # Required!
    llm_provider="openai",
    llm_model="gpt-4"
)
```

## 📁 Key Modifications

### Added Files
- `src/crewai/integrations/token_storage.py` - Token storage integration
- `src/crewai/integrations/llm_factory.py` - LLM factory with secure token retrieval
- `backend/agents/thinkos_crew.py` - High-level wrapper with full CrewAI features
- `backend/agents/model_config_manager.py` - Database-driven model configuration

### Modified Core Components
- `src/crewai/agent.py` - Added mandatory `token_manager` parameter
- `src/crewai/crew.py` - Added mandatory `token_manager` parameter
- `src/crewai/utilities/llm_utils.py` - Removed all environment variable support
- Package name changed to `crewai-thinkos`

## 🔧 Database-Driven Configuration

Models can be configured in the application_settings table:

```python
# Import configurations
python scripts/manage_model_configs.py import examples/model_configs.json

# List configurations
python scripts/manage_model_configs.py list

# Use in code
agent = crew.create_agent(
    role="Planner",
    goal="Strategic planning",
    agent_type="planner"  # Uses database configuration
)
```

## 📚 Documentation

- [ThinkOSCrew Guide](../docs/THINKOS_CREW_GUIDE.md) - Complete wrapper documentation
- [Database Configuration](../docs/THINKOS_CREW_DATABASE_CONFIG.md) - Model configuration guide
- [Security Overview](../docs/CREWAI_SECURITY.md) - Security implementation details

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