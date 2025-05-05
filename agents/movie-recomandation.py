import requests

from utils import handle_stream_data

def user_input_callback():
    """
    Callback function to get user input.
    """
    return input()

def recommend_movies_with_llm():
    """
    Recommends movies using the LLM.
    """
    preferences = input("Tell me about your movie preferences: ")

    # Prepare the API request to Ollama
    url = "http://localhost:11434/api/generate"
    data = {
        "model": "Llama3.2:1b",
        "prompt": f"Suggest a movie night for a group of people. Ask me for their preferences and then recommend a movie.",
    }

    # Send the request to Ollama
    response = requests.post(url, json=data, stream=True)

    # Process the LLM's response
    recommendations = handle_stream_data.extract_reminder_info(response, callback=user_input_callback)
    print(recommendations)  # Print the LLM's recommendations


recommend_movies_with_llm()
