from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

chat_completion = client.chat.completions.create(
    model="dwightfoster03/functionary-small-v3.1",
    messages=[{"role": "user",
            "content": "What is the weather for Istanbul?"}
    ],
    tools=[{
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "Get the current weather",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA"
                        }
                    },
                    "required": ["location"]
                }
            }
        }],
    tool_choice="auto"
)

print(chat_completion.choices[0].message.tool_calls[0].function)