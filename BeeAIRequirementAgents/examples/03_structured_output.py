import asyncio
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import get_llm
from pydantic import BaseModel, Field
from typing import List
from beeai_framework.backend import UserMessage, SystemMessage

# Define a structured output for business planning
class BusinessPlan(BaseModel):
    """A comprehensive business plan structure."""
    business_name: str = Field(description="Catchy name for the business")
    elevator_pitch: str = Field(description="30-second description of the business")
    target_market: str = Field(description="Primary target audience")
    unique_value_proposition: str = Field(description="What makes this business special")
    revenue_streams: List[str] = Field(description="Ways the business will make money")
    startup_costs: str = Field(description="Estimated initial investment needed")
    key_success_factors: List[str] = Field(description="Critical elements for success")
async def structured_output_example():
    llm = get_llm(temperature=0)
    
    messages = [
        SystemMessage(content="You are an expert business consultant and entrepreneur."),
        UserMessage(content="Create a business plan for a mobile app that helps people find and book unique local experiences in their city.")
    ]
    
    # Generate structured response using create_structure() method
    # response_format makes the model return data matching the schema.
    response = await llm.run(messages, response_format=BusinessPlan)
    plan = BusinessPlan.model_validate_json(response.get_text_content())
    
    print("User: Create a business plan for a mobile app that helps people find and book unique local experiences in their city.")
    print("\n🚀 AI-Generated Business Plan:")
    print(f"💡 Business Name: {plan.business_name}")
    print(f"🎯 Elevator Pitch: {plan.elevator_pitch}")
    print(f"👥 Target Market: {plan.target_market}")
    print(f"⭐ Unique Value Proposition: {plan.unique_value_proposition}")
    print(f"💰 Revenue Streams: {', '.join(plan.revenue_streams)}")
    print(f"💵 Startup Costs: {plan.startup_costs}")
    print(f"🔑 Key Success Factors:")
    for factor in plan.key_success_factors:
        print(f"  - {factor}")

async def main() -> None:
    logging.getLogger('asyncio').setLevel(logging.CRITICAL) # Suppress unwanted warnings
    await structured_output_example()

if __name__ == "__main__":
    asyncio.run(main())
