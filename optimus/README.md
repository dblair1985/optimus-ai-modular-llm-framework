# Optimus Bot: Clean Modular Rebuild with Local Mistral LLM

A modular, self-healing AI coding agent that uses local Mistral LLM for code analysis, generation, and improvement tasks.

## Features

- 🤖 **Local Mistral LLM Integration**: Uses ctransformers for local inference without cloud dependencies
- 🧩 **Modular Architecture**: Clean, swappable components with hot-loadable skills
- 🧠 **Persistent Memory**: Stores and retrieves context across sessions
- 📋 **Intelligent Planning**: Generates structured step-by-step execution plans
- 🔧 **Extensible Skills**: Easy to add new capabilities and tools
- 📊 **Code Analysis**: Advanced variable flow tracing and code scanning

## Directory Structure

```
optimus/
├── main.py                    # Entry point
├── config/
│   └── settings.py           # Configuration management
├── core/
│   ├── agent_loop.py         # Main agent execution loop
│   ├── planner.py            # Task planning and step generation
│   ├── memory.py             # Persistent memory system
│   └── llm_interface.py      # LLM abstraction layer
├── llms/
│   └── mistral_runner.py     # Local Mistral LLM runner
├── skills/
│   ├── __init__.py           # Skills registry and hot-loading
│   ├── generate_task_code.py # Code generation skill
│   └── trace_variable_flow.py # Variable flow analysis skill
├── utils/
│   ├── code_scanner.py       # Codebase scanning utilities
│   └── file_io.py            # Safe file operations
└── data/
    ├── code_map.json         # Project structure mapping
    └── memory.json           # Persistent memory storage
```

## Installation

1. **Clone or create the project structure**:
   ```bash
   # The directory structure is already created
   cd optimus
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Download a Mistral model** (optional for development):
   ```bash
   # Example: Download a GGUF format Mistral model
   # Place it in a models/ directory and update the MODEL_PATH in settings.py
   ```

## Configuration

Set the model path in `config/settings.py` or via environment variable:

```bash
export MODEL_PATH="/path/to/your/mistral/model.gguf"
```

## Usage

### Basic Usage

```python
from core.agent_loop import run_agent

# Run the agent with a specific goal
success = run_agent("Improve error handling in my Python code")
```

### Command Line

```bash
python main.py
```

### Programmatic Usage

```python
from core.agent_loop import run_agent
from core.memory import Memory
from skills import list_available_skills

# Check available skills
print("Available skills:", list_available_skills())

# Run agent with custom goal
goal = "Analyze variable flow in my codebase"
success = run_agent(goal)

# Check memory
memory = Memory()
context = memory.get_recent_context(goal)
print("Recent context:", context)
```

## Skills System

### Available Skills

- **generate_task_code**: Generate code for specific tasks or improvements
- **trace_variable_flow**: Analyze how variables flow through code

### Adding New Skills

1. Create a new Python file in the `skills/` directory
2. Implement your skill function
3. Register it in `skills/__init__.py`

Example:
```python
# skills/my_new_skill.py
def my_new_skill(param1: str, param2: int = 10) -> str:
    """My custom skill implementation"""
    return f"Processed {param1} with value {param2}"

# skills/__init__.py
from skills.my_new_skill import my_new_skill

# Add to registry
registry.register("my_new_skill", my_new_skill)
```

## Architecture

### Core Components

1. **Agent Loop** (`core/agent_loop.py`): Main execution engine that coordinates planning and skill execution
2. **Planner** (`core/planner.py`): Uses LLM to generate structured execution plans
3. **Memory** (`core/memory.py`): Persistent storage for learning and context
4. **LLM Interface** (`core/llm_interface.py`): Abstraction layer for LLM interactions

### Skills Registry

The skills system supports hot-loading and dynamic registration:
- Skills are automatically discovered and loaded
- New skills can be added without restarting
- Each skill is a simple Python function with clear parameters

### Memory System

- Stores goal-specific execution history
- Provides context for future planning
- Supports retrieval of recent interactions
- JSON-based persistent storage

## Development

### Running Tests

```bash
pytest tests/
```

### Code Formatting

```bash
black optimus/
flake8 optimus/
```

### Adding Logging

```python
import logging
logging.basicConfig(level=logging.INFO)
```

## Configuration Options

Key configuration parameters in `config/settings.py`:

- `MODEL_PATH`: Path to local Mistral model
- `EMBEDDING_MODEL`: Sentence transformer model for embeddings
- `max_tokens`: Maximum tokens for LLM generation
- `temperature`: LLM temperature setting
- `memory_path`: Path to memory storage file

## Troubleshooting

### Model Loading Issues

If the Mistral model fails to load:
1. Check the model path in configuration
2. Ensure ctransformers is properly installed
3. Verify model format compatibility (GGUF recommended)
4. The system will fall back to mock responses for development

### Memory Issues

If memory persistence fails:
1. Check write permissions in the data/ directory
2. Verify JSON format in memory.json
3. Clear memory with `memory.clear_goal(goal_name)`

### Skill Loading Issues

If skills fail to load:
1. Check Python import paths
2. Verify skill function signatures
3. Use `reload_skills()` to refresh the registry

## Examples

### Example 1: Code Generation

```python
from skills.generate_task_code import generate_task_code

code = generate_task_code("Create a function to validate email addresses")
print(code)
```

### Example 2: Variable Flow Analysis

```python
from skills.trace_variable_flow import trace_variable_flow

analysis = trace_variable_flow("my_script.py", "user_data")
print(analysis)
```

### Example 3: Custom Agent Goal

```python
from core.agent_loop import run_agent

# Complex goal with multiple steps
goal = """
Analyze the codebase for potential security vulnerabilities,
generate patches for any issues found, and create documentation
for the improvements made.
"""

success = run_agent(goal)
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure code passes linting
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Roadmap

- [ ] Web interface for agent interaction
- [ ] Integration with more LLM backends
- [ ] Advanced code analysis skills
- [ ] Plugin system for external skills
- [ ] Distributed execution support
- [ ] Integration with popular IDEs
