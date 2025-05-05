"""
Central planner agent that coordinates multiple worker agents (crawlers) to extract specified information from a given URL.

Attributes:
    url (str): The URL to be crawled.
    info_to_extract (set): A set of information to extract (e.g., product names, prices, descriptions).

Methods:
    devise_plan(): Devises a plan for extracting the specified information from the URL.
    assign_tasks(): Assigns tasks to the worker agents based on the devised plan.
    monitor_progress(): Monitors the progress of the worker agents.
    log_error(error): Logs an error encountered by a worker agent.

Worker agents (crawlers) are responsible for:
    - Extracting specific information from the URL as assigned by the central planner.
    - Reporting back to the central planner if an error is encountered or if specific information cannot be found.
"""

from openai import OpenAI
import json
from dotenv import load_dotenv  # Add this line to import load_dotenv
import os  # Add this line to import os

load_dotenv()  # Add this line to load environment variables from the root .env file

MODEL = "gemini-2.0-flash-exp"
google_key = os.getenv(
    "GOOGLE_API_KEY"
)  # Replace hardcoded key with environment variable
client = OpenAI(
    api_key=google_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# --- Define functions that the agents can call ---


def log_error(error_message, url, missing_info=None):
    """Logs an error encountered during crawling."""
    log_entry = {
        "error": error_message,
        "url": url,
        "missing_information": missing_info,
    }
    print(f"Error logged: {json.dumps(log_entry, indent=2)}")
    # In a real system, you'd likely save this to a database or log file
    return json.dumps({"status": "error logged"})


def crawl_page(url):
    """Simulates crawling a webpage and extracting information."""
    # In a real crawler, this would involve fetching the HTML, parsing it, etc.
    print(f"Crawling: {url}")

    # Simulate finding some information and missing others
    if "product" in url:
        if "product1" in url:
            return json.dumps({"product_name": "Product 1", "price": "$10"})
        elif "product2" in url:
            return json.dumps(
                {"product_name": "Product 2", "price": "$10"}
            )  # Simulate missing description
        else:
            return {"error": "unknown product"}
    else:
        return json.dumps({"content": f"Content from {url}"})


# --- Define the available tools for the OpenAI API ---
tools = [
    {
        "type": "function",
        "function": {
            "name": "log_error",
            "description": "Log an error encountered during web crawling.",
            "parameters": {
                "type": "object",
                "properties": {
                    "error_message": {
                        "type": "string",
                        "description": "Description of the error.",
                    },
                    "url": {
                        "type": "string",
                        "description": "URL where the error occurred.",
                    },
                    "missing_info": {
                        "type": "string",
                        "description": "Specific information that was not found.",
                    },
                },
                "required": ["error_message", "url"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "crawl_page",
            "description": "Crawl a given URL and extract information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "The URL to crawl."}
                },
                "required": ["url"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
]

# --- Central Planner Logic (using OpenAI Chat Completion) ---


def create_crawling_plan(start_url, information_to_extract):
    """
    Uses the OpenAI API to create a plan for crawling and then executes it.
    """
    messages = [
        {
            "role": "system",
            "content": "You are a central planner for a web crawler. "
            "You are given a start URL and a list of information to extract. "
            "You need to devise a plan to crawl the website and extract the information. "
            "If any information is missing or an error occurs, use the log_error tool."
            f"Use the crawl_page tool to simulate crawling pages.",
        },
        {
            "role": "user",
            "content": f"Crawl {start_url} and extract: {', '.join(information_to_extract)}",
        },
    ]

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools,
        tool_choice="auto",  # Let the model decide whether to call a tool
    )
    response_message = response.choices[0].message  # Correctly access the response
    if hasattr(response_message, "content"):
        print(response_message.content)
    print(response_message)
    # --- Execute the plan suggested by the AI ---

    while True:
        if hasattr(response_message, "tool_calls"):
            for tool_call in response_message.tool_calls:
                # Which tool call was invoked
                tool_name = tool_call.function.name
                # tool args
                arguments = json.loads(tool_call.function.arguments)

                # Handle tool calls
                if tool_name == "crawl_page":
                    tool_response = crawl_page(url=arguments.get("url"))

                    # # send the info on the tool call and tool response to model
                    messages.append(
                        {
                            "role": "assistant",
                            "content": str(response_message),
                        }
                    )  # extend conversation with tool call
                    messages.append(
                        {
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": tool_name,
                            "content": json.dumps(tool_response),
                        }
                    )  # extend conversation with tool response
                    print(messages)
                    # call the model again to see what to do next
                    response = client.chat.completions.create(
                        model=MODEL,
                        messages=messages,
                        tools=tools,
                        # tool_choice="auto",  # Let the model decide whether to call a tool
                    )
                    response_message = response.choices[0].message

                elif tool_name == "log_error":
                    tool_response = log_error(
                        error_message=arguments.get("error_message"),
                        url=arguments.get("url"),
                        missing_info=arguments.get("missing_info"),
                    )
                    # Finish and just log
                    print(tool_response)
                    break
        else:
            print("No tool call invoked.")
            break


# --- Example Usage ---

start_url = "https://www.example.com/products"
info_to_extract = ["product_name", "price", "description"]

create_crawling_plan(start_url, info_to_extract)
