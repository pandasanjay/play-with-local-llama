"""
This example is from OpenAI Cookbook, but modified to work with Gemini. The original example can be found at:
https://github.com/openai/openai-cookbook/blob/main/examples/Structured_outputs_multi_agent.ipynb
This script defines a multi-agent system for processing, analyzing, and visualizing data using OpenAI's API. The system consists of three main agents:
1. Data Processing Agent: Cleans, transforms, and aggregates data.
2. Analysis Agent: Performs statistical, correlation, and regression analysis.
3. Visualization Agent: Creates bar charts, line charts, and pie charts.
Functions:
- clean_data(data): Cleans the provided data by removing duplicates.
- stat_analysis(data): Performs statistical analysis on the given dataset.
- plot_line_chart(data, x_key, y_key, plot_type="scatter"): Creates a line chart or bar chart from the provided data.
- execute_tool(tool_calls, messages): Executes the specified tools based on the tool calls.
- handle_data_processing_agent(query, conversation_messages): Handles the data processing agent's tasks.
- handle_analysis_agent(query, conversation_messages): Handles the analysis agent's tasks.
- handle_visualization_agent(query, conversation_messages): Handles the visualization agent's tasks.
- handle_user_message(user_query, conversation_messages=[]): Handles the user's query and routes it to the relevant agents.
Example usage:
- The user provides a query with data and requests for data cleaning, statistical analysis, and visualization.
- The system processes the query, routes it to the appropriate agents, and executes the required tasks.
"""

from openai import OpenAI
from IPython.display import Image
import json
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO
import numpy as np
import os
from dotenv import load_dotenv  # Add this line to import load_dotenv

load_dotenv()  # Add this line to load environment variables from the root .env file

# MODEL = "dwightfoster03/functionary-small-v3.1"

# client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")


MODEL = "gemini-2.0-flash-exp"
google_key = os.getenv("GOOGLE_API_KEY")  # Replace hardcoded key with environment variable
client = OpenAI(
    api_key=google_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
triaging_system_prompt = """You are a Triaging Agent. Your role is to assess the user's query and route it to the relevant agents. The agents available are:
- Data Processing Agent: Cleans, transforms, and aggregates data.
- Analysis Agent: Performs statistical, correlation, and regression analysis.
- Visualization Agent: Creates bar charts, line charts, and pie charts.

Use the send_query_to_agents tool to forward the user's query to the relevant agents. Also, use the speak_to_user tool to get more information from the user if needed."""

processing_system_prompt = """
You are a Data Processing Agent. Your role is to clean, transform, and aggregate data. You should always return a tool from tool definitions.
"""

analysis_system_prompt = """You are an Analysis Agent. Your role is to perform statistical, correlation, and regression analysis using the following tools:
- stat_analysis
- correlation_analysis
- regression_analysis"""

visualization_system_prompt = """You are a Visualization Agent. Your role is to create bar charts, line charts, and pie charts using the following tools:
- create_bar_chart
- create_line_chart
- create_pie_chart"""


triage_tools = [
    {
        "type": "function",
        "function": {
            "name": "send_query_to_agents",
            "description": "Sends the user query to relevant agents based on their capabilities.",
            "parameters": {
                "type": "object",
                "properties": {
                    "agents": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "An array of agent names to send the query to.",
                    },
                    "query": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Create a plan from user query for each agent.",
                    },
                },
                "required": ["agents", "query"],
            },
        },
        #"strict": True,
    }
]

