# Getting Started with LangChain and Google AI
# ============================================
# This tutorial demonstrates the basics of using LangChain with Google's Gemini models
# LangChain is a framework for developing applications powered by language models

import getpass
import os

# Setup: Get API key if not already in environment
if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google AI API key: ")
    
from langchain_google_genai import ChatGoogleGenerativeAI

# ============== PART 1: Basic LLM Interaction ==============
# Initialize the LLM with specific parameters
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-001",  # Model name
    temperature=0,                  # Lower values = more deterministic responses
    max_tokens=None,                # Maximum length of response
    timeout=None,                   # Request timeout
    max_retries=2,                  # Number of retries if request fails
)

# Create a simple conversation with system and user messages
messages = [
    # System message sets the behavior of the assistant
    (
        "system",
        "You are a helpful assistant that translates English to French. Translate the user sentence.",
    ),
    # User message provides the input to translate
    ("human", "I love programming."),
]

# Send the messages to the model and get a response
ai_msg = llm.invoke(messages)

# Display the response
print("=== Basic LLM Response ===")
print(ai_msg.content)
print()

# ============== PART 2: Using Prompt Templates and Chains ==============
# LangChain's power comes from creating reusable components and chains
from langchain_core.prompts import ChatPromptTemplate

# Create a reusable prompt template with placeholders
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant that translates {input_language} to {output_language}.",
        ),
        ("human", "{input}"),
    ]
)

# Create a simple chain: Prompt Template -> LLM
chain = prompt | llm

# Execute the chain with specific parameters
out_mes = chain.invoke(
    {
        "input_language": "English",
        "output_language": "German",
        "input": "I love programming.",
    }
)

print("=== Chain Output ===")
print(out_mes.content)
print()

# ============== PART 3: Image Generation with Gemini ==============
# Gemini models can also generate images
import base64
from io import BytesIO

from IPython.display import Image, display

# Initialize a model specifically for image generation
image_llm = ChatGoogleGenerativeAI(model="models/gemini-2.0-flash-exp-image-generation")

# Create a message requesting an image
message = {
    "role": "user",
    "content": "Generate an image of a cuddly cat wearing a hat.",
}

# Generate the image
response = image_llm.invoke(
    [message],
    generation_config=dict(response_modalities=["TEXT", "IMAGE"]),
)

# Process and display the image
print("=== Image Generation ===")
print("Image has been generated. In a notebook environment, you would see the image displayed.")
print("To view the image, you need to run this in a Jupyter notebook or save it to a file.")

# The code below works in a notebook environment:
# image_base64 = response.content[0].get("image_url").get("url").split(",")[-1]
# image_data = base64.b64decode(image_base64)
# display(Image(data=image_data, width=300))

# ============== NEXT STEPS ==============
# Try changing the prompts, models, or parameters
# Experiment with different input languages and sentences
# Check out the function calling examples in the agents/function_calling directory