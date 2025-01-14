import json
from openai import OpenAI
from functions import add_numbers, get_current_date, string_length, get_html
from function_specs import fun_specs

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
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
messages = [
    # {
    #     "role": "user",
    #     "content": "What is the sum of 15 and 27?",
    # },
    # {
    #     "role": "user",
    #     "content": "What is todays date?",
    # },
    # {
    #     "role": "user",
    #     "content": "What is the length of string 'hello'?",
    # },
    {
        "role": "user",
        "content": "Get the Text content of https://www.example.com",
    }
]
chat_completion = client.chat.completions.create(
    model="dwightfoster03/functionary-small-v3.1",
    messages=messages,
    tools=tools,
    tool_choice="auto"
)

response = chat_completion.choices[0].message

if hasattr(response, 'tool_calls'):
    tool_calls = response.tool_calls  # Access as an attribute, not a function call
    if tool_calls:
        tool_call = tool_calls[0]
        # Extract function name and arguments
        tool_call_id = tool_calls[0].id
        function_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        print(f"Function name: {function_name}")
        print(f"Arguments: {arguments}")

        # Execute the Function
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

        # --- Feeding back the result to the LLM ---
        # 1. Format the output for the LLM
        # formatted_output = json.dumps({"result": result})  # Assuming 'result' can be serialized to JSON

        # 2. Construct a new prompt
        messages.append({
            "role":"tool", 
            "tool_call_id":tool_call_id, 
            "name": function_name, 
            "content":result
        })

        # messages.append({
        #     "role": "system",  # or "assistant" or a custom role
        #     "content": f"Function call result: `json\n{formatted_output}\n`"
        # })
        # messages.append({
        #     "role": "user",
        #     "content": "Please provide the final answer, taking into account the function call result."
        # })

        # 3. Send the new prompt to the LLM
        chat_completion = client.chat.completions.create(
            model="dwightfoster03/functionary-small-v3.1",
            messages=messages,
            # tools=tools,
        )

        # 4. Extract and process the final response
        final_response = chat_completion.choices[0].message.content
        print(f"Final Response: {final_response}")

    else:
        print("No tool calls found in the response.")
        print(f"Response: {response}")

else:
    print("No function call found in the response.")
    print(f"Response: {response}")