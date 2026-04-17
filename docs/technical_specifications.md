# Technical Specifications: Rappi Intelligent Operations Agent

## 1. Project Overview
This project aims to build a high-performance, multi-agent AI system to democratize data access for Rappi's Strategy, Planning & Analytics (SP&A) teams. The system will allow users to query operational metrics in natural language and receive both textual insights and interactive visualizations.

## 2. System Architecture (Multi-Agent System)
Using the **Google Agent Development Kit (ADK)**, the system is structured hierarchically:

### 2.1 Root Agent (The Interface)
- **Role:** Entry point for all user interactions.
- **Key Functions:**
    - Input guardrails (ensuring queries are business-related).
    - Session/Memory management.
    - Intent detection (General Query vs. Detailed Analysis vs. Report Generation).
- **Tools:** Memory Store, Router.

### 2.2 Orchestrator Agent (The Planner)
- **Role:** High-level reasoning and task delegation.
- **Key Functions:**
    - Decomposing complex queries (e.g., "Compare X and Y" -> 1. Get X, 2. Get Y, 3. Compare).
    - Managing the flow of information between specialized sub-agents.
- **Tools:** Planner, Sub-agent Registry.

### 2.3 Specialized Sub-Agents
1.  **Data Analyst Agent:**
    - **Capability:** Python/Pandas expert.
    - **Task:** Writing and executing code to filter, aggregate, and analyze `dummy_data.xlsx`.
    - **Context:** Aware of the Data Dictionary (Lead Penetration, Gross Profit UE, etc.).
2.  **Data Visualizer Agent:**
    - **Capability:** Plotly specialist.
    - **Task:** Transforming JSON/DataFrame results into interactive charts (Line, Bar, Scatter).
3.  **Suggestions Agent:**
    - **Capability:** Proactive Insight Generator.
    - **Task:** Running background checks for anomalies or interesting correlations related to the user's query.

## 3. Data Dictionary & Source
- **Source File:** `data/dummy_data.xlsx`
- **Datasets:**
    - **Metrics Input:** Operational metrics (Lead Penetration, Perfect Order, etc.) by Country/City/Zone/Type/Priority for weeks L8W to L0W.
    - **Orders:** Transactional volume per zone for weeks L8W to L0W.
- **Metric Definitions:** (As per assignment document, e.g., *Perfect Order* = Orders without cancellations or defects / Total Orders).

## 4. Tech Stack & Engineering Standards
- **Environment:** Python 3.12+ managed by `uv`.
- **LLM Layer:** `LiteLLM` for model agnostic implementation (Default: `gpt-4o-mini`).
- **UI:** `Plotly Dash` for a professional, data-centric dashboard interface.
- **Testing:** `pytest` for comprehensive unit and integration coverage.
- **Documentation:** Google-style docstrings and Markdown-based project logs.

## 5. Implementation Roadmap
### Phase 1: Foundation & Data
- Environment setup with `uv`.
- Data loading and cleaning module.
- Validation of metrics calculations.

### Phase 2: Core Chatbot (Multi-Agent)
- Implementation of Root and Orchestrator agents.
- Tool definition for Data Analyst (Pandas sandbox).
- Integration of LiteLLM.

### Phase 3: Visualization & UI
- Implementation of Data Visualizer agent.
- Dash UI development (Chat window + Side panel for charts).

### Phase 4: Automated Insights
- Logic for anomaly detection and trend analysis.
- Executive report generation module (Markdown).

### Phase 5: Refinement & Demo
- Performance tuning.
- Preparing the 5 demo cases.
