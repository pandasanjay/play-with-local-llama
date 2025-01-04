import scrapy
from scrapy_playwright.page import PageMethod
import json
import requests
from crawler_agent.spiders.available_func_for_llm import (
    available_functions,
    parse_llm_output,
    extract_reminder_info
)  # Import your function definitions


class MyCrawlerSpider(scrapy.Spider):
    name = "air_crawler"
    start_urls = ["https://httpbin.org/forms/post"]  # Replace with your target URL
    OLLAMA_API_URL = "http://localhost:11434/api/generate"  # Default Ollama API URL
    OLLAMA_MODEL = "Llama3.2"  # Replace with your Ollama model name

    # def __init__(self):
        # self.llm = pipeline('text-generation', model='/home/sanjay-dev/.llama/checkpoints/Llama3.2-1B/hf-output/', device=0) # Initialize your LLM
       
        # Ensure the path is correct and device is set appropriately (e.g., 'cuda:0' for GPU)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                meta={
                    "playwright": True,
                    "playwright_include_page": True,
                    "playwright_page_methods": [
                        PageMethod(
                            "wait_for_selector", "body"
                        ),  # Wait for the body to load
                    ],
                },
            )

    async def parse(self, response):
        page = response.meta["playwright_page"]
        page_content = await page.content()
        print(f"Length of page content: {len(page_content)}")
        print(page_content)
        prompt = f"""
        You are an agent interacting with a web page. Your goal is to fill out the form on the page and navigate to the next steps if applicable.
        Here is the HTML content of the page:
        ```html
        {page_content}
        ```

        Available actions:
        actions:
        - fill - Fill a form field
        - click - click a button or link or checkbox, radio, dropdown
        - navigate - navigate to a new page
        selector: CSS or XPath selector of the element
        value: Add related generated value to enter (for fill action)

        Respond ONLY with a valid JSON list of actions to perform. Do not include any other text, explanations, or code snippets.

        Build the json as array like below keep all the action in order.
        
        Example of correct JSON output:
         [
            {{"action": "fill", "selector": "[name='custname']", "value": "John Doe"}},
            {{"action": "fill", "selector": "[type='tel'][name='custtel']", "value": "1234567890"}},
            {{"action": "fill", "selector": "[type='email'][name='custemail']", "value": "johndoe@example.com"}},
            {{"action": "click", "selector": "input[type=radio][name='size'][value='large']"}},
            {{"action": "click", "selector": "input[type=checkbox][name='topping'][value='bacon']"}},
            {{"action": "fill", "selector": "[name='comments']", "value": "I need my order by 1 PM"}},
            {{"action": "fill", "selector": "[type='time']", "value": "13:00"}},
            {{"action": "click", "selector": "button"}}
        ]
        
        If no HTML content context provided and no actions are needed, return an empty JSON array [].
        """
        print("-----------------")
        print(prompt)
        print(f"Prompt length: {len(prompt)}")
        # Ollama API call
        try:
            ollama_response = requests.post(
                self.OLLAMA_API_URL,
                json={
                    "model": self.OLLAMA_MODEL,
                    "prompt": prompt,
                    "stream": True,  # Important for single response
                },
                stream=True
                # timeout=30,  # Set a timeout
            )
            ollama_response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            llm_response = extract_reminder_info(ollama_response)
            llm_response = llm_response.replace("```", "")
            # llm_response = json.loads(llm_response)
            # llm_response = ollama_response.json()["response"]

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error communicating with Ollama API: {e}")
            await page.close()
            return

        actions = parse_llm_output(llm_response)
        print(f"Actions to perform: {actions}")
        if actions:
            for action in actions:
                if action["action"] == "fill":
                    try:
                        await page.fill(action["selector"], action["value"])
                    except Exception as e:
                        self.logger.error(
                            f"Error filling field: {e}, selector: {action['selector']}"
                        )
                elif action["action"] == "click":
                    try:
                        await page.click(action["selector"])
                    except Exception as e:
                        self.logger.error(
                            f"Error clicking element: {e}, selector: {action['selector']}"
                        )
                elif action["action"] == "navigate":
                    try:
                        yield scrapy.Request(
                            action["url"],
                            meta={
                                "playwright": True,
                                "playwright_include_page": True,
                                "playwright_page_methods": [
                                    PageMethod(
                                        "wait_for_selector", "body"
                                    ),  # Wait for the next page to load
                                ],
                            },
                        )
                    except Exception as e:
                        self.logger.error(
                            f"Error navigating: {e}, url: {action['url']}"
                        )

        await page.close()
