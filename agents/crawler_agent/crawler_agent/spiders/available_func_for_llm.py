import json

def fill_form_field(selector: str, value: str):
    """Fills a form field.

    Args:
        selector: CSS or XPath selector of the field.
        value: The value to enter.
    """
    return {"action": "fill", "selector": selector, "value": value}

def click_element(selector: str):
    """Clicks an element.

    Args:
        selector: CSS or XPath selector of the element.
    """
    return {"action": "click", "selector": selector}

def navigate_to_page(url: str):
    """Navigates to a new page.

    Args:
        url: The URL to navigate to.
    """
    return {"action": "navigate", "url": url}


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
# Function to parse LLM output and check if the output is valid JSON
def parse_llm_output(llm_output):
    try:
      actions = json.loads(llm_output)
      return actions
    except json.JSONDecodeError:
      print(f"Invalid JSON output from LLM: {llm_output}")
      return None

available_functions = {
    "fill_form_field": fill_form_field,
    "click_element": click_element,
    "navigate_to_page": navigate_to_page,
}