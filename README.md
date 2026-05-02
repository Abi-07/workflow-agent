# Workflow Agent

A full-fledged AI agent capable of orchestrating and executing complex workflows with integrated voice capabilities. This agent uses natural language processing, intent recognition, and dynamic task planning to execute multi-step operations autonomously.

## Features

- **Workflow Orchestration**: Plan and execute complex, multi-step workflows autonomously
- **Voice Interface**: Natural voice input and output capabilities
- **Intent Recognition**: Intelligent parsing of user intent using advanced NLP
- **Dynamic Planning**: Automatic task planning and replanning based on execution feedback
- **Tool Integration**: Extensible tool registry for integrating external services (calendar, etc.)
- **Memory Management**: Long-term and short-term memory for context awareness
- **State Management**: Robust state tracking throughout agent execution
- **LLM Integration**: Powered by large language models for natural interactions

## Project Structure

```
agent/          - Core agent logic (executor, planner, intent parser, etc.)
app/            - Application setup and configuration
memory/         - Long-term and short-term memory systems
prompts/        - LLM prompt templates for various agent functions
schemas/        - Data models for execution, intents, plans, and tools
tools/          - Tool registry and integrations (e.g., calendar)
utils/          - Utilities (LLM, logging, parsing, prompt loading)
tests/          - Test suite for agent components
```

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd voice-agent
```

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up credentials:

- Place your API credentials in `credentials.json`
- Generate and store authentication tokens in `token.json`
- Configure environment variables in `.env` (see `.env.example` if available)

## Usage

Start the workflow agent:

```bash
python -m app.main
```

## Architecture

The agent operates through several core components:

- **Intent Parser**: Analyzes user input to extract intent and parameters
- **Planner**: Generates execution plans based on recognized intents
- **Replanner**: Adjusts plans based on execution feedback
- **Executor**: Carries out planned tasks using available tools
- **Memory Systems**: Maintains context across conversations and sessions
- **Tool Registry**: Manages available tools and their integrations

## Configuration

Edit `app/config.py` to customize:

- Agent behavior and parameters
- LLM model selection and settings
- Tool availability and settings
- Memory constraints and parameters

## Testing

Run tests with:

```bash
pytest tests/
```

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

This project is licensed under the MIT License.

See the [LICENSE](LICENSE) file for details.