preprocess_tools = [
    {
        "type": "function",
        "function": {
            "name": "clean_data",
            "description": "Cleans the provided data by removing duplicates and handling missing values.",
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {
                        "type": "string",
                        "description": "The dataset to clean. Should be in a suitable format such as JSON or CSV.",
                    }
                },
                "required": ["data"],
                "additionalProperties": False,
            },
        },
        #"strict": True,
    },
    {
        "type": "function",
        "function": {
            "name": "transform_data",
            "description": "Transforms data based on specified rules.",
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {
                        "type": "string",
                        "description": "The data to transform. Should be in a suitable format such as JSON or CSV.",
                    },
                    "rules": {
                        "type": "string",
                        "description": "Transformation rules to apply, specified in a structured format.",
                    },
                },
                "required": ["data", "rules"],
                "additionalProperties": False,
            },
        },
        # "strict": True
    },
    {
        "type": "function",
        "function": {
            "name": "aggregate_data",
            "description": "Aggregates data by specified columns and operations.",
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {
                        "type": "string",
                        "description": "The data to aggregate. Should be in a suitable format such as JSON or CSV.",
                    },
                    "group_by": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Columns to group by.",
                    },
                    "operations": {
                        "type": "string",
                        "description": "Aggregation operations to perform, specified in a structured format.",
                    },
                },
                "required": ["data", "group_by", "operations"],
                "additionalProperties": False,
            },
        },
        #"strict": True,
    },
]


analysis_tools = [
    {
        "type": "function",
        "function": {
            "name": "stat_analysis",
            "description": "Performs statistical analysis on the given dataset.",
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {
                        "type": "string",
                        "description": "The dataset to analyze. Should be in a suitable format such as JSON or CSV.",
                    }
                },
                "required": ["data"],
                "additionalProperties": False,
            },
        },
        #"strict": True,
    },
    {
        "type": "function",
        "function": {
            "name": "correlation_analysis",
            "description": "Calculates correlation coefficients between variables in the dataset.",
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {
                        "type": "string",
                        "description": "The dataset to analyze. Should be in a suitable format such as JSON or CSV.",
                    },
                    "variables": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of variables to calculate correlations for.",
                    },
                },
                "required": ["data", "variables"],
                "additionalProperties": False,
            },
        },
        #"strict": True,
    },
    {
        "type": "function",
        "function": {
            "name": "regression_analysis",
            "description": "Performs regression analysis on the dataset.",
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {
                        "type": "string",
                        "description": "The dataset to analyze. Should be in a suitable format such as JSON or CSV.",
                    },
                    "dependent_var": {
                        "type": "string",
                        "description": "The dependent variable for regression.",
                    },
                    "independent_vars": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of independent variables.",
                    },
                },
                "required": ["data", "dependent_var", "independent_vars"],
                "additionalProperties": False,
            },
        },
        #"strict": True,
    },
]

visualization_tools = [
    {
        "type": "function",
        "function": {
            "name": "create_bar_chart",
            "description": "Creates a bar chart from the provided data.",
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {
                        "type": "string",
                        "description": "The data for the bar chart. Should be in a suitable format such as JSON or CSV.",
                    },
                    "x": {"type": "string", "description": "Column for the x-axis."},
                    "y": {"type": "string", "description": "Column for the y-axis."},
                },
                "required": ["data", "x", "y"],
                "additionalProperties": False,
            },
        },
        #"strict": True,
    },
    {
        "type": "function",
        "function": {
            "name": "create_line_chart",
            "description": "Creates a line chart from the provided data.",
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {
                        "type": "string",
                        "description": "The data for the line chart. Should be in a suitable format such as JSON or CSV.",
                    },
                    "x": {"type": "string", "description": "Column for the x-axis."},
                    "y": {"type": "string", "description": "Column for the y-axis."},
                },
                "required": ["data", "x", "y"],
                "additionalProperties": False,
            },
        },
        #"strict": True,
    },
    {
        "type": "function",
        "function": {
            "name": "create_pie_chart",
            "description": "Creates a pie chart from the provided data.",
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {
                        "type": "string",
                        "description": "The data for the pie chart. Should be in a suitable format such as JSON or CSV.",
                    },
                    "labels": {
                        "type": "string",
                        "description": "Column for the labels.",
                    },
                    "values": {
                        "type": "string",
                        "description": "Column for the values.",
                    },
                },
                "required": ["data", "labels", "values"],
                "additionalProperties": False,
            },
        },
        #"strict": True,
    },
]


# Example query

user_query = """
Below is some data. I want you to first remove the duplicates then analyze the statistics of the data as well as plot a line chart.

house_size (m3), house_price ($)
90, 100
80, 90
100, 120
90, 100
"""


