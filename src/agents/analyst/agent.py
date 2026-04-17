# src/agents/analyst/agent.py

from google.adk.agents import LlmAgent
from src.agents.analyst.prompt import ANALYST_INSTRUCTIONS
from src.agents.analyst.tools import run_pandas_query

analyst_agent = LlmAgent(
    name="rappi_analyst_agent",
    model="gemini-3-flash-preview",
    instruction=ANALYST_INSTRUCTIONS,
    tools=[run_pandas_query]
)
