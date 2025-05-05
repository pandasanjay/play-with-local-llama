import requests


class LlamaOllama:
    def __init__(self, base_url="http://localhost:11434", model_name="Llama3.2:1b"):
        self.base_url = base_url
        self.model_name = model_name

    def generate_text(self, prompt, max_tokens=150, temperature=0.7, top_p=0.9):
        url = f"{self.base_url}/api/generate"
        data = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,  # Set to True for streaming responses (more advanced)
            "options": {
                "num_predict": max_tokens,
                "temperature": temperature,
                "top_p": top_p,
            },
        }
        headers = {"Content-Type": "application/json"}

        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()  # Raise an exception for bad status codes

            response_json = response.json()
            return response_json["response"]

        except requests.exceptions.RequestException as e:
            print(f"Error communicating with Ollama API: {e}")
            return ""

    def summarize_text(self, text, max_tokens=100, temperature=0.5, top_p=0.9):
        prompt = f"""
        You are a helpful assistant that provides concise and accurate news summaries.
        Please provide a summary of the following text in less than {max_tokens} words:

        {text}

        Summary:
        """

        summary = self.generate_text(
            prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
        )
        return summary

    def is_article_relevant(self, article_title, article_content, user_preferences):
        """
        Asks Llama whether an article is relevant to a user's preferences.

        Args:
            article_title (str): The title of the article.
            article_content (str): The content of the article.
            user_preferences (dict): The user's preferences (likes and dislikes).

        Returns:
            bool: True if Llama thinks the article is relevant, False otherwise.
        """

        prompt = f"""
        You are an expert news analyst tasked with determining if a news article aligns with a user's interests.

        User Preferences:
        Likes: {", ".join(user_preferences.get("likes", []))}
        Dislikes: {", ".join(user_preferences.get("dislikes", []))}

        Article Title: {article_title}
        Article Content: {article_content}

        Based on the user's preferences, is this article relevant to their interests? Respond with 'yes' or 'no' only.
        """

        url = f"{self.base_url}/api/generate"
        data = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.0,  # Lower temperature for more deterministic output
            },
        }
        headers = {"Content-Type": "application/json"}

        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            response_json = response.json()
            answer = response_json["response"].strip().lower()
            print(f"llm title: {article_title} - answer: {answer}")

            return "yes" in answer  # Check if the answer is affirmative

        except requests.exceptions.RequestException as e:
            print(f"Error communicating with Ollama API: {e}")
            return False


# Example usage (you can test this directly in llama_utils.py):
if __name__ == "__main__":
    llama = LlamaOllama()
    prompt = "What are some tips for summarizing news articles?"
    response = llama.generate_text(prompt)
    print(response)
