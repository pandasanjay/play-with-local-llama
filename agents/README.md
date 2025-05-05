# AI Agents: From Basic to Advanced

This directory contains a collection of increasingly complex AI agent implementations, from simple single-function agents to sophisticated multi-agent systems.

## Learning Path

### 1. Basic Agents
These agents perform specific, well-defined tasks:

- [reminder-agent.py](./reminder-agent.py): A simple agent that helps set and manage reminders
- [movie-recomandation.py](./movie-recomandation.py): An agent that recommends movies based on user preferences

### 2. Function Calling Agents
These examples demonstrate how to make LLMs invoke specific functions:

- [function_calling/function_calling_with_llm.py](./function_calling/function_calling_with_llm.py): Basic function calling 
- [function_calling/function_calling_with_llm_v2.py](./function_calling/function_calling_with_llm_v2.py): Advanced function calling with feedback loops

### 3. Specialized Agents
These agents have more complex capabilities:

- [news-summary-agent/](./news-summary-agent/): Retrieves and summarizes news articles
- [crawler_agent/](./crawler_agent/): Web crawling and information extraction

### 4. Advanced Agent Architectures
These examples show how to build more sophisticated agent systems:

- [multi-agent/](./multi-agent/): Multiple specialized agents working together
- [planning_agent/](./planning_agent/): Agents that can make and execute plans

## Key Concepts

### Agent Components
Most agents in this collection include the following components:

1. **Memory**: How agents store and retrieve information
2. **Tools**: Functions that agents can call to interact with the world
3. **Planning**: How agents decide what actions to take
4. **Execution**: How agents carry out their plans
5. **Feedback**: How agents learn from the results of their actions

### Design Patterns

As you explore these examples, look for these common design patterns:

1. **Function Calling**: Allowing LLMs to invoke external functions
2. **RAG (Retrieval-Augmented Generation)**: Using external data to enhance LLM outputs
3. **Chain of Thought**: Breaking complex reasoning into steps
4. **Tool Use**: Providing agents with capabilities through defined tools
5. **Multi-agent Collaboration**: Having specialized agents work together

## Getting Started

Start with the simplest examples and work your way up to the more complex ones. For each example:

1. Read the code and comments to understand the architecture
2. Run the example to see it in action
3. Modify the code to experiment with different behaviors
4. Try to combine ideas from multiple examples

## Advanced Customization

Once you're comfortable with the basic examples, you can:

1. Create new functions for agents to call
2. Design new agent architectures for specific tasks
3. Implement more sophisticated memory systems
4. Build custom agent evaluation frameworks