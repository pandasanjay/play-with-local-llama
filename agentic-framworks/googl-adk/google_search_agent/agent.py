from google.adk.agents import Agent
from google.adk.tools import google_search  # Import the tool
from opik.integrations.adk import OpikTracer

opik_tracer = OpikTracer()

root_agent = Agent(
   # A unique name for the agent.
   name="basic_search_agent",
   # The Large Language Model (LLM) that agent will use.
   model="gemini-2.0-flash-exp",
   # model="gemini-2.0-flash-live-001",  # New streaming model version as of Feb 2025
   # A short description of the agent's purpose.
   description="Agent to answer questions using Google Search.",
   # Instructions to set the agent's behavior.
   instruction="You are an expert researcher. You always stick to the facts.",
   # Add google_search tool to perform grounding with Google search.
   tools=[google_search],
   before_agent_callback=opik_tracer.before_agent_callback,
   after_agent_callback=opik_tracer.after_agent_callback,
   before_model_callback=opik_tracer.before_model_callback,
   after_model_callback=opik_tracer.after_model_callback,
   before_tool_callback=opik_tracer.before_tool_callback,
   after_tool_callback=opik_tracer.after_tool_callback,
)