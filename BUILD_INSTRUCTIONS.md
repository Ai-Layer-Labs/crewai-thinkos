# Building CrewAI-ThinkOS

## Prerequisites

- Python 3.10+
- pip
- build tools: `pip install build`

## Build Steps

1. Install dependencies:
   ```bash
   pip install -e .
   ```

2. Build the package:
   ```bash
   python -m build
   ```

3. The built packages will be in `dist/`:
   - `crewai_thinkos-*.whl` (wheel)
   - `crewai_thinkos-*.tar.gz` (source)

## Installation in ThinkOS

```bash
cd /path/to/thinkos
pip install /path/to/crewai-thinkos/dist/crewai_thinkos-*.whl
```

## Testing

```bash
# Run tests
pytest tests/

# Run integration example
python examples/thinkos_integration/basic_usage.py
```