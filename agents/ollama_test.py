import requests
import json

OLLAMA_API_URL = "http://localhost:11434/api/generate"  # Default Ollama API URL
OLLAMA_MODEL = "Llama3.2:1b"  # Replace with the actual model name you have running in Ollama

def call_ollama(prompt, model=OLLAMA_MODEL):
    """Calls the Ollama API for text generation."""
    try:
        response = requests.post(
            OLLAMA_API_URL,
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,  # Get the full response at once
                "raw": True
            },
            # timeout=10  # Set a timeout (in seconds)
        )
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        return response.json()["response"]
    except requests.exceptions.RequestException as e:
        print(f"Error calling Ollama API: {e}")
        return None
    except (KeyError, json.JSONDecodeError) as e:
        print(f"Error parsing Ollama response: {e}. Raw response: {response.text if 'response' in locals() else 'No response received'}")
        return None

# Sample usage with context
context = """
You are a helpful assistant that provides concise answers.
"""

questions = [
    "What is the capital of France?",
    "What is the largest planet in our solar system?",
    "What is the chemical symbol for water?",
]

for question in questions:
    prompt = f"{context}\n{question}"
    print(f"Prompt: {prompt}")
    ollama_response = call_ollama(prompt)
    if ollama_response:
        print(f"Ollama Response: {ollama_response}\n")
    else:
        print("Failed to get a response from Ollama.\n")

# Example without context
print("Example without context:")
prompt_no_context = "Write a short poem about nature."
ollama_response_no_context = call_ollama(prompt_no_context)
if ollama_response_no_context:
    print(f"Ollama Response: {ollama_response_no_context}\n")
else:
    print("Failed to get a response from Ollama.\n")


# Example with different model (if you have multiple models running)
print("Example with different model (if available):")
prompt_diff_model = "Tell me a joke."
ollama_response_diff_model = call_ollama(prompt_diff_model, model="llama2:13b") # Replace with your model name
if ollama_response_diff_model:
    print(f"Ollama Response: {ollama_response_diff_model}\n")
else:
    print("Failed to get a response from Ollama or model not found.\n")