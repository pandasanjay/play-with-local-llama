# News Summary Agent: A Practical Example

This directory contains a complete implementation of a news summarization agent that retrieves, processes, and summarizes news articles based on user preferences.

## Overview

The News Summary Agent demonstrates several key AI agent capabilities:
- Retrieving information from external sources (news articles)
- Understanding user preferences
- Generating personalized summaries
- Maintaining memory of past interactions

## Components

### 1. News Retriever (`retrieval.py`)
Responsible for fetching relevant news articles based on user queries.

### 2. User Preferences (`memory.py`) 
Stores and manages user preferences to personalize news summaries.

### 3. LLM Interface (`llama_utils.py`)
Handles communication with the language model for generating summaries.

### 4. Main Agent Logic (`news-summary-agent.py`)
Orchestrates the entire process from query to personalized summary.

## How It Works

1. User submits a query for news (e.g., "latest discoveries in space and AI")
2. Agent retrieves relevant news articles using the NewsRetriever
3. Agent filters and ranks articles based on user preferences
4. Agent generates a personalized summary highlighting the most relevant information
5. Agent can update user preferences based on feedback

## Usage Example

```python
from news-summary-agent import NewsSummarizerAgent

# Create the agent
agent = NewsSummarizerAgent()

# Initialize user preferences
agent.update_user_preferences("user1", 
                              likes=["technology", "space"], 
                              dislikes=["gossip", "politics"])

# Get a personalized news summary
query = "latest discoveries in space and AI"
summary = agent.get_news_summary("user1", query)
print(summary)

# Update preferences based on feedback
agent.update_user_preferences("user1", 
                              likes=["quantum computing"], 
                              dislikes=["international news"])
```

## Key Technical Concepts

### RAG (Retrieval-Augmented Generation)
This agent implements RAG by:
1. Retrieving external information (news articles)
2. Processing and filtering that information
3. Using it to augment the LLM's knowledge
4. Generating a personalized output

### Personalization
The agent personalizes its output by:
1. Maintaining user preference profiles
2. Filtering and ranking content based on those preferences
3. Emphasizing topics the user likes
4. De-emphasizing topics the user dislikes

### Memory
The agent maintains memory through:
1. Storing user preferences persistently
2. Updating preferences based on feedback
3. Using past preferences to inform future summaries

## Extending the Agent

You can extend this agent in several ways:
1. Add more sophisticated article retrieval (e.g., semantic search)
2. Implement more complex user preference modeling
3. Add multi-user support with separate preference profiles
4. Incorporate feedback mechanisms to improve summaries over time