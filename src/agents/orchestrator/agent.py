# src/agents/orchestrator/agent.py

from google.adk.agents import SequentialAgent
from src.agents.analyst.agent import analyst_agent
from src.agents.visualizer.agent import visualizer_agent
from src.agents.suggestion.agent import suggestion_agent

orchestrator_agent = SequentialAgent(
    name="rappi_orchestrator",
    sub_agents=[analyst_agent, suggestion_agent, visualizer_agent]
)
