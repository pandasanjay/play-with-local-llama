import json
import os
from llama_utils import LlamaOllama

class NewsRetriever:
    def __init__(self, filepath="articles.json"):
        self.filepath = filepath
        self.load_articles()
        self.llama = LlamaOllama() # Initialize Ollama in retriever

    def load_articles(self):
        try:
            with open(self.filepath, "r") as f:
                self.articles = json.load(f)
        except FileNotFoundError as e:
            print("No articles found.", e)
            self.articles = []

    def search_articles(self, query, user_preferences):
        # Basic keyword matching with deduplication
        relevant_articles = []
        seen_titles = set()  # Keep track of article titles we've already added

        for article in self.articles:
            if any(keyword.lower() in article["title"].lower() or keyword.lower() in tag.lower() for keyword in query.split() for tag in article['tags']):
                # Add article only if its title hasn't been seen before
                if article["title"] not in seen_titles:
                    relevant_articles.append(article)
                    seen_titles.add(article["title"])

        # Filter based on user preferences using LLM
        filtered_articles = []
        for article in relevant_articles:
            if self.llama.is_article_relevant(article["title"], article["content"], user_preferences):
                filtered_articles.append(article)

        return filtered_articles

# Example usage:
if __name__ == "__main__":
    retriever = NewsRetriever()
    user_preferences = {"likes": ["technology", "space"], "dislikes": ["gossip"]}
    query = "new discoveries in science and technology"  # Query with multiple keywords
    results = retriever.search_articles(query, user_preferences)
    for article in results:
        print(article["title"])