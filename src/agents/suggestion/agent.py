# src/agents/suggestion/agent.py

from google.adk.agents import LlmAgent
from src.agents.suggestion.prompt import SUGGESTION_INSTRUCTIONS
from src.agents.suggestion.tools import get_available_metrics

suggestion_agent = LlmAgent(
    name="rappi_suggestion_agent",
    model="gemini-3-flash-preview",
    instruction=SUGGESTION_INSTRUCTIONS,
    tools=[get_available_metrics]
)
