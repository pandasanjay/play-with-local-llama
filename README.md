# LLM and Agentic AI Systems: A Beginner's Guide

This repository provides a structured approach to learning about Large Language Models (LLMs) and Agentic AI systems through practical examples.

## Prerequisites

- Python 3.10+
- A Google API key (for Gemini models) or access to local LLM via Ollama
- Basic understanding of Python programming

## Installation

### Using uv (Recommended)

This project uses [uv](https://astral.sh/uv), an extremely fast Python package manager and project tool written in Rust.

1. Install uv:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Create a virtual environment and install dependencies:
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip sync
```

3. Install optional dependencies:
```bash
# For development tools
uv pip install -e ".[dev]"

# For notebook support
uv pip install -e ".[notebook]"

# For GPU acceleration
uv pip install -e ".[gpu]"

# For web-related examples
uv pip install -e ".[web]"
```

### Using pip (Alternative)

If you prefer traditional pip:
```bash
pip install -r requirements.txt
```

## Ollama Setup

For examples using local LLMs, you'll need to install [Ollama](https://ollama.ai/) separately on your system:

1. Install Ollama:
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

2. Start the Ollama service:
```bash
ollama serve
```

3. Pull the models required for the examples:
```bash
ollama pull llama2
ollama pull mistral
ollama pull dwightfoster03/functionary-small-v3.1
```

## Using the Development Container

This repository includes a devcontainer configuration for VS Code with CUDA support:

1. Install [Docker](https://www.docker.com/products/docker-desktop/) and [VS Code](https://code.visualstudio.com/)
2. Install the [Remote Development extension pack](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack)
3. Install [Ollama](https://ollama.ai/) on your host system (not in the container)
4. Open this repository in VS Code and click "Reopen in Container" when prompted
5. The container will set up everything automatically, including:
   - Python 3.10 with uv package manager
   - CUDA support for GPU acceleration
   - All required dependencies

Note: Ollama needs to be running on your host system and accessible to the container. The default connection URL is http://localhost:11434.

## Learning Path

### 1. Basic LLM Interactions
Start with the simplest examples to understand how to interact with language models:

- **Simple Text Generation**: [test_llama.py](./test_llama.py)
- **Getting Started with LangChain**: [agentic-framworks/langchain/get_started.py](./agentic-framworks/langchain/get_started.py)

To run using uv:
```bash
uv run test_llama.py
# or using the defined script shortcut
uv run --script tutorial
```

### 2. Function Calling
Learn how to make LLMs call specific functions:

- **Basic Function Calling**: [agents/function_calling/function_calling_with_llm.py](./agents/function_calling/function_calling_with_llm.py)
- **Advanced Function Calling**: [agents/function_calling/function_calling_with_llm_v2.py](./agents/function_calling/function_calling_with_llm_v2.py)

To run using uv:
```bash
uv run --script function-call
```

### 3. Simple Agents
Explore single-purpose agents:

- **Movie Recommendation Agent**: [agents/movie-recommendation.py](./agents/movie-recomandation.py)
- **Reminder Agent**: [agents/reminder-agent.py](./agents/reminder-agent.py)

### 4. Advanced Agents
Dive into more complex agent systems:

- **News Summary Agent**: [agents/news-summary-agent/news-summary-agent.py](./agents/news-summary-agent/news-summary-agent.py)
- **Web Crawler Agent**: [agents/crawler_agent/](./agents/crawler_agent/)

### 5. Multi-Agent Systems
Learn how multiple agents can work together:

- **Multi-Agent System**: [agents/multi-agent/multi-agent-strctured_out.py](./agents/multi-agent/multi-agent-strctured_out.py)
- **Planning Agent**: [agents/planning_agent/centralized_planning.py](./agents/planning_agent/centralized_planning.py)

### 6. Advanced Topics
Explore more advanced concepts:

- **Model Internals**: Check the [tokenizers/](./tokenizers/) and [transformers/](./transformers/) directories
- **Fine-tuning**: See examples in [fine-tuning/](./fine-tuning/)

## Quick Start Guide

If you're completely new to LLMs and AI agents, follow these steps:

1. Start with [agentic-framworks/langchain/get_started.py](./agentic-framworks/langchain/get_started.py) to understand basic LLM interactions
2. Move to [agents/function_calling/function_calling_with_llm.py](./agents/function_calling/function_calling_with_llm.py) to learn about function calling
3. Try out the simple agents in the [agents/](./agents/) directory
4. Progress to more complex multi-agent systems

## Resources

- [LangChain Documentation](https://python.langchain.com/docs/)
- [Ollama GitHub Repository](https://github.com/ollama/ollama)
- [Google AI Studio](https://ai.google.dev/)
- [uv Documentation](https://docs.astral.sh/uv/)
