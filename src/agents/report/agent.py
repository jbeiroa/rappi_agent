# src/agents/report/agent.py

from google.adk.agents import LlmAgent
from src.agents.report.prompt import REPORT_INSTRUCTIONS
import os

report_agent = LlmAgent(
    name="rappi_report_agent",
    model="gemini-3-flash-preview",
    instruction=REPORT_INSTRUCTIONS
)
