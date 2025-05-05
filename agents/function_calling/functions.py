import datetime
import requests

def add_numbers(a, b):
  """Adds two numbers and returns the sum.

  Args:
    a: The first number.
    b: The second number.

  Returns:
    The sum of a and b.
  """
  return a + b

def get_current_date():
  """Returns the current date in YYYY-MM-DD format.

  Returns:
    The current date as a string.
  """
  return datetime.date.today().strftime("%Y-%m-%d")

def string_length(text):
  """Returns the length of a string.

  Args:
    text: The input string.

  Returns:
    The length of the string.
  """
  return len(text)

def get_html(url):
  """Fetches the HTML content of a given URL.

  Args:
    url: The URL to fetch.

  Returns:
    The HTML content as a string, or None if an error occurred.
  """
  try:
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad status codes
    return response.text
  except requests.exceptions.RequestException as e:
    print(f"Error fetching URL: {e}")
    return None

# Example usage (you can uncomment these to test the functions)
# print(add_numbers(5, 3))
# print(get_current_date())
# print(string_length("Hello world!"))
# print(get_html("https://www.example.com"))