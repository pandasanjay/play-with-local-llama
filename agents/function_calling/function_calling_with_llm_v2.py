# Function Calling with LLMs - Advanced Example
# ===============================================
# This tutorial demonstrates how to use function calling capabilities with LLMs
# Function calling allows LLMs to request the execution of specific functions based on user input

import json
from openai import OpenAI
from functions import add_numbers, get_current_date, string_length, get_html
from function_specs import fun_specs

# ============== PART 1: Setup Client and Tools ==============
# Initialize the OpenAI client with Ollama as the backend
# This setup allows you to use local LLMs with OpenAI-compatible APIs
client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

# Define the tools (functions) that the model can call
# Each tool has a name, description, and parameters
tools = [
    {
        "type": "function",
        "function": {
            "name": spec["name"],
            "description": spec["description"],
            "parameters": spec["parameters"],
        }
    }
    for spec in fun_specs
]

# ============== PART 2: Create Messages Array ==============
# The messages array contains the conversation history
# Uncomment different examples to try different function calls
messages = [
    # Example 1: Add numbers
    # {
    #     "role": "user",
    #     "content": "What is the sum of 15 and 27?",
    # },
    
    # Example 2: Get current date
    # {
    #     "role": "user",
    #     "content": "What is today's date?",
    # },
    
    # Example 3: String length
    # {
    #     "role": "user",
    #     "content": "What is the length of string 'hello'?",
    # },
    
    # Example 4: Get HTML content from a URL
    {
        "role": "user",
        "content": "Get the Text content of https://www.example.com",
    }
]

# ============== PART 3: Get Completion from LLM ==============
# Send the messages to the model and get a response
chat_completion = client.chat.completions.create(
    model="dwightfoster03/functionary-small-v3.1",  # Using a model with function calling ability
    messages=messages,
    tools=tools,                                    # Provide available tools to the model
    tool_choice="auto"                              # Let the model decide which tool to use
)

# Get the response from the model
response = chat_completion.choices[0].message

# ============== PART 4: Handle Tool Calls ==============
# Check if the model requested a tool call
if hasattr(response, 'tool_calls'):
    tool_calls = response.tool_calls
    if tool_calls:
        print("=== Function Call Detected ===")
        tool_call = tool_calls[0]
        
        # Extract tool details
        tool_call_id = tool_calls[0].id
        function_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        
        print(f"Function name: {function_name}")
        print(f"Arguments: {arguments}")

        # Execute the requested function
        result = None
        if function_name == "add_numbers":
            result = add_numbers(arguments["a"], arguments["b"])
        elif function_name == "get_current_date":
            result = get_current_date()
        elif function_name == "string_length":
            result = string_length(arguments["text"])
        elif function_name == "get_html":
            result = get_html(arguments["url"])
        else:
            result = "Error: Unknown function."

        # Print the result
        print(f"Result of function call: {result}")

        # ============== PART 5: Feed Result Back to the LLM ==============
        # Update the messages array with the function result
        messages.append({
            "role": "tool", 
            "tool_call_id": tool_call_id, 
            "name": function_name, 
            "content": result
        })

        # Get the final response from the model
        print("\n=== Getting Final Response ===")
        final_completion = client.chat.completions.create(
            model="dwightfoster03/functionary-small-v3.1",
            messages=messages
        )
        
        print("Final Answer:")
        print(final_completion.choices[0].message.content)
else:
    # The model didn't request a function call
    print("=== Direct Answer ===")
    print(response.content)

# ============== NEXT STEPS ==============
# 1. Try uncommenting different message examples
# 2. Add your own custom functions in functions.py
# 3. Update function_specs.py with new function definitions
# 4. Explore more complex function calling patterns with multiple functions