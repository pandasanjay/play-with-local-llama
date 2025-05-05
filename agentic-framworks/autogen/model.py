from autogen_core.models import UserMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import os
from dotenv import load_dotenv  # Add this line to import load_dotenv

load_dotenv()  # Load environment variables from .env file
MODEL = 'gemini-1.5-flash-8b' #"gemini-2.0-flash-exp"
google_key = os.getenv("GOOGLE_API_KEY")


async def main():
    model_client = OpenAIChatCompletionClient(
        model=MODEL,
        api_key=google_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )
    response = await model_client.create(
        [UserMessage(content="What is the capital of France?", source="user")]
    )
    print(response)


import asyncio

asyncio.run(main())
