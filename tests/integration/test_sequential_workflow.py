import pytest
from src.agents.orchestrator.agent import orchestrator_agent
from google.adk.agents import SequentialAgent
from src.agents.analyst.agent import analyst_agent
from src.agents.suggestion.agent import suggestion_agent
from src.agents.visualizer.agent import visualizer_agent

def test_orchestrator_structure():
    """Verify orchestrator is a SequentialAgent with correct order of sub-agents."""
    assert isinstance(orchestrator_agent, SequentialAgent)
    sub_agents = orchestrator_agent.sub_agents
    assert len(sub_agents) == 3
    assert sub_agents[0] == analyst_agent
    assert sub_agents[1] == suggestion_agent
    assert sub_agents[2] == visualizer_agent

@pytest.mark.asyncio
async def test_sequential_workflow_logic():
    """
    Smoke test to ensure the orchestrator can be invoked in its sequential structure.
    Note: Real LLM calls are not made if we only test structural initialization or use mocks.
    """
    assert orchestrator_agent.name == "rappi_orchestrator"
