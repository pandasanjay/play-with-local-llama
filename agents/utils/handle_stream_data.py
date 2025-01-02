import json
def extract_reminder_info(response):
        reminder_info = ""
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode("utf-8")
                try:
                    json_line = json.loads(decoded_line)
                    if "response" in json_line:
                        reminder_info += json_line["response"]
                except json.JSONDecodeError:
                    pass  # Ignore lines that are not valid JSON
        return reminder_info