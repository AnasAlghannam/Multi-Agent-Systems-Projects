import asyncio
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import get_llm
from beeai_framework.agents.requirement import RequirementAgent
from beeai_framework.memory import UnconstrainedMemory

async def minimal_tracked_agent_example():
    """
    Minimal RequirementAgent
    """
    llm = get_llm(temperature=0)
    
    # CONSISTENT SYSTEM PROMPT (used in all examples)
    SYSTEM_INSTRUCTIONS = """You are an expert cybersecurity analyst specializing in threat assessment and risk analysis.

Your methodology:
1. Analyze the threat landscape systematically
2. Research authoritative sources when available
3. Provide comprehensive risk assessment with actionable recommendations
4. Focus on practical, implementable security measures"""
    # Minimal RequirementAgent
    minimal_agent = RequirementAgent(
        llm=llm,
        tools=[],  # No tools yet
        memory=UnconstrainedMemory(),
        instructions=SYSTEM_INSTRUCTIONS
    )
    
    # CONSISTENT QUERY (used in all examples)
    ANALYSIS_QUERY = """Analyze the cybersecurity risks of quantum computing for financial institutions. 
    What are the main threats, timeline for concern, and recommended preparation strategies?"""
    
    result = await minimal_agent.run(ANALYSIS_QUERY)
    print(f"\n💬 Pure LLM Analysis:\n{result.last_message.text}")

async def main() -> None:
    logging.getLogger('asyncio').setLevel(logging.CRITICAL)
    await minimal_tracked_agent_example()

if __name__ == "__main__":
    asyncio.run(main())