def clean_data(data):
    data_io = StringIO(data)
    df = pd.read_csv(data_io, sep=",")
    df_deduplicated = df.drop_duplicates()
    return df_deduplicated


def stat_analysis(data):
    data_io = StringIO(data)
    df = pd.read_csv(data_io, sep=",")
    return df.describe()


def plot_line_chart(data, x_key, y_key, plot_type="scatter"):
    data = json.loads(data)
    print('data:x', data[x_key], x_key)
    print('data:Y', data[y_key], y_key)
    # Dynamically extract x and y data based on provided keys
    try:
        x_values = list(data[x_key].values())
        y_values = list(data[y_key].values())
    except KeyError as e:
        print(f"Key not found in data: {e}")
        return
    
    if plot_type == "scatter":
        # Create the scatter plot with connected points
        plt.plot(x_values, y_values, marker='o', linestyle='-')
        plt.xlabel(x_key)
        plt.ylabel(y_key)
        plt.title(f'{y_key} vs. {x_key}')

    elif plot_type == "bar":
        # Create the bar chart
          # Define the bar width
        bar_width = 0.35

        # Generate x-axis positions for the bars
        index = range(len(x_values))

        # Create the figure and the first y-axis
        fig, ax1 = plt.subplots()

        # Create bars for house sizes
        ax1.bar(index, x_values, bar_width, label= x_key)
        ax1.set_xlabel('House Index')
        ax1.set_ylabel(x_key, color='b')
        ax1.tick_params('y', labelcolor='b')
        ax1.set_xticks(index)
        ax1.set_xticklabels([f'Data {i+1}' for i in index])  # You can customize these labels

        # Create a second y-axis for house prices
        ax2 = ax1.twinx()
        ax2.bar([i + bar_width for i in index], y_values, bar_width, label= y_key, color='r')
        ax2.set_ylabel(y_key, color='r')
        ax2.tick_params('y', labelcolor='r')

        # Add title and legend
        plt.title(f'{x_key} and {y_key}')
        fig.tight_layout()
        fig.legend(loc="upper left", bbox_to_anchor=(0,1), bbox_transform=ax1.transAxes)


    else:
        print("Invalid plot type specified. Choose 'scatter' or 'bar'.")
        return

    # Display the plot
    plt.grid(True)
    plt.show()


# Define the function to execute the tools
def execute_tool(tool_calls, messages):
    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        tool_arguments = json.loads(tool_call.function.arguments)

        if tool_name == "clean_data":
            # Simulate data cleaning
            cleaned_df = clean_data(tool_arguments["data"])
            cleaned_data = {"cleaned_data": cleaned_df.to_dict()}
            messages.append(
                {"role": "tool", "name": tool_name, "content": json.dumps(cleaned_data)}
            )
            print("Cleaned data: ", cleaned_df)
        elif tool_name == "transform_data":
            # Simulate data transformation
            transformed_data = {"transformed_data": "sample_transformed_data"}
            messages.append(
                {
                    "role": "tool",
                    "name": tool_name,
                    "content": json.dumps(transformed_data),
                }
            )
        elif tool_name == "aggregate_data":
            # Simulate data aggregation
            aggregated_data = {"aggregated_data": "sample_aggregated_data"}
            messages.append(
                {
                    "role": "tool",
                    "name": tool_name,
                    "content": json.dumps(aggregated_data),
                }
            )
        elif tool_name == "stat_analysis":
            # Simulate statistical analysis
            stats_df = stat_analysis(tool_arguments["data"])
            stats = {"stats": stats_df.to_dict()}
            messages.append(
                {"role": "tool", "name": tool_name, "content": json.dumps(stats)}
            )
            print("Statistical Analysis: ", stats_df)
        elif tool_name == "correlation_analysis":
            # Simulate correlation analysis
            correlations = {"correlations": "sample_correlations"}
            messages.append(
                {"role": "tool", "name": tool_name, "content": json.dumps(correlations)}
            )
        elif tool_name == "regression_analysis":
            # Simulate regression analysis
            regression_results = {"regression_results": "sample_regression_results"}
            messages.append(
                {
                    "role": "tool",
                    "name": tool_name,
                    "content": json.dumps(regression_results),
                }
            )
        elif tool_name == "create_bar_chart":
            # Simulate bar chart creation
            bar_chart = {"bar_chart": "sample_bar_chart"}
            messages.append(
                {"role": "tool", "name": tool_name, "content": json.dumps(bar_chart)}
            )
        elif tool_name == "create_line_chart":
            # Simulate line chart creation
            line_chart = {"line_chart": "sample_line_chart"}
            messages.append(
                {"role": "tool", "name": tool_name, "content": json.dumps(line_chart)}
            )
            f_data = tool_arguments['data']
            print(tool_arguments)
            plot_line_chart(f_data, tool_arguments['x'], tool_arguments['y'])
        elif tool_name == "create_pie_chart":
            # Simulate pie chart creation
            pie_chart = {"pie_chart": "sample_pie_chart"}
            messages.append(
                {"role": "tool", "name": tool_name, "content": json.dumps(pie_chart)}
            )
    return messages


