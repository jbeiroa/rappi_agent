# src/agents/visualizer/agent.py

from google.adk.agents import LlmAgent
from src.agents.visualizer.prompt import VISUALIZER_INSTRUCTIONS
from src.agents.visualizer.tools import generate_chart_spec

visualizer_agent = LlmAgent(
    name="rappi_visualizer_agent",
    model="gemini-3-flash-preview",
    instruction=VISUALIZER_INSTRUCTIONS,
    tools=[generate_chart_spec]
)
