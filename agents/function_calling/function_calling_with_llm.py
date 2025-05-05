import json
from llama_cpp import Llama
from functions import add_numbers, get_current_date, string_length, get_html
from agents.function_calling.function_specs import fun_specs
from llama_cpp.llama_tokenizer import LlamaHFTokenizer
# Initialize the LLM
llm = Llama.from_pretrained(
    repo_id="meetkai/functionary-small-v3.1-GGUF",
    filename="functionary-small-llama-3.1.Q4_0.gguf",
    chat_format="functionary",
    n_ctx=8192, 
    verbose=True,
    # n_gpu_layers=-1,
    # chat_format="chatml-function-calling",
    tokenizer=LlamaHFTokenizer.from_pretrained("meetkai/functionary-small-v3.1-GGUF")
)
# --- Define the Tools (Function Specifications) ---
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

#print(tools)
# --- Construct the Chat Messages ---
messages = [
    {
        "role": "user",
        "content": "What is the sum of 15 and 27?",
    },
]

# # --- Construct the Prompt ---
# prompt = """
# You are a helpful assistant with access to the following functions:

# {function_specs}

# Use these functions to assist the user when appropriate. 
# If the user asks a question that can be answered by one of the available functions, generate a JSON object with the function name and arguments.
# Only use the provided functions. Do not attempt to answer questions directly if a function can be used.

# Here are some examples:

# User: What is the sum of 10 and 20?
# Assistant: ```json
# {{
#   "name": "add_numbers",
#   "arguments": {{
#     "a": 10,
#     "b": 20
#   }}
# }}
# ```
# User: What is the current date?
# Assistant: ```json
# {{
# "name": "get_current_date",
# "arguments": {{}}
# }}
# ```
# User: What is the length of string "hello"?
# Assistant: ```json
# {{
#   "name": "string_length",
#   "arguments": {{
#     "text": "hello"
#   }}
# }}
# ```
# """.format(function_specs=json.dumps(fun_specs, indent=2))

# # --- Example User Input ---
# user_input = "What is the sum of 15 and 27?"

# # --- Add User Input to Prompt ---
# prompt += f"\nUser: {user_input}\nAssistant:"

# # Generate text
# output = llm(
#     prompt,
#     max_tokens=64,  # Limit the response length
#     stop=["Question:", "\n"],
#     echo=True,
# )
# # --- Print the Output ---
# print(output)
# --- Call the LLM ---
# --- Force the Use of the add_numbers Function ---
tool_choice = {
    "type": "function",
    "function": {"name": "add_numbers"}
}
response = llm.create_chat_completion(
    messages=messages,
    tools=tools,
    tool_choice="auto",
    # tool_choice=tool_choice,
    #max_tokens=512, # Increased to generate proper response
    # stop=["<|im_end|>"],  # Stop at the end of the assistant's response
)

# --- Print the Output ---


# # --- Basic Function Call Handling (Incomplete) ---
# response_text = output["choices"][0]["text"]
# if "function_call" in response_text:  # Basic check for function call
#     print("Function call detected!")
#     # (In the next step, we'll parse the JSON and execute the function)
# else:
#     print("No function call detected.")
#     print(response_text)

# --- Enhanced Function Call Handling ---
response = response["choices"][0]
print(response)
# Check if "function_call" exists in the response
if "function_call" in response["message"].keys():
    function_call = json.loads(response["message"]["function_call"]['arguments'])
    
    functions = function_call["functions"]
    # Extract function name and arguments
    function_name = list(functions.keys())[0]
    arguments = functions[function_name]

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

else:
    print("No function call found in the response.")
    print(f"Response: {response}")