# Define the functions to handle each agent's processing
def handle_data_processing_agent(query, conversation_messages):
    conversation_messages.append({"role": "system", "content": processing_system_prompt})
    # conversation_messages.append(use_query)
    conversation_messages.append({"role": "user", "content": query})
    
    print("messages:", conversation_messages)
    response = client.chat.completions.create(
        model=MODEL,
        messages=conversation_messages,
        temperature=0,
        tools=preprocess_tools,
        tool_choice="auto",
    )
    print(response.choices[0].message)
    # conversation_messages.append(
    #     [tool_call.function for tool_call in response.choices[0].message.tool_calls]
    # )
    execute_tool(response.choices[0].message.tool_calls, conversation_messages)


def handle_analysis_agent(query, conversation_messages):
    conversation_messages.append({"role": "system", "content": analysis_system_prompt})
    conversation_messages.append({"role": "user", "content": query})

    response = client.chat.completions.create(
        model=MODEL,
        messages=conversation_messages,
        temperature=0,
        tools=analysis_tools,
        tool_choice="auto",
    )
    print(response.choices[0].message.tool_calls)
    # conversation_messages.append(
    #     [tool_call.function for tool_call in response.choices[0].message.tool_calls]
    # )
    execute_tool(response.choices[0].message.tool_calls, conversation_messages)


def handle_visualization_agent(query, conversation_messages):
    conversation_messages.append({"role": "system", "content": visualization_system_prompt})
    conversation_messages.append({"role": "user", "content": query})

    response = client.chat.completions.create(
        model=MODEL,
        messages=conversation_messages,
        temperature=0,
        tools=visualization_tools,
        tool_choice="auto",
    )
    print(response.choices[0].message)
    # conversation_messages.append(
    #     [tool_call.function for tool_call in response.choices[0].message.tool_calls]
    # )
    execute_tool(response.choices[0].message.tool_calls, conversation_messages)


# Function to handle user input and triaging
def handle_user_message(user_query, conversation_messages=[]):
    user_message = {"role": "user", "content": user_query}
    conversation_messages.append(user_message)

    messages = [{"role": "system", "content": triaging_system_prompt}]
    messages.extend(conversation_messages)

    print("User Query:", messages)
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0,
        tools=triage_tools,
        tool_choice="auto",
    )

    print(response.choices[0].message)

    # conversation_messages.append(
    #     [tool_call.function for tool_call in response.choices[0].message.tool_calls]
    # )

    for tool_call in response.choices[0].message.tool_calls:
        if tool_call.function.name == "send_query_to_agents":
            arguments = json.loads(tool_call.function.arguments)
            agents = arguments["agents"]
            query = arguments["query"]
            print("Query:", query)
            print("Agents:", agents)
            for i, agent in enumerate(agents):
                if agent == "Data Processing Agent":
                    handle_data_processing_agent(query[i], conversation_messages)
                elif agent == "Analysis Agent":
                    handle_analysis_agent(query[i], conversation_messages)
                elif agent == "Visualization Agent":
                    handle_visualization_agent(query[i], conversation_messages)

    return conversation_messages


handle_user_message(user_query)
