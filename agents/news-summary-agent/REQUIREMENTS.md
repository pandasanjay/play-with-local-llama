The "Personalized News Summarizer"

 Retrieval, long-term memory (basic).
**Goal:** Create an agent that remembers user preferences and uses them to find and summarize relevant news articles.
Retrieval: Similar to Project 2, but you might need to expand your knowledge base or implement a more realistic web search simulation.
**Long-term Memory:**
Store user preferences in a simple data structure (e.g., a dictionary or a JSON file). For example: {"user1": {"likes": ["technology", "space"], "dislikes": ["politics"]}}.
Use these preferences to filter search results or to weight the relevance of retrieved information.
You could also start experimenting with updating user preferences based on feedback (e.g., if the user says "I don't like this article," you might add the article's topic to their "dislikes").
Summarization: Use Llama to generate short summaries of the selected news articles. You can guide Llama with specific instructions in the prompt (e.g., "Summarize this article in two sentences, focusing on the key takeaways").

Gemini Link: https://gemini.google.com/app/99b9018389426810