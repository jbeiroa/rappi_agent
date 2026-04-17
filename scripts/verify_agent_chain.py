import asyncio
import os
from src.agents.root.agent import root_agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

async def verify_chain():
    print("--- Starting Rappi Agent Delegation Verification ---")
    print("Initializing Runner and Session Service...\n")
    
    session_service = InMemorySessionService()
    # Pre-create the session to avoid "Session not found"
    await session_service.create_session(
        user_id="test_user", 
        session_id="test_session",
        app_name="rappi_ops_agent"
    )
    
    # Set up the Runner
    runner = Runner(
        agent=root_agent,
        app_name="rappi_ops_agent",
        session_service=session_service
    )
    
    scenarios = [
        {
            "name": "Data Query (Average Lead Penetration)",
            "query": "What is the average Lead Penetration in Mexico for the current week?"
        },
        {
            "name": "Visualization Request (Profit Trends)",
            "query": "Show me a line chart of the Gross Profit UE evolution in Chapinero over the last 8 weeks."
        }
    ]
    
    for scenario in scenarios:
        print(f"Scenario: {scenario['name']}")
        print(f"Query: {scenario['query']}")
        print("-" * 30)
        
        # Wrap query in Content object
        message = types.Content(
            role="user",
            parts=[types.Part.from_text(text=scenario['query'])]
        )
        
        full_response = ""
        try:
            # Runner.run_async requires user_id, session_id, and new_message (Content object)
            async for event in runner.run_async(
                user_id="test_user",
                session_id="test_session",
                new_message=message
            ):
                # Accumulate text from events
                if hasattr(event, 'content') and event.content and hasattr(event.content, 'parts'):
                    for part in event.content.parts:
                        if hasattr(part, 'text') and part.text:
                            print(part.text, end="", flush=True)
                            full_response += part.text
                
                # Log tool calls for deeper verification
                if hasattr(event, 'tool_call') and event.tool_call:
                    print(f"\n[Tool Call: {event.tool_call.name}]")
            
            print(f"\n\nFinal Full Response length: {len(full_response)}")
        except Exception as e:
            print(f"\nError during verification: {e}")
        
        print("\n" + "=" * 50 + "\n")

if __name__ == "__main__":
    if not os.getenv("GEMINI_API_KEY"):
        print("Warning: GEMINI_API_KEY not found. Default Gemini models will fail.")
    
    asyncio.run(verify_chain())
