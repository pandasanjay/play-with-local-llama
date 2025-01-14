fun_specs = [
    {
        "name": "add_numbers",
        "description": "Adds two numbers and returns the sum.",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {"type": "number", "description": "The first number."},
                "b": {"type": "number", "description": "The second number."},
            },
            "required": ["a", "b"],
        },
    },
    {
        "name": "get_current_date",
        "description": "Returns the current date in YYYY-MM-DD format.",
        "parameters": {"type": "object", "properties": {}},
    },
    {
        "name": "string_length",
        "description": "Returns the length of a string.",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "The input string."},
            },
            "required": ["text"],
        },
    },
    {
        "name": "get_html",
        "description": "Fetches the HTML content of a given URL.",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "The URL to fetch."},
            },
            "required": ["url"],
        },
    },
]