import requests
import json
from utils import handle_stream_data
import schedule
import time

 
def set_reminder(query):
    """
    Sets a reminder using the user's query and Ollama API.
    """
    # Prepare the API request
    url = "http://localhost:11434/api/generate"  # Ollama's API endpoint
    data = {
        "model": "Llama3.2:1b",  # Or the name of your loaded model
        "prompt": f"action - 'Set a reminder'. Respond with a JSON object containing the action, task, time_interval (convert to minute) and time_type (e.g minute). Do not include any other text or formatting. Here is the user's query: {query}",
        # "stream": True,  # Tell Ollama to stream the response
    }
    response = requests.post(url, json=data, stream=True)

    

    reminder_info = handle_stream_data.extract_reminder_info(response)

    # Send the request to Ollama
    # Parse the JSON response
    try:
        # Remove backticks from reminder_info
        reminder_info = reminder_info.replace("```", "")
        reminder_data = json.loads(reminder_info)  # Directly parse the response
        task = reminder_data.get("task", "")
        time_interval = reminder_data.get("time_interval", 0)

        print(reminder_data)

        # Schedule the reminder using the `schedule` library
        # Scheduling logic using `schedule` library
        schedule.every(time_interval).minutes.do(lambda: print(f"Reminder: {task}"))
        # Add more conditions for different time intervals (e.g., days, weeks)
        # This will print the reminder every hour

        while True:
            schedule.run_pending()
            time.sleep(1)

    except json.JSONDecodeError:
        print(f"Error: Invalid JSON response from LLM. {reminder_info}")
    except requests.RequestException as e:
        print(f"Error: An error occurred while making the request. {response}", e)
    except Exception as e:
        print(f"Error: An unexpected error occurred. {response}", e)


# Get user input
query = input("What would you like to be reminded about? ")

# Set the reminder
set_reminder(query)
