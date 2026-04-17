# src/agents/orchestrator/agent.py

from google.adk.agents import LlmAgent
from src.agents.orchestrator.prompt import ORCHESTRATOR_INSTRUCTIONS
from src.agents.analyst.agent import analyst_agent
from src.agents.visualizer.agent import visualizer_agent

orchestrator_agent = LlmAgent(
    name="rappi_orchestrator",
    model="gemini-3-flash-preview",
    instruction=ORCHESTRATOR_INSTRUCTIONS,
    sub_agents=[analyst_agent, visualizer_agent]
)
