from llama_utils import LlamaOllama
from memory import UserPreferences
from retrieval import NewsRetriever

class NewsSummarizerAgent:
    def __init__(self):
        self.llama = LlamaOllama()  # Use LlamaOllama instead of LlamaModel
        self.memory = UserPreferences()
        self.retriever = NewsRetriever()

    def get_news_summary(self, user_id, query):
        user_preferences = self.memory.get_user_preferences(user_id)
        articles = self.retriever.search_articles(query, user_preferences)

        if not articles:
            return "I couldn't find any relevant news articles matching your preferences."

        summaries = []
        for article in articles:
            summary = self.llama.summarize_text(article["content"])
            summaries.append(f"{article['title']}:\n{summary}\n")

        return "\n".join(summaries)

    def update_user_preferences(self, user_id, likes=None, dislikes=None):
        self.memory.update_user_preferences(user_id, likes, dislikes)

# Example usage:
if __name__ == "__main__":
    agent = NewsSummarizerAgent()

    # # Initial user preferences
    # agent.update_user_preferences("user1", likes=["technology", "space"], dislikes=["gossip", "politics"])

    # # Get news summary
    query = "latest discoveries in space and AI"
    # summary = agent.get_news_summary("user1", query)
    # print(summary)

    # # Update preferences based on feedback (you can add more interactive feedback mechanisms later)
    # agent.update_user_preferences("user1", likes=["quantum computing"], dislikes=["international news"])

    # Get another summary
    summary = agent.get_news_summary("user1", query)
    print(summary)