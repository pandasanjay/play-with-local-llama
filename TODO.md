# Step-by-Step Learning Journey

This document provides a structured learning path to guide you through this repository, from basic LLM interactions to advanced agentic systems.

## Phase 1: Understanding LLM Basics
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Try the basic LLM interaction example: `test_llama.py`
- [ ] Learn about LangChain: `agentic-framworks/langchain/get_started.py`
- [ ] Study basic tokenization: `tokenizers/helloworld_tokenizers.ipynb`

## Phase 2: Function Calling
- [ ] Understand function calling basics: `agents/function_calling/function_calling_with_llm.py`
- [ ] Explore advanced function calling: `agents/function_calling/function_calling_with_llm_v2.py`
- [ ] Examine function specifications: `agents/function_calling/function_specs.py`
- [ ] Try modifying and adding new functions

## Phase 3: Simple Agents
- [ ] Study the movie recommendation agent: `agents/movie-recomandation.py`
- [ ] Explore the reminder agent: `agents/reminder-agent.py`
- [ ] Try adding new features to these simple agents
- [ ] Create your own simple agent with a specific purpose

## Phase 4: Advanced Agents with Components
- [ ] Explore the News Summary Agent: `agents/news-summary-agent/`
- [ ] Understand its component architecture:
  - [ ] Retrieval: `agents/news-summary-agent/retrieval.py`
  - [ ] Memory: `agents/news-summary-agent/memory.py`
  - [ ] LLM Interface: `agents/news-summary-agent/llama_utils.py`
- [ ] Try the Web Crawler Agent: `agents/crawler_agent/`

## Phase 5: Multi-Agent Systems
- [ ] Study the multi-agent architecture: `agents/multi-agent/multi-agent-strctured_out.py`
- [ ] Understand agent communication patterns
- [ ] Examine how tasks are distributed among agents
- [ ] Explore the planning agent: `agents/planning_agent/centralized_planning.py`

## Phase 6: Advanced LLM Topics
- [ ] Learn about self-attention: `tokenizers/self_attention.ipynb`
- [ ] Understand multi-head attention: `tokenizers/multi_head_attention.ipynb`
- [ ] Explore model fine-tuning: `fine-tuning/hf_guide_image_clacification_loRa.ipynb`

## Phase 7: Building Your Own Systems
- [ ] Design a new agent with a unique purpose
- [ ] Implement a multi-agent system for a complex task
- [ ] Experiment with different LLM models (local and API-based)
- [ ] Try implementing a RAG-based system with your own data

## Advanced Challenges
- [ ] Add streaming capabilities to function calling examples
- [ ] Implement agent memory persistence across sessions
- [ ] Create an evaluation framework to measure agent performance
- [ ] Build a user interface for interacting with your agents
- [ ] Explore fine-tuning for improving agent performance