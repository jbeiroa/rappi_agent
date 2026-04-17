# src/agents/root/agent.py

from google.adk.agents import LlmAgent
from src.agents.root.prompt import ROOT_INSTRUCTIONS
from src.agents.orchestrator.agent import orchestrator_agent
import os
from dotenv import load_dotenv

load_dotenv()

root_agent = LlmAgent(
    name="rappi_root_agent",
    model="gemini-3-flash-preview",
    instruction=ROOT_INSTRUCTIONS,
    sub_agents=[orchestrator_agent]
)
