# Rappi Intelligent Operations Agent Context

## 1. Project Overview
This project is a multi-agent system designed to democratize data access for Rappi's Strategy, Planning & Analytics teams. It processes an Excel dataset of operational metrics and answers complex business questions using natural language.

## 2. Architecture (Google ADK)
The system is built using the **Google Agent Development Kit (ADK)** (google-adk) and follows a strict hierarchy using LlmAgent:
*   **root_agent** (`src/agents/root/`): Entry point. Handles guardrails and memory.
    *   Sub-agent: **orchestrator_agent**
*   **orchestrator_agent** (`src/agents/orchestrator/`): The planner. Decomposes queries and delegates.
    *   Sub-agents: **analyst_agent**, **visualizer_agent**
*   **analyst_agent** (`src/agents/analyst/`): Executes pandas queries via the `run_pandas_query` tool.
*   **visualizer_agent** (`src/agents/visualizer/`): Generates Plotly chart specifications (JSON) via `generate_chart_spec`.

Each agent is organized in its own directory with the following structure:
- `agent.py`: Agent definition (LlmAgent).
- `prompt.py`: System instructions/prompts (in Spanish).
- `tools.py`: Agent-specific tools.

## 3. Tech Stack & Environment
*   **Dependency Management**: uv. Always use `uv add <package>` or `uv run <command>`.
*   **LLM Orchestration**: litellm (configured via .env).
*   **Data Processing**: pandas and numpy.
*   **UI/UX**: Plotly Dash (Phase 3).
*   **Testing**: pytest (Phase 4).

## 4. Data Context
*   **Source**: data/dummy_data.xlsx
*   **Loader**: src/data_loader.py transforms wide-format week data into a long-format DataFrame.
*   **State Management**: src/agents/shared_state.py holds the singleton DataLoader instance so all agents query the same in-memory DataFrame.
*   **Time Dimension**: Data spans 9 weeks (L8W = 8 weeks ago, L0W = current week).

## 5. Engineering Standards
*   **Dependencies**: Never use pip directly; always use uv.
*   **Agent Definition**: Always use LlmAgent from google.adk.agents (not Agent). Use the sub_agents parameter to define hierarchy. Organize each agent in its own directory with `agent.py`, `prompt.py`, and `tools.py`.
*   **Language**: Developer communication and `GEMINI.md` must be in English. The application UI, agent prompts, and all files in the `docs/` directory must be in Spanish.
*   **Data Access**: Agents must not load the Excel file directly; they must use src.agents.shared_state.get_combined_data().
*   **Safety**: Ensure the analyst_agent uses a restricted execution environment (eval with local variables) to prevent destructive system commands.
*   **Logging**: Use the standard Python `logging` module in `main.py` and tools. Monitor the agent's "chain of thought" by logging tool calls and text chunks. Respect the `LOG_LEVEL` environment variable.
*   **Naming Conventions**: The `test_` prefix for files is strictly reserved for actual testing frameworks (e.g., pytest). Do not use `test_` for general scripts or verifications.